import PfamData
import SCOP
import GOTerms
import BLAST

def benchmark_scop(scop_result_a, scop_result_b):
    if scop_result_a == "" or scop_result_b == "":
        return 'u' 
    elif scop_result_a == scop_result_b:
        return 1
    else:
        return 0

def benchmark(query_protein_id):
    query_scop_family = SCOP.get_family_uniprot(query_protein_id)
    benchmarks = []
    for blast_result in BLAST.blast(query_protein_id):
        for hit_protein_id in blast_result['subjects']:
            hit_scop_family = SCOP.get_family_uniprot(hit_protein_id)
            benchmarks.append((
                query_protein_id,
                benchmark_scop(query_scop_family, hit_scop_family),
                blast_result['evalue']))
    return benchmarks

if __name__ == '__main__':
    f = open('proteins.txt', 'r') 
    for line in f:
        print benchmark(line.strip("\n"))
