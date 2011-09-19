# Fundamentals of Bioinformatics
# Execrise 5
# Get matching sequences using NCBI BLAST

from time import sleep
import re
import urllib2 

f = open('proteins.txt', 'r') 

ls = [] 
for line in f: 
	print line
	ls.append(line) 

for i in range(len(ls)):
	baseUrl = 'http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Put&QUERY='
	url = baseUrl + ls[i].strip('\n') + '&DATABASE=swissprot&PROGRAM=blastp&FILTER=T&EXPECT=100&FORMAT_TYPE=Text'
	fh = urllib2.urlopen(url)
	query = fh.read() 
	fh.close() 
	m = re.search("^<\!--QBlastInfoBegin\s*RID = (.*)\s*RTOE = (.*)$", query, re.MULTILINE)
	rid = m.groups()[0]
	rtoe= int(m.groups()[1])
	print rtoe
	sleep(rtoe+1)
	baseurl = 'http://www.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&RID='
	url = baseurl + rid + '&FORMAT_OBJECT=Alignment&ALIGNMENT_VIEW=Tabular&FORMAT_TYPE=Text&ALIGNMENTS=5'
	fh = urllib2.urlopen(url)
	result = fh.read() 
	fh.close() 
	output = ls[i].strip('\n') + "_BLASTR.txt" 
	o = open(output, 'w') 
	o.write(result) 
	o.close() 
