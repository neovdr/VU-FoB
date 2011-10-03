import urllib2
import re

def get_pdbs(protein_id):
    baseUrl = 'http://www.uniprot.org/uniprot/'
    url = baseUrl + protein_id + '.txt'	
    fh = urllib2.urlopen(url)
    pdbs = []
    for line in fh:
        if line[0:2] != 'DR':
            continue
        else:
            fields = line[5:].split(";")
            if fields[0].strip() != 'PDB':
                continue
            pdbs.append(fields[1].strip())
    return pdbs

def get_family_uniprot(protein_id):
    """Get the SCOP family of a protein found by it's uniprot accession"""
    pdbs = get_pdbs(protein_id)
    f = ""
    n = 0
    while (f == ""):
        if len(pdbs) < n+1:
            #print "no pdbs in scop for: " + protein_id + " (" + str(n) +\
            #    " pdbs tried)"
            return ""
        f = get_family_pdb(pdbs[n])
        n = n + 1
    return f

def get_family_pdb(pdb):
    """Get the SCOP family of a protein found by an PDB id"""
    baseUrl = 'http://scop.mrc-lmb.cam.ac.uk/scop/search.cgi?lev=fa&pdb='
    url = baseUrl + pdb
    fh = urllib2.urlopen(url)
    result = fh.read()
    fh.close()

    m = re.search("<title>SCOP: Family: (.*)</title>", result, re.MULTILINE)
    if m:
        return m.groups()[0]

    m = re.search("<title>SCOP: Search Results: None</title>", result, re.MULTILINE)
    if m:
        #print "could'nt find pdb " + str(pdb) + " in SCOP"
        return ""

    print "ERROR: unknown result from SCOP"

if __name__ == "__main__":
    f = open('proteins.txt', 'r') 
    for line in f:
        print get_family_uniprot(line.strip())
