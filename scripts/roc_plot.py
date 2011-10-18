import benchmark
import matplotlib.pyplot as plot

def tp_fp_list(benchmark):
    tp = 0
    fp = 0
    tp_list = []
    fp_list = []
    for hit in benchmark:
        if hit['benchmark'] == 1:
            tp = tp + 1
        if hit['benchmark'] == "u":
            fp = fp + 1
        if hit['benchmark'] == 0:
            fp = fp + 1
        tp_list.append(tp)
        fp_list.append(fp)
    return (tp_list, fp_list)
        
def roc_plot(benchmark, title="ROC plot", filename=""):
    (y, x) = tp_fp_list(benchmark)
    plot.figure()
    plot.title(title)
    plot.xlabel("Number of False Positives")
    plot.ylabel("Number of True Positives")
    plot.axis([0, x[len(x)-1]+1, 0, y[len(y)-1]+1])
    plot.plot(x, y, 'k')
    if (filename != ""):
        plot.savefig(filename)
    #plot.show()

if __name__ == '__main__':
    f = open('proteins.txt', 'r')
    for line in f:
        protein_id = line.strip("\n")
        b = benchmark.benchmark(protein_id,
                      blast_service='psi',
                      method=benchmark.GeneOntology_SharedTerms(3),
                      n_alignments=200,
                      max_evalue=0.1)
        print "benchmarked"
        roc_plot(b,
                title="ROC plot GO-3 PSI-BLAST " + protein_id,
                filename="roc_plot_go-3_psi_" + protein_id)
