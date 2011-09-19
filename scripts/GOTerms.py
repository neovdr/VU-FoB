import string
import re

# Open a GO file
f = open("P62158_GO.txt", 'r')

for line in f:
    r = re.split("\t", line)
    protein_id = r[1]
    go_term = r[6]
    go_term_s = r[7]
    aspect = r[11]
    evidence = r[9]
    print aspect, go_term, evidence
