import urllib2
import re
import os.path
import pickle

def get_pdbs(protein_id):
    """Get pdbs from uniprot for uniprot protein id"""
    #Query uniprot
    #Build the URL
    baseUrl = 'http://www.uniprot.org/uniprot/'
    url = baseUrl + protein_id + '.txt' 
    # Open the URL and read the result
    fh = urllib2.urlopen(url)
    result = fh.read()
    
    #Save the result
    output = protein_id + "_uniprot.txt"  
    o = open(output, 'w') 
    o.write(result) 
    o.close()
    
    # Get the pdb from the result of the query to uniprot
    f = open(protein_id + "_uniprot.txt", 'r')
    pdbs = []
    for line in f:
        #The first two character of every give the type of information 
        #Find a line with reference (starts with DR)
        if line[0:2] != 'DR':
            continue
        else:
            #From character column 5 onwards the format is semicolon separated
            fields = line[5:].split(";")
            #The first column gives the source.
            #Find only the lines with a pdb reference (PDB)
            if fields[0].strip() != 'PDB':
                continue
            #The second column gives the actual pdb id
            pdbs.append(fields[1].strip())
    return pdbs


def get_family_uniprot(protein_id):
    """Get the SCOP family of a protein found by it's uniprot accession"""
    #first try to find a cached result
    if (os.path.exists(os.path.join('cache', protein_id + '_SCOP.pkl'))):
        f = open(os.path.join('cache', protein_id + '_SCOP.pkl'), 'rb')
        p = pickle.load(f)
        f.close()
        return p
    #Get the corresponding PDB ID for the specific UniProt ID
    pdbs = get_pdbs(protein_id)
    family = ""
    n = 0
    while (family == ""):
        if len(pdbs) < n+1:
            #print "no pdbs in scop for: " + protein_id + " (" + str(n) +\
            #    " pdbs tried)"
            return ""
        family = get_family_pdb(pdbs[n])
        n = n + 1
    #write to file system cache
    f = open(os.path.join('cache', protein_id + '_SCOP.pkl'), 'wb')
    pickle.dump(family, f)
    f.close()
    return family

def get_family_pdb(pdb):
    """Get the SCOP family of a protein found by an PDB id, cached"""
    #first try to find a cached result
    if (os.path.exists(os.path.join('cache', pdb + '_SCOP.pkl'))):
        f = open(os.path.join('cache', pdb + '_SCOP.pkl'), 'rb')
        p = pickle.load(f)
        f.close()
        return p
    #write to file system cache
    r = get_family_pdb_uc(pdb)
    f = open(os.path.join('cache', pdb + '_SCOP.pkl'), 'wb')
    pickle.dump(r, f)
    f.close()
    return r

def get_family_pdb_uc(pdb):
    """Get the SCOP family of a protein found by an PDB id, uncached"""
    #Query the scop database
    #Build the URL
    baseUrl = 'http://scop.mrc-lmb.cam.ac.uk/scop/search.cgi?lev=fa&pdb='
    url = baseUrl + pdb
    #Open the URL and read the result
    fh = urllib2.urlopen(url)
    result = fh.read()
    fh.close()
    
    #Save the result
    output = pdb + "_SCOP.html"  
    o = open(output, 'w') 
    o.write(result) 
    o.close()
    
    #The family should be in the title of the page
    m = re.search("<title>SCOP: Family: (.*)</title>", result, re.MULTILINE)
    if m:
        return m.groups()[0]
    
    #There can also be no search results for this pdb 
    m = re.search("<title>SCOP: Search Results: None</title>", result, re.MULTILINE)
    if m:
        #print "could'nt find pdb " + str(pdb) + " in SCOP"
        return ""
    
    #If we didn't return yet, we got something unexpected
    print "ERROR: unknown result from SCOP, pdb: " + pdb
    return ""

if __name__ == "__main__":
    f = open('proteins.txt', 'r') 
    for line in f:
        print get_family_uniprot(line.strip())
