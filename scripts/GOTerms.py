import string
import re
import urllib2

class GOTerm:
    """A single GO term supported by one or more evidence"""
    def __init__(self, go_id, name):
        self.go_id = go_id
        self.name = name
        self.evidence = []

    def add_evidence(self, eclass, ref):
        self.evidence.append( (ref, eclass) )

    def __str__(self):
        f = self.name
        for e in self.evidence:
            f += " " + str(e)
        return f

class GOTerms:
    """Holds the GO term of a protein"""
    def __init__(self, protein_id):
        self.protein_id = protein_id
        self.terms = []

    def add_term(self, go_id, name, evidence_class, evidence_ref):
        #search for term
        for term in self.terms:
            if term.go_id == go_id:
                term.add_evidence(evidence_class, evidence_ref)
                return
        #term not found, so add it to the list
        new_term = GOTerm(go_id, name)
        new_term.add_evidence(evidence_class, evidence_ref)
        self.terms.append(new_term)

    def __str__(self):
        f = "Protein ID: " + self.protein_id + "\n"
        f += "Terms:\n"
        for t in self.terms:
            f += "    " + str(t) + "\n"
        return f
        

def getGOTerms(protein_id):
    """Get the GO terms for and uniprot protein id"""
    baseUrl = 'http://www.ebi.ac.uk/QuickGO/GAnnotation?protein='
    url = baseUrl + protein_id + '&format=tsv'	
    fh = urllib2.urlopen(url)

    terms = GOTerms(protein_id)
    fh.next() # skip headers
    for line in fh:
        r = re.split("\t", line)
        terms.add_term(r[6], r[7], r[9], r[8])
        aspect = r[11]


    fh.close()
    return terms

f = open('proteins.txt', 'r')
for line in f:
    print getGOTerms(line.strip("\n"))
