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

class GeneOntology_SharedTerms(Method):
    """Benchmark using the number of shared GeneOntology terms.
        
    If the number of shared terms is higher than a certain threshold the
    proteins are seen a homologs.
    """

    def __init__(self, threshold):
        """Initialise the shared GO term threshold"""
        self.threshold = threshold

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

class CombineTakeOnes(Method):
    """Benchmark using the combination of different methods
    
    Take 1 if one of them has a 1
    Take 0 if one of them has a 0
    Take u otherwise
    """
    
    def __init__(list_of_methods)
        pass

def benchmark(query_protein_id, method=Pfam(), blast_service='plain',
              max_evalue=None, n_alignments=100):
    query_result = method.get_result(query_protein_id)
    print "DEBUG: BLASTing"
    blast_results = BLAST_Client.blast(query_protein_id, service=blast_service,
                                       max_evalue=max_evalue,
                                       n_alignments=n_alignments)
    benchmarks = []
    print "DEBUG: benchmarking"
    for blast_result in blast_results:
        for hit_protein_id in blast_result['subjects']:
            hit_result = method.get_result(hit_protein_id)
            b = method.benchmark(query_result, hit_result)
            benchmarks.append({
                'protein_id' : hit_protein_id,
                'benchmark' : b,
                'evalue' : blast_result['evalue']})
    return benchmarks

if __name__ == '__main__':
    f = open('proteins.txt', 'r') 
    for line in f:
        print benchmark(line.strip("\n"), method=GeneOntology_SharedTerms(3))
