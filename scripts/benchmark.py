import os.path
import random
import pickle

import Pfam_Client
import SCOP_Client
import GO_Client
import BLAST_Client

class Method:
    """A method to compare the performance of two methods to one golden
       standard."""

    def get_result(self, protein_id):
        """Get the result of the golden standard."""
        raise NotImplementedError()

    def benchmark(self, result_a, result_b):
        """Compare two results of the get_result method."""
        raise NotImplementedError()

class SCOP(Method):
    """Benchmark using the SCOP families"""

    def get_result(self, protein_id):
        """ Get the SCOP result"""
        return SCOP_Client.get_family_uniprot(protein_id)

    def benchmark(self, result_a, result_b):
        if result_a == "" or result_b == "":
                #Protein has no available structural information
            return 'u' 
        elif result_a == result_b:
                #Proteins are found to be of the same family
            return 1
        else:
                #Proteins are of a different family
            return 0

    def name(self):
        return "scop"
    
    def fname(self):
        return "SCOP"

class Pfam(Method):
    """Benchmark using the Pfam families"""

    def get_result(self, protein_id):
        """Get the Pfam result"""
        return Pfam_Client.get_families(protein_id)

    def benchmark(self, results_a, results_b):
        result = "u"
        for result_a in results_a:
            for result_b in results_b:
                if (len(result_a['clans']) > 1) or (len(result_b['clans']) > 1):
                                        # We found multiple clans for one or both proteins
                    print "ERROR: benchmark Pfam does not implement multiple clans"
                if (len(result_a['clans']) == 0) or (len(result_b['clans']) == 0):
                    continue
                                        # No clans found
                elif result_a['clans'][0]['accession'] == result_b['clans'][0]['accession']:
                    # Proteins are found to be of the same clan
                                        return 1
                else:
                                        # Proteins are of a different clan
                    result = 0
        return result

    def name(self):
        return "pfam"
    
    def fname(self):
        return "Pfam"

class GeneOntology_SharedTerms(Method):
    """Benchmark using the number of shared GeneOntology terms.
        
    If the number of shared terms is higher than a certain threshold the
    proteins are seen a homologs.
    """

    def __init__(self, threshold):
        """Initialise the shared GO term threshold"""
        self.threshold = int(threshold)

    def get_result(self, protein_id):
        """Get the GO term result"""
        return GO_Client.getGOTerms(protein_id)
    
    def benchmark(self, result_a, result_b):
        shared_count = 0 # The number of shared terms
        # There are not enough GO terms for at least one protein
        if ((len(result_a.terms) < self.threshold) or
            (len(result_b.terms) < self.threshold)
           ): return 'u'
        # If a shared term is found the counter increases
        # When the counter reaches the threshold the function returns
        for term_a in result_a.terms:
            for term_b in result_b.terms:
                if term_a.go_id == term_b.go_id:
                    shared_count = shared_count + 1
                    if shared_count >= self.threshold:
                        return 1
        # The shared GO terms are below the shared term threshold. Return
        return 0
    
    def name(self):
        return "GO(" + str(self.threshold) + ")"
    
    def fname(self):
        return "go(" + str(self.threshold) + ")"

class CombineTakeOnes(Method):
    """Benchmark using the combination of different methods
    
    Take 1 if one of them has a 1
    Take 0 if one of them has a 0
    Take u otherwise

    """
    
    def __init__(self, list_of_methods):
        self.methods = list_of_methods

    def get_result(self, protein_id):
        """Get the results from all underlying methods"""
        results = {}
        for method in self.methods:
            results[method.name] = method.get_result(protein_id)
        return results

    def benchmark(self, result_a, result_b):
        """Benchmark based on the underlying methods

        Take 1 if one of them has a 1
        Take 0 if one of them has a 0
        Take u otherwise

        """
        benchmark = 'u'
        for method in self.methods:
            b = method.benchmark(result_a[method.name], result_b[method.name])
            if b == 1:
                return 1
            if b == 0:
                benchmark = 0
        return benchmark

    def name(self):
        name = "combined("
        first = True
        for method in self.methods:
            if not first:
                name = name + ","
            name = name + method.name()
            first = False
        name += ")"
        return name

    def fname(self):
        name = "Combination ("
        first = True
        for method in self.methods:
            if not first:
                name = name + ", "
            name = name + method.fname()
            first = False
        name = name + ")"
        return name

class Blast():

    def __init__(self, max_evalue=100, max_alignments=100):
        self.max_evalue = max_evalue
        self.max_alignments = max_alignments

    def search_homologs(self, protein_id):
        return BLAST_Client.blast(protein_id,
            max_evalue=self.max_evalue,
            n_alignments=self.max_alignments)

class RandomUniprot():

    def search_homologs(self, protein_id):
        # Caching, so we don't generate different random ids all the time
        cache_filename = os.path.join('cache', 'random.pkl')
        if (os.path.exists(cache_filename)):
            f = open(cache_filename, 'rb')
            p = pickle.load(f)
            f.close()
            return p
        r = []
        for random_line in random.sample(open('pid.dat', 'r').readlines(), 1000):
            r.append({'subjects' : [random_line.strip()],
                      'evalue' : 1000})

        # Write cache
        f = open(cache_filename, 'wb')
        pickle.dump(r, f)
        f.close()

        return r

def benchmark(query_protein_id, golden_standard=Pfam(),
              search_method=Blast()):
    query_result = golden_standard.get_result(query_protein_id)
    blast_results = search_method.search_homologs(query_protein_id)
    benchmarks = []
    for blast_result in blast_results:
        for hit_protein_id in blast_result['subjects']:
            hit_result = golden_standard.get_result(hit_protein_id)
            b = golden_standard.benchmark(query_result, hit_result)
            benchmarks.append({
                'protein_id' : hit_protein_id,
                'benchmark' : b,
                'evalue' : blast_result['evalue']})
    return benchmarks

if __name__ == '__main__':
    f = open('proteins.txt', 'r') 
    for line in f:
        print benchmark(line.strip("\n"),
                        golden_standard=GeneOntology_SharedTerms(3),
                        search_method=RandomUniprot())
