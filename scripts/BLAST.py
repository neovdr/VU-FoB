# Fundamentals of Bioinformatics
# Exercise 5
# Get matching sequences using NCBI BLAST

from time import sleep
import re
import urllib2
import pickle
import os.path

def query_server(protein_id):
    if (os.path.exists(protein_id + '_BLAST.html')):
        f = open(protein_id + '_BLAST.html')
        result = f.read()
        f.close()
        return result
    baseUrl = 'http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Put&QUERY='
    url = baseUrl + protein_id + '&DATABASE=swissprot&PROGRAM=blastp&FILTER=T&EXPECT=100&FORMAT_TYPE=Text'
    fh = urllib2.urlopen(url)
    query = fh.read() 
    fh.close() 
        
    # Find a comment with request id (RID) and estimated time of completion
    # (RTOE). It looks like this:
    # <!--QBlastInfoBegin
    #     RID = 7WS3FMZW01P
    #     RTOE = 11
    # QBlastInfoEnd
    # -->
    m = re.search("^<\!--QBlastInfoBegin\s*RID = (.*)\s*RTOE = (.*)$", query, re.MULTILINE)
    rid = m.groups()[0]
    rtoe = int(m.groups()[1])

    status = ""
    wait_time = rtoe + 1
    while (status != "READY"): 
        print "Waiting {0:d} seconds for BLAST results".format(wait_time)
        sleep(wait_time)
        baseurl = 'http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&RID='
        url = baseurl + rid + '&FORMAT_OBJECT=Alignment&ALIGNMENT_VIEW=Tabular&FORMAT_TYPE=Text&ALIGNMENTS=100'
        fh = urllib2.urlopen(url)
        result = fh.read() 
        fh.close()

        # Find a comment with the request status. It looks like this:
        # <!--
        # QBlastInfoBegin
        #     Status=WAITING
        # QBlastInfoEnd
        # -->
        m = re.search("<\!--\s*QBlastInfoBegin\s*Status=(.*)", result, re.MULTILINE)
        status = m.groups()[0]
        wait_time = 60
    
    #Save the result
    output = protein_id + "_BLAST.html"  
    o = open(output, 'w') 
    o.write(result) 
    o.close()
    
    return result

def parse_id(s):
    #FIXME we only deal with uniprot ids
    cols = re.split("\|", s)
    if cols[2] == "sp":
        m = re.search("^(.*)\..", cols[3])
        if m:
            return m.groups()[0]
    return ""

def parse_ids(s):
    ids = []
    for id_s in re.split(";", s):
        i = parse_id(id_s)
        if i != "":
            ids.append(i)
    return ids

def parse_blast_result(s):
    lines = re.split("\n", s)
    blast_hits = []
    for line in lines:
        if len(line) < 1:
            #this line is empty
            continue
        if line[0] == '#':
            #this line is a comment
            continue
        cols = re.split("\t", line)
        h = {'query' : parse_id(cols[0]),
             'subjects' : parse_ids(cols[1]),
             'evalue' : float(cols[11]),
             'bit-score' : float(cols[12])}
        blast_hits.append(h)
    return blast_hits
        
def blast(protein_id):
    #first try to find a cached result
    if (os.path.exists(os.path.join('cache', protein_id + '_BLAST.pkl'))):
        f = open(os.path.join('cache', protein_id + '_BLAST.pkl'), 'rb')
        p = pickle.load(f)
        f.close()
        return p
    result = query_server(protein_id)
    #Find the result between the PRE tags
    m = re.search("^<PRE>(.*)^</PRE>", result, re.MULTILINE + re.DOTALL)
    r = parse_blast_result(m.groups()[0])
    r.sort(key=lambda hit: hit['evalue'])
    #write to file system cache
    f = open(os.path.join('cache', protein_id + '_BLAST.pkl'), 'wb')
    pickle.dump(r, f)
    f.close()
    return r

if __name__ == "__main__":
    f = open('proteins.txt', 'r') 
    for line in f:
        protein_id = line.strip("\n")
        print [r['subjects'] for r in blast(protein_id)]
