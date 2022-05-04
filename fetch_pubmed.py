import csv
import re
import urllib
import urllib.request
from time import sleep
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

query = "<serch term>"

# common settings between esearch and efetch
base_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
db = 'db=pubmed'
json_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id='

# esearch settings
search_eutil = 'esearch.fcgi?'
search_term = '&term=' + query
search_usehistory = '&usehistory=y'
search_rettype = '&rettype=json'
search_retmax = '&retmax=200'

# call the esearch command for the query and read the web result
search_url = base_url+search_eutil+db+search_term+search_usehistory+search_rettype+search_retmax 
#print("this is the esearch command:\n" + search_url + "\n")
f = urllib.request.urlopen (search_url)
search_data = str(f.read().decode('utf-8', 'ignore'))
# print(search_url)

# extract the total abstract count
total_abstract_count = int(re.findall("<Count>(\d+?)</Count>",search_data)[0])
get_pmids = re.findall("<Id>(\d+?)</Id>",search_data)
n=20
pmid_chunks = [get_pmids[i:i + n] for i in range(0, len(get_pmids), n)]

# print(pmid_chunks)
# exit()

# efetch settings summary or abstract
fetch_eutil = 'efetch.fcgi?'
retmax = 2
retstart = 0
fetch_retmode = "&retmode=text"
fetch_rettype = "&rettype=summary"

# obtain webenv and querykey settings from the esearch results
fetch_webenv = "&WebEnv=" + re.findall ("<WebEnv>(\S+)<\/WebEnv>", search_data)[0]
fetch_querykey = "&query_key=" + re.findall("<QueryKey>(\d+?)</QueryKey>",search_data)[0]

# for testing purposes use a smaller number
# total_abstract_count = int(130)

# call efetch commands using a loop until all abstracts are obtained
run = True
all_abstracts = list()
loop_counter = 1
doi_url = "http://dx.doi.org/"

# print (get_pmids)

# print(pmid_json_url)
# exit()



# print(j_data)


def parse_jdata(jsondata,pmid):
    #print(jsondata['result'][pmid]['uid'])
    i_pmid = jsondata['result'][pmid]['uid']
    i_author = []

    for auth in jsondata['result'][pmid]['authors']:
        #print (auth['name'])
        i_author.append(auth['name'])
        # print(jsondata['result'][pmid][auth]['name'])
    # print(i_author)
    i_allauthors = str.join(", ",i_author)
    #print(jsondata['result'][pmid]['title'])
    i_title = jsondata['result'][pmid]['title']

    
    if jsondata['result'][pmid]['volume'] !="":
        #print (jsondata['result'][pmid]['volume'])
        i_volume = " volume: "+ str(jsondata['result'][pmid]['volume'])
    else:    
        i_volume = ""

    if jsondata['result'][pmid]['issue'] !="":
        #print (jsondata['result'][pmid]['issue'])
        i_issue = ", issue: "+jsondata['result'][pmid]['issue']
    else:
        i_issue = ""
        

    if jsondata['result'][pmid]['elocationid'] !="":
        # print (jsondata['result'][pmid]['elocationid'])
        i_doi = re.sub("doi: ",'',jsondata['result'][pmid]['elocationid'])
        #print(doi_url+i_doi)
    else:
        i_doi =""

    if jsondata['result'][pmid]['pubdate']:
        #print (jsondata['result'][pmid]['pubdate'])
        i_year = (jsondata['result'][pmid]['pubdate'])[:4]

    if jsondata['result'][pmid]['fulljournalname']:
        #print (jsondata['result'][pmid]['fulljournalname'])
        i_journal = jsondata['result'][pmid]['fulljournalname']
        
    print('<li class="mylistyle"><span class="pmed"><b>'+ i_title+'</b> Authors:'+i_allauthors+'<i><b>'+ i_volume + i_issue+',</b> '+i_journal+'</i> ('+i_year+') <a href="'+doi_url+i_doi+'">Pubmed Link</a></span></li>')

#Create a list for the web page
print ("<ul>")
for pmid_ch in pmid_chunks:
    pmid_str = ','.join(map(str,pmid_ch))
    pmid_json_url = json_url+pmid_str
    j = urllib.request.urlopen(pmid_json_url)
    j_data = str(j.read().decode('utf-8', 'ignore'))
    jsondata = json.loads(j_data)

    for pmid in pmid_ch:
        
        loop_counter += 1
        # if loop_counter == 4: exit ()
        parse_jdata(jsondata, pmid)
        
    # exit()
    sleep(5)

print("<ul>")