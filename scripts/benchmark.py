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
    n = 0
    b = BLAST.blast(query_protein_id)
    print b
    print len(b)
    for blast_result in b:
        print "BLAST " + str(n)
        n = n + 1
        for hit_protein_id in blast_result['subjects']:
            hit_scop_family = SCOP.get_family_uniprot(hit_protein_id)
            benchmarks.append({
                'protein_id' : hit_protein_id,
                'benchmark' : benchmark_scop(query_scop_family, hit_scop_family),
                'evalue' : blast_result['evalue']})
    return benchmarks

if __name__ == '__main__':
    f = open('proteins.txt', 'r') 
    for line in f:
        print benchmark(line.strip("\n"))
