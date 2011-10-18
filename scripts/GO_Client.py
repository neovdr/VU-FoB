import re
import urllib2
from copy import copy

# The codes in different evidence classses
EC_EXPERIMENTAL = ["EXP", "IDA", "IPI", "IMP", "IGI", "IEP"]
EC_COMPUTATIONAL = ["ISS", "ISO", "ISA", "ISM", "IGC", "IBA", "IBD",
                    "IKR", "IRD", "RCA"]
EC_AUTHOR = ["TAS", "NAS"]
EC_CURATOR = ["IC", "ND"]
EC_AUTOMATIC = ["IEA"]
EC_OBSOLETE = ["NR"]

class GOTerm:
    """A single GO term supported by one or more evidence"""

    def __init__(self, go_id, name):
        self.go_id = go_id
        self.name = name
        self.evidence = []

    def add_evidence(self, evidence_code, ref):
        """Add evidence for this GO Terms"""
        self.evidence.append( (ref, evidence_code) )

    def has_evidence(self, evidence_code):
        """Check whether this term has evidence with a certain code"""
        for (ref, ec) in self.evidence:
            if (ec == evidence_code):
                return True
        return False

    def has_evidence_class(self, evidence_class):
        """Check whether this term has evidence with a certain class"""
        for (ref, ec) in self.evidence:
            if (ec in evidence_class):
                return True
        return False

    def __str__(self):
        f = self.name
        for e in self.evidence:
            f += " " + str(e)
        return f

class GOTerms:
    """Holds the GO term of a protein"""

    def __init__(self, protein_id):
                #Initialize the class with a specific protein_id
        self.protein_id = protein_id
        self.terms = []

    def add_term(self, go_id, name, evidence_class, evidence_ref):
        """Add a term with evidence to this list of GO Terms"""
        #search for term
        for term in self.terms:
            if term.go_id == go_id:
                term.add_evidence(evidence_class, evidence_ref)
                return
        #term not found, so add it to the list
        new_term = GOTerm(go_id, name)
        new_term.add_evidence(evidence_class, evidence_ref)
        self.terms.append(new_term)

    def filter_out_evidence(self, evidence_code):
        """Get all the terms without evidence with a code"""
        r = copy(self)
        r.terms = [t for t in self.terms if not(t.has_evidence(evidence_code))]
        return r

    def filter_evidence(self, evidence_code):
        """Get all the terms with evidence with a code"""
        r = copy(self)
        r.terms = [t for t in self.terms if t.has_evidence(evidence_code)]
        return r

    def filter_out_evidence_class(self, evidence_class):
        """Get all the terms without evidence with a code in a class"""
        r = copy(self)
        r.terms = [t for t in self.terms if
                   not(t.has_evidence_class(evidence_class))]
        return r

    def filter_evidence_class(self, evidence_class):
        """Get all the terms with evidence with a code"""
        r = copy(self)
        r.terms = [t for t in self.terms if
                   t.has_evidence_class(evidence_class)]
        return r


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
    result = fh.read()
    fh.close()
    
    #Save the result
    output = protein_id + '_GOTerms.txt'
    o = open(output, 'w') 
    o.write(result) 
    o.close()
    
    f = open(protein_id + "_GOTerms.txt", 'r')
    terms = GOTerms(protein_id)
    f.next() # skip headers
    for line in f:
        r = re.split("\t", line)
        terms.add_term(r[6], r[7], r[9], r[8])
        #aspect = r[11]

    fh.close()
    return terms

if __name__ == "__main__":
    f = open('proteins.txt', 'r')
    for line in f:
        print getGOTerms(line.strip("\n")).filter_evidence_class(EC_EXPERIMENTAL)
