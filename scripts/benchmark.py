import Pfam_Client
import SCOP_Client
import GO_Client
import BLAST_Client

class Method:
    """A method to compare the performance of two methods to one goldens
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
        return SCOP_Client.get_family_uniprot(protein_id)

    def benchmark(self, result_a, result_b):
        if result_a == "" or result_b == "":
            return 'u' 
        elif result_a == result_b:
            return 1
        else:
            return 0

class Pfam(Method):
    """Benchmark using the SCOP families"""

    def get_result(self, protein_id):
        return Pfam_Client.get_families(protein_id)

    def benchmark(self, results_a, results_b):
        result = "u"
        for result_a in results_a:
            for result_b in results_b:
                if (len(result_a['clans']) > 1) or (len(result_b['clans']) > 1):
                    print "ERROR: benchmark Pfam does not implement multiple clans"
                if (len(result_a['clans']) == 0) or (len(result_b['clans']) == 0):
                    continue
                elif result_a['clans'][0]['accession'] == result_b['clans'][0]['accession']:
                    return 1
                else:
                    result = 0
        return result

def benchmark(query_protein_id, method=Pfam(), blast_service='plain',
        max_evalue=None, n_alignments=100):
    query_result = method.get_result(query_protein_id)
    blast_results = BLAST_Client.blast(query_protein_id, service=blast_service,
            max_evalue=max_evalue, n_alignments=n_alignments)
    benchmarks = []
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
        print benchmark(line.strip("\n"))
