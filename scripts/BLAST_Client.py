"""
A client for the BLAST service

A client for the BLAST service located at http://blast.ncbi.nlm.nih.gov/.
The blast() function is the main entry.
"""
import time
import re
import urllib2
import pickle
import os.path

def query_server(protein_id, n_alignments=50, service='plain',
        expect=100, filter_lc=True):
    """Query the BLAST server using blastp.
    
    Returns text returned from the BLAST service. Also performs caching upon
    this result. Provide either the number of alignemns as n_alignments or the
    maximum e value as evalue, not both.
    
    Arguments:
        protein_id -- uniprot protein_id to query
        n_alignments -- The number of alignments to query for. Might return more
            or less.
        max_evalue -- The results have this maximum evalue.
        service -- plain or psi
        expect -- Expected number of hits by random chance. As explained in
            http://www.ncbi.nlm.nih.gov/BLAST/blastcgihelp.shtml#expect
        filter -- filter regions of low complexity
    """
    # Caching
    cache_filename = (protein_id + "_BLAST(" +
                      str(n_alignments)
                      + ',' + service
                      + ',' + str(expect)
                      + ',' + str(filter_lc) +
                      ").html")
    if (os.path.exists(cache_filename)):
        f = open(cache_filename)
        result = f.read()
        f.close()
        return result

    # Do the query / request
	# Here by altering the SERVICE setting in the url PSI-BLAST is used
	
    url = ('http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Put' + 
          '&QUERY=' + protein_id +
          '&DATABASE=swissprot' + 
          '&PROGRAM=blastp'
          '&FILTER=' + ('T' if filter_lc else 'F') +
          '&EXPECT=' + str(expect) +
          '&FORMAT_TYPE=Text' +
          '&SERVICE=' + service)
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
    
    # Wait until result is expected to be finished and retrieve the result.
    status = ""
    wait_time = rtoe + 5 # Wait some seconds more than requested.
    while (status != "READY"): 
        print "Waiting {0:d} seconds for BLAST results".format(wait_time)
        time.sleep(wait_time)
        url = ('http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get'
               '&FORMAT_OBJECT=Alignment' + 
               '&ALIGNMENT_VIEW=Tabular' +
               '&FORMAT_TYPE=Text' +
               '&RID=' + str(rid) +
               '&ALIGNMENTS=' + str(n_alignments)
              )
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
    o = open(cache_filename, 'w') 
    o.write(result) 
    o.close()
    
    return result

def parse_id(s):
    """Parse a protein id"""
    #FIXME we only deal with uniprot ids
    cols = re.split("\|", s)
    if cols[2] == "sp": #Uniprot id
        m = re.search("^(.*)\..", cols[3])
        if m:
            return m.groups()[0]
    return ""

def parse_ids(s):
    """Parse a list of protein ids"""
    ids = []
    for id_s in re.split(";", s):
        i = parse_id(id_s)
        if i != "":
            ids.append(i)
    return ids

def parse_blast_result(s):
    """Parse a table of BLAST results.
    
        Returns a list of hashes with the keys:
            query -- The query protein id
            subjects -- A list of protein ids of hits
            evalue -- The evalue of these these hits
            bit-score -- The bit socre of these hits
    
    """
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

def blast(protein_id, n_alignments=50, max_evalue=None, service='plain'):
    """Query the BLAST server and parse the results.

    Arguments:
        protein_id -- uniprot protein_id to query
        n_alignments -- The number of alignments to query for. Might return
            more or less.
        max_evalue -- The results have this maximum evalue.
        

    Returns a list of hashes with the keys:
        query -- The query protein id
        subjects -- A list of protein ids of hits
        evalue -- The evalue of these these hits
        bit-score -- The bit socre of these hits

    """
    # Caching
    cache_filename = os.path.join('cache',
                                  protein_id + '_BLAST' +
                                  str((n_alignments,max_evalue,service)) +
                                  '.pkl')
    if (os.path.exists(cache_filename)):
        f = open(cache_filename, 'rb')
        p = pickle.load(f)
        f.close()
        return p

    # Query the server
    result = query_server(protein_id, n_alignments=n_alignments,
                          service=service)
    #Find the result between the PRE tags and parse it
    m = re.search("^<PRE>(.*)^</PRE>", result, re.MULTILINE + re.DOTALL)
    r = parse_blast_result(m.groups()[0])
    # Sort on e value
    r.sort(key=lambda hit: hit['evalue'])
    # Filter on e value
    if max_evalue:
        i = 0
        for hit in r:
            if hit['evalue'] > max_evalue:
                break
            else:
                i = i + 1
        del r[i:len(r)]

    # Write cache
    f = open(cache_filename, 'wb')
    pickle.dump(r, f)
    f.close()

    return r

if __name__ == "__main__":
    f = open('proteins.txt', 'r') 
    for line in f:
        protein_id = line.strip("\n")
        print [r for r in blast(protein_id, max_evalue=0.01, n_alignments=200)]
