
# Get data from GO files

# Import libraries
import urllib2 
from xml.etree.ElementTree import parse
sectmp= 'DUF'
# Open a Pfam File
fb = open ('proteins.txt', 'r')
for line in fb:
	f = open(line.strip('\n') + "_Pfam.txt", 'r')
	# Parse the XML file into a hierarchical tree
	tree = parse(f)
	f.close()
	# Set an element to point to the root
	elem = tree.getroot()
	tmp = '*'
	#Access the tree structure
	for node in elem:
		# Get to the match entries
		for node in node[3]:
			# If it is not a domain of unknown function and we haven't already parsed the same family accession
			
			if (tmp != node.attrib['accession']) and (node.attrib['id'].find(sectmp) == -1):
				# Do something with the matches!
				print 'Family Accesion ID: ' + node.attrib['accession']
				print 'Family ID: ' +node.attrib['id']
				#Access Pfam again with the accession ID to find the clan of the family
				tmp = node.attrib['accession']
				baseUrl = 'http://pfam.sanger.ac.uk/family?output=xml&acc='
				url = baseUrl + node.attrib['accession']
				fh = urllib2.urlopen(url) 
				result = fh.read() 
				#Save the output
				output = node.attrib['accession'] + "_Pfam.txt"  
				o = open(output, 'w') 
				o.write(result) 
				o.close() 
				#Parse the XML file to get the clan
				f= open( node.attrib['accession'] + "_Pfam.txt",'r')
				sectree = parse(f)
				f.close()
				secelem = sectree.getroot()
				#Get to the Clan entry
				for node in secelem:
					# Do something with the clan!
					for e in node:
						if (e.text != None):
							# Ignore comments etc.
							continue
						print 'Clan Accesion ID: ' + e.attrib['clan_acc']
						print 'Clan ID: ' + e.attrib['clan_id']
						break
				fh.close()
fb.close()