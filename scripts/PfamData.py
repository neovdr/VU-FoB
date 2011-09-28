
# Get data from GO files

# Import libraries
import string # Library for string operations
from xml.etree.ElementTree import parse

# Open a Pfam File
f = open("P62158_Pfam.txt", 'r')
# Parse the XML file into a hierarchical tree
tree = parse(f)
# Set an element to point to the root
elem = tree.getroot()

#Access the tree structure
for node in elem:
	# Get to the match entries
	for node in node[3]:
		# Do something with the matches!
		print node.attrib['accession']
		print node.attrib['id']		
