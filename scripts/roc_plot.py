from benchmark import benchmark
import matplotlib.pyplot as plot

def tp_fp_list(benchmark):
    tp = 0
    fp = 0
    tp_list = []
    fp_list = []
    for hit in benchmark:
        if hit[1] == 1:
            tp = tp + 1
        if hit[0] == 0:
            fp = fp + 1
        tp_list.append(tp)
        fp_list.append(fp)
    return (tp_list, fp_list)
        
def roc_plot(benchmark):
    (y, x) = tp_fp_list(benchmark)
    plot.figure()
    plot.plot(x, y)
    plot.show()

if __name__ == '__main__':
    f = open('proteins.txt', 'r') 
    roc_plot(benchmark(f.readline().strip("\n")))
