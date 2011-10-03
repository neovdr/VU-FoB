#!/usr/bin/python

file = open("P62158_BLASTR.txt", "r")
# open the file, as a test

def parse_BLASTR(file):
	
	"""
	parse the protein_id_BLASTR.txt to get the lists of protein IDs from blast hits (top 5)
	"""
	protein_ID_result = []
	# construct the empty list
	if "gi" == line[0:2]:
	# select the line started with gi
		for hit in line.split ()[1].split(";"):
			protein_ID_result.append(hit.split("|")[3])
		return protein_ID_result
	
for line in file:
	protein_ID_result = parse_BLASTR(line)
	if protein_ID_result:
		print protein_ID_result
	
	
	
	