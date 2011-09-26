#Create GO Term PFAM and SCOP files for proteins in text file
import urllib2 
import SCOP

f = open('proteins.txt', 'r') 
for line in f: 
	baseUrl = 'http://pfam.sanger.ac.uk/protein?output=xml&acc=' 
	url = baseUrl + line.strip('\n')
	fh = urllib2.urlopen(url) 
	result = fh.read() 
	fh.close()
	output = line.strip('\n') + "_Pfam.txt"  
	o = open(output, 'w') 
	o.write(result) 
	o.close() 
	
f = open('proteins.txt', 'r') 
for line in f:
        pdbs = SCOP.get_pdbs(line.strip("\n"))
        if len(pdbs) < 1:
            print "No pdb for: " + line
            continue
        pdb = pdbs[0]
	baseUrl = 'http://scop.mrc-lmb.cam.ac.uk/scop/search.cgi?lev=fa&pdb=' 
	url = baseUrl + pdb
	fh = urllib2.urlopen(url) 
	result = fh.read() 
	fh.close()	 
	output = pdb + "_SCOP.txt"  
	o = open(output, 'w') 
	o.write(result) 
	o.close() 
