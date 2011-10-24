import benchmark
import matplotlib.pyplot as plot

"""Makes two list for the roc plot, false and true positives.

One counts the false positives, over the total number of results excluding
ones that have an unknown result in the golden standard. The other does the
same for the true positives.

Argument:
    benchmark : The benchmarked list of results. As returned by
        benchmark.benchmark. 

"""
def tp_fp_list(benchmark):
    tp = 0
    fp = 0
    u = 0
    tp_list = []
    fp_list = []
    for hit in benchmark:
        if hit['benchmark'] == 1:
            tp = tp + 1
        if hit['benchmark'] == "u":
            u = u + 1
        if hit['benchmark'] == 0:
            fp = fp + 1
        tp_list.append(tp)
        fp_list.append(fp)
    return (tp_list, fp_list, u)
        
def roc_plot(benchmark, title="ROC plot", filename="", random=None, numbers=True):
    print benchmark
    (y, x, u) = tp_fp_list(benchmark)
    print (y, x)
    fig = plot.figure()
    ax = fig.add_subplot(111)
    plot.title(title)
    plot.xlabel("Number of False Positives")
    plot.ylabel("Number of True Positives")
    plot.axis([-1, x[len(x)-1]+1, -1, y[len(y)-1]+1])
    plot.plot(x, y, 'b')
    if random:
        (ry, rx, ru) = tp_fp_list(random)
        ax.plot(rx, ry, 'g')
    if numbers:
        annotation = ("#TP=" + str(y[len(y)-1]) + "\n" +
                      "#FP=" + str(x[len(x)-1]) + "\n" +
                      "#U=" + str(u))
        plot.figtext(0.01, 0.99, annotation,
            fontsize=11,
            horizontalalignment = 'left',
            verticalalignment = 'top')
    if (filename != ""):
        plot.savefig(filename)
    #plot.show()

if __name__ == '__main__':
    f = open('proteins.txt', 'r')
    for line in f:
        protein_id = line.strip("\n")
        b = benchmark.benchmark(protein_id,
                      blast_service='plain',
                      method=benchmark.Pfam(),
                      n_alignments=1000,
                      max_evalue=0.01)
        roc_plot(b,
                title="ROC plot Pfam BLAST " + protein_id,
                filename="roc_plot_pfam_plain_" + protein_id)
