import PfamData
import SCOP
import GOTerms

def benchmark_scop(scop_result_a, scop_result_b):
    if scop_result_a == "" or scop_result_b == "":
        return 'u' 
    elif scop_result_a == scop_result_b:
        return 1
    else:
        return 0
    
if __name__ == '__main__':
    import BLAST
    f = open('proteins.txt', 'r') 
    for line in f:
        p_a = line.strip()
        s_a = SCOP.get_family_uniprot(p_a)
        for blast_result in BLAST.blast(p_a):
            for p_b in blast_result['subjects']:
                s_b = SCOP.get_family_uniprot(p_b)
                print(p_a + "(" + s_a + ") : " +
                      p_b + "(" + s_b + ") ::: " +
                      str(benchmark_scop(s_a, s_b)))
