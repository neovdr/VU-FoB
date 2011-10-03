import urllib2 
from xml.etree.ElementTree import parse

def get_clan_id(family_id):
	"""Get a list of clans of a Pfam family"""
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
			clan_ids.append({'accession' : clan_membership.attrib['clan_acc'],  
							 'id' : clan_membership.attrib['clan_id']})
	return clan_ids

def get_families(protein_id):
	"""Get a list of Pfam families for a protein id"""
	baseUrl = 'http://pfam.sanger.ac.uk/protein?output=xml&acc=' 
	url = baseUrl + protein_id
	fh = urllib2.urlopen(url) 
	result = fh.read()
	fh.close()
	#Save the result
	output = protein_id + "_Pfam.txt"  
	o = open(output, 'w') 
	o.write(result) 
	o.close()
	f = open(protein_id + "_Pfam.txt", 'r')
	tree = parse(f)
	f.close()
	root = tree.getroot()
	last_family_accession = '' # temporary variable to detect double family
	families = []
	for entry in root:
		for match in entry.find("{http://pfam.sanger.ac.uk/}matches"):
			if ((last_family_accession != match.attrib['accession']) # we didn't parse this before
					and (match.attrib['id'].find('DUF') == -1)): # it's not a domain of unknown function
				families.append({'accession' : match.attrib['accession'],
								 'id' : match.attrib['id'],
								 'clans' : get_clan_id(match.attrib['accession'])})
				last_family_accession = match.attrib['accession']
	return families	
				
if __name__ == "__main__":
	fb = open ('proteins.txt', 'r')
	for line in fb:
		print get_families(line.strip("\n"))
	fb.close()