import PfamData
import SCOP
import GOTerms
import BLAST

class Method:

    def get_result(self, protein_id):
        raise NotImplementedError()

    def benchmark(self, result_a, result_b):
        raise NotImplementedError()

class SCOP_B(Method):
    def get_result(self, protein_id):
        return SCOP.get_family_uniprot(protein_id)

    def benchmark(self, result_a, result_b):
        if result_a == "" or result_b == "":
            return 'u' 
        elif result_a == result_b:
            return 1
        else:
            return 0

def benchmark(query_protein_id, method=SCOP_B()):
    query_result = method.get_result(query_protein_id)
    blast_results = BLAST.blast(query_protein_id)
    benchmarks = []
    for blast_result in blast_results:
        for hit_protein_id in blast_result['subjects']:
            hit_result = method.get_result(hit_protein_id)
            benchmarks.append({
                'protein_id' : hit_protein_id,
                'benchmark' : method.benchmark(query_result, hit_result),
                'evalue' : blast_result['evalue']})
    return benchmarks

if __name__ == '__main__':
    f = open('proteins.txt', 'r') 
    for line in f:
        print benchmark(line.strip("\n"))
