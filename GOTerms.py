
# Import libraries
import string # Library for string operations
import re # Library for regular expressions

# Open a GO file
f = open("./GO/P62158_GO.txt", 'r')

# Set the reg-ex we search for, in this case a tab character
tab = re.compile('\t')

# Create 2 lists one with tab positions, one where we store the GO data
tabpos = []
GOls = []

for line in f:
	tabtemp = []
	a = tab.finditer(line) # Search for tab positions
	GOls.append(line) # Add the GO lines to the list
	for match in a:
		tabtemp.append(match.start()) 
	tabpos.append(tabtemp) # Add the tab positions to the list

GOls[1][tabpos[1][6]:tabpos[1][7]].strip('\t') # By giving selecting the column numbers we could extract specific data we are interested in.


