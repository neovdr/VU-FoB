from benchmark import benchmark
import matplotlib.pyplot as plot

def tp_fp_list(benchmark):
    tp = 0
    fp = 0
    tp_list = []
    fp_list = []
    for hit in benchmark:
        if hit['benchmark'] == 1:
            tp = tp + 1
#        if hit['benchmark'] == "u":
#            fp = fp + 1
        if hit['benchmark'] == 0:
            fp = fp + 1
        tp_list.append(tp)
        fp_list.append(fp)
    return (tp_list, fp_list)
        
def roc_plot(benchmark):
    print benchmark
    (y, x) = tp_fp_list(benchmark)
    print y
    print x
    plot.figure()
    plot.plot(x, y)
    plot.show()

if __name__ == '__main__':
    f = open('proteins.txt', 'r')
    print "start"
    b = benchmark(f.readline().strip("\n"))
    print "plot"
    roc_plot(b)
