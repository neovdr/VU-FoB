#Create GO Term PFAM and SCOP files for proteins in text file
import urllib2 

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
