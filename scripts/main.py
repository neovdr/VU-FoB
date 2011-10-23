#!/usr/bin/env python

import getopt
import sys

import roc_plot
import benchmark

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                "n:e:g:sph",
                ["max-aligments=", "e-value", "go=", "scop", "pfam", "help"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    maxalignments = 100
    evalue = 0.1
    methods = []
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-n", "--max-alignments"):
            maxalignments = a
        elif o in ("-e", "--e-value"):
            evalue = a
        elif o in ("-g", "--go"):
            methods.append(("go", a))
        elif o in ("-s", "--scop"):
            methods.append(("scop", None))
        elif o in ("-p", "--pfam"):
            methods.append(("pfam", None))
        else:
            print "Unknown option " + o
            usage
    
    if len(args) != 1:
        print "Expected one filename"
        usage()
        sys.exit(2)
    filename = args[0]

    if len(methods) != 1:
        print "Please provide one golden standard to use"
        usage()
        sys.exit(2)
    if methods[0][0] == "go":
        method = benchmark.GeneOntology_SharedTerms(methods[0][1])
    elif methods[0][0] == "pfam":
        method = benchmark.Pfam()
    elif methods[0][0] == "scop":
        method = benchmark.SCOP()
    else:
        assert False, "We made an unkown method!"

    f = open(filename, 'r')
    for line in f:
        protein_id = line.strip("\n")
        plot_title = ("BLAST(e=" + str(evalue) + ") "
                      + protein_id +
                      " (" + method.fname() + ")")
        plot_filename = "roc_plot_" + method.name() + "_" + protein_id
        b = benchmark.benchmark(protein_id,
                      blast_service='plain',
                      method=method,
                      n_alignments=maxalignments,
                      max_evalue=evalue)
        roc_plot.roc_plot(b, title=plot_title, filename=plot_filename)
    

def usage():
    print """This is a script that draws roc plots of using BLAST for homology
search compared to a golden standard (GeneOntology, Pfam or SCOP). One filename
is expected as an argument that contains a list of uniprot protein ids to use.

Command line options:

-n --maxalignments
    The number maximum number of alignments to get from SCOP. Default is 100.

-e --e-value
    The results from blast are filtered by e-value. BLAST results with a e-value
    higher than this are thrown away. Default is 0.1.

-g --go
    Use GeneOntology as the golden standard. Two proteins are homologs if they
    share this number of terms.

-s -scop
    Use SCOP as the golden standard.

-p --pfam
    Use Pfam as the golden standard.

-h --help
    Show this help text.
"""

if __name__ == "__main__":
    main()
