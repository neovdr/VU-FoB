import urllib2 
from xml.etree.ElementTree import parse

def get_clan_id(family_id):
	"""Get the clan accessions of a Pfam family"""
	#Query Pfam
	baseUrl = 'http://pfam.sanger.ac.uk/family?output=xml&acc='
	url = baseUrl + family_id
	fh = urllib2.urlopen(url) 
	result = fh.read()
	fh.close() 
	#Save the result from Pfam
	output = family_id + "_Pfam.xml"  
	o = open(output, 'w') 
	o.write(result) 
	o.close()
	#Parse the result from Pfam to get the clan
	f = open( family_id + "_Pfam.xml", 'r')
	tree = parse(f)
	f.close()
	root = tree.getroot()
	clan_ids = []
	for entry in root.findall("{http://pfam.sanger.ac.uk/}entry"):
		clan_membership = entry.find("{http://pfam.sanger.ac.uk/}clan_membership")
		if (clan_membership != None):
			print 'Clan Accesion ID: ' + clan_membership.attrib['clan_acc']
			print 'Clan ID: ' + clan_membership.attrib['clan_id']

def get_accessions(protein_id):
	f = open(line.strip('\n') + "_Pfam.txt", 'r')
	# Parse the XML file into a hierarchical tree
	tree = parse(f)
	f.close()
	# Set an element to point to the root
	root = tree.getroot()
	last_family_accession = '' # temporary variable to detect double family 
	#Access the tree structure
	for entry in root:
		# Get to the match entries
		for match in entry.find("{http://pfam.sanger.ac.uk/}matches"):
			# If it is not a domain of unknown function and we haven't already parsed the same family accession
			if ((last_family_accession != match.attrib['accession'])
					and (match.attrib['id'].find('DUF') == -1)):
				print 'Family Accesion ID: ' + match.attrib['accession']
				print 'Family ID: ' + match.attrib['id']
				last_family_accession = match.attrib['accession']
				get_clan_id(match.attrib['accession'])
				
if __name__ == "__main__":
	fb = open ('proteins.txt', 'r')
	for line in fb:
		get_accessions(line)
	fb.close()