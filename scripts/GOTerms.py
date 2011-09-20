import string
import re
import urllib2

class GOTerm:
    """A single GO term supported by one or more evidence"""
    def ___init___(self, go_id, name):
        self.go_id = go_id
        self.name = name
        evidence = []

    def add_evidence(self, eclass, ref):
        evidence.append (ref, eclass)

class GOTerms:
    """Holds the GO term of a protein"""
    def ___init___(self, protein_id):
        self.protein_id = protein_id
        self.terms = []

    def add_term(self, go_id, name, evidence_class, evidence_ref):
        #search for term
        for term in this.terms:
            if term.go_id == go_id:
                term.add_evidence(evidence_class, evidence_ref)
                return
        #term not found, so add it to the list
        new_term = GoTerm(go_id, name)
        new_term.add_evidence(evidence_class, evidence_ref)
        self.terms.append(new_term)

def getGOTerms(proteinid):
    baseUrl = 'http://www.ebi.ac.uk/QuickGO/GAnnotation?protein='
    url = baseUrl + proteinid + '&format=tsv'	
    fh = urllib2.urlopen(url)

    terms = GoTerms(protein_id)
    for line in fh:
        r = re.split("\t", line)
        add_term(r[6], r[7], r[9], r[8])
        aspect = r[11]


    fh.close()
    return terms

f = open('proteins.txt', 'r')
for line in f:
    getGOTerms(line.strip("\n"))
