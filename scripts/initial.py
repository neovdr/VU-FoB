#Create GO Term PFAM and SCOP files for proteins in text file
import urllib2 
f = open('proteins.txt', 'r') 

ls = [] 
for line in f: 
	print line
	ls.append(line) 

for i in range(len(ls)):
	baseUrl = 'http://www.ebi.ac.uk/QuickGO/GAnnotation?protein='
	url = baseUrl + ls[i].strip('\n') + '&format=tsv'
		
	fh = urllib2.urlopen(url)
	result = fh.read() 
	fh.close() 
	
	output = ls[i].strip('\n') + "_GO.txt" 
	o = open(output, 'w') 
	o.write(result) 
	o.close() 
	


import urllib2 
f = open('proteins.txt', 'r') 

ls = [] 
for line in f: 
	print line
	ls.append(line) 

for i in range(len(ls)): 
	baseUrl = 'http://pfam.sanger.ac.uk/protein?output=xml&acc=' 
	url = baseUrl + ls[i].strip('\n')
	fh = urllib2.urlopen(url) 
	result = fh.read() 
	fh.close()	 
	output = ls[i].strip('\n') + "_Pfam.txt"  
	o = open(output, 'w') 
	o.write(result) 
	o.close() 
	
import urllib2 
f = open('proteins_pdb.txt', 'r') 

ls = [] 
for line in f: 
	print line
	ls.append(line) 

for i in range(len(ls)): 
	baseUrl = 'http://scop.mrc-lmb.cam.ac.uk/scop/search.cgi?pdb=' 
	url = baseUrl + ls[i].strip('\n')
	fh = urllib2.urlopen(url) 
	result = fh.read() 
	fh.close()	 
	output = ls[i].strip('\n') + "_SCOP.txt"  
	o = open(output, 'w') 
	o.write(result) 
	o.close() 
