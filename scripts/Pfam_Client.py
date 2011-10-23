import urllib2 
from xml.etree.ElementTree import parse
import os.path


def get_clan_id(family_id):
    """Get a list of clans of a Pfam family"""
    # Caching
    cache_filename = family_id + "_Pfam-clans.xml"  
    if not (os.path.exists(cache_filename)):
        # If we didn't cache the result get it from the server
        #Build the URL
        baseUrl = 'http://pfam.sbc.su.se/family?output=xml&acc='
        url = baseUrl + family_id
        #Open the URL and read the result
        fh = urllib2.urlopen(url) 
        result = fh.read()
        fh.close() 
        #Save the result
        o = open(cache_filename, 'w') 
        o.write(result) 
        o.close()
    #Parse the result from Pfam to get the clan
    f = open(cache_filename, 'r')
    tree = parse(f)
    f.close()
    root = tree.getroot()
    clan_ids = []
    #Search in the tree structure that resulted from parsing for the clan data
    for entry in root.findall("{http://pfam.sanger.ac.uk/}entry"):
        clan_membership = entry.find("{http://pfam.sanger.ac.uk/}clan_membership")
        #Provided the clan data exists, store it.
        if (clan_membership != None):
            clan_ids.append({'accession' : clan_membership.attrib['clan_acc'],  
                             'id' : clan_membership.attrib['clan_id']})
    return clan_ids

def get_families(protein_id):
    """Get a list of Pfam families for a protein id"""
    cache_filename = protein_id + "_Pfam-families.xml"  
    if not (os.path.exists(cache_filename)):
        # If we didn't cache the result get it from the server
        #Build the URL
        baseUrl = 'http://pfam.sbc.su.se/protein?output=xml&acc=' 
        url = baseUrl + protein_id
        #Open the URL and read the result
        fh = urllib2.urlopen(url) 
        result = fh.read()
        fh.close()
        #Save the result
        o = open(cache_filename, 'w') 
        o.write(result) 
        o.close()
    #Parse the result from Pfam to get the family
    f = open(cache_filename, 'r')
    tree = parse(f)
    f.close()
    root = tree.getroot()
    last_family_accession = '' # temporary variable to detect double family
    families = []
    #Search in the tree structure for family data
    for entry in root:
        matches = entry.find("{http://pfam.sanger.ac.uk/}matches")
        if matches == None:
            continue
        for match in matches:
            if ((last_family_accession != match.attrib['accession']) # we didn't parse this before
                and (match.attrib['id'].find('DUF') == -1)): # it's not a domain of unknown function
                #Store the data
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
