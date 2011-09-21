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

pdb = get_pdbs('P08046')[0]


