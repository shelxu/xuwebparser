import requests
from bs4 import BeautifulSoup
import re
import csv
from collections import defaultdict
import logging
logging.basicConfig(level=logging.WARNING, format='=====================>%(asctime)s %(lineno)-6d: %(message)s')

csv_file = open('../temp/USnewsRanking.csv', 'w', newline='')
writer = csv.writer(csv_file)

#read CSV for N number of people's interests by university
csv_interests = open('../temp/interests.csv.txt', 'r')
reader = csv.reader(csv_interests, delimiter=',')
line_count = 0
intDict = defaultdict(list)
intPeople = []
defaultInt = 'N'
numberPeople = 0
for row in reader:
    if line_count == 0:
        row.pop(0)
        intPeople = row
        intPeople.append('Any Interest?')
        line_count += 1
    else:
        if len(row) == 0:
            print ("Interest File Input should be CSV file with university name as the first colummn, person interests expressed as Y or N in subsequent columns" )
            exit()
        college = row.pop(0)
        intDict[college]= row 
        if 'Y' in row:
            intDict[college].append('Y')
        else:
            intDict[college].append('N')
        numberPeople = len( row )
    logging.warning(row)

    
urls = ['https://www.usnews.com/best-colleges/rankings/national-universities?_mode=table',\
         'https://www.usnews.com/best-colleges/rankings/national-universities?_page=2&_mode=table',
         'https://www.usnews.com/best-colleges/rankings/national-universities?_page=3&_mode=table',
         'https://www.usnews.com/best-colleges/rankings/national-universities?_page=4&_mode=table',
         'https://www.usnews.com/best-colleges/rankings/national-universities?_page=5&_mode=table',
         'https://www.usnews.com/best-colleges/rankings/national-universities?_page=6&_mode=table']

rankingUrls = { 'Engineering'   : 'https://www.usnews.com/best-colleges/rankings/engineering-doctorate', \
                'BioMed'        : 'https://www.usnews.com/best-colleges/rankings/engineering-doctorate-biological-biomedical', \
                'Computer'      : 'https://www.usnews.com/best-colleges/rankings/engineering-doctorate-computer', \
                'DoubleE'       : 'https://www.usnews.com/best-colleges/rankings/engineering-doctorate-electrical-electronic-communications', \
                'BusRank'       : 'https://www.usnews.com/best-colleges/rankings/business-overall', \
                'BusAcct'       : 'https://www.usnews.com/best-colleges/rankings/business-accounting', \
                'BusEnt'        : 'https://www.usnews.com/best-colleges/rankings/business-entrepreneurship',\
                'BusFin'        : 'https://www.usnews.com/best-colleges/rankings/business-finance', \
                'BusMgmt'       : 'https://www.usnews.com/best-colleges/rankings/business-management',\
                'BusMarketing'  : 'https://www.usnews.com/best-colleges/rankings/business-marketing',\
                'BusOps'        : 'https://www.usnews.com/best-colleges/rankings/business-production-operations-management',\
                'BusQuant'      : 'https://www.usnews.com/best-colleges/rankings/business-quantitative-analysis',\
                'BusRE'         : 'https://www.usnews.com/best-colleges/rankings/business-real-estate',\
                'BusSupply'     : 'https://www.usnews.com/best-colleges/rankings/business-supply-chain-management-logistics',
                'LiberalArts'   : 'https://www.usnews.com/best-colleges/rankings/national-liberal-arts-colleges'}

columns = ['University','Univ Rank', 'Locations', 'URLs', 'Top Majors', 'Sector', 'Founding', 'Religion', 'Calendar', 'Setting', 'Endorsement', 'Acceptance Rate', 'Tuition']
 
defaultRanking = 300

d = defaultdict(list)
ranks1 = []
names = []
locations = []
tuitions = []
uurls = []
umajors = []
usettings = []
uacceptances = []

#national rankings
for url in urls:
    r = requests.get(url, headers={'User-Agent':'test'})
    soup = BeautifulSoup(r.text, "lxml")
    for rank in soup.findAll('div', attrs={'class': 'ranklist-ranked-item RankList__Rank-s1dx9co1-2 jNcEpG'}):
        logging.warning(rank.text)
        if( "#" in rank.text ):
            ranks1.append(int(re.findall('\d+', rank.text)[0]))
            logging.info( ranks1 )
	
    for location in soup.findAll('p', attrs={'class': 'Paragraph-fqygwe-0 fJtpNK'}):
        locations.append(str.strip(location.text))
        logging.warning("===locations===")
        logging.info(locations)
		
    for college in soup.findAll('h3', attrs={'class': 'sc-bdVaJa kyuLHz'}):
        logging.warning("===COLLEGE===")
        logging.info(str.strip(college.text))
        names.append(str.strip(college.text))
        for uurl in college.findAll('a', href=True):
            uurl1="http://colleges.usnews.rankingsandreviews.com"+str.strip(uurl['href'])
            uurls.append(uurl1)
            logging.warning( "===University URL===" )
            logging.info(uurl1)

#parsing each university page               
            majors = []
            settings = []
            acceptances = []
            r1 = requests.get(uurl1, headers={'User-Agent':'test'})
            soup1 = BeautifulSoup(r1.text, "lxml")
            for major in soup1.findAll( 'span', attrs={'class': 'flex-medium text-muted'}):
                majors.append(str.strip(major.text))
            umajors.append(majors)
            for tuition in soup1.findAll( 'section', attrs={'class': 'hero-stats-widget-stats' }):
                tuitionstart = tuition.text.find('$') + 1
                if( tuition.text.find('Out-of-state') > 0 ):
                    tuitionstart = tuition.text[tuition.text.find( '$' ) + 1:].find('$') + tuition.text.find( '$' ) + 2
                #tuitionend = tuition.text.find('(') - 1
                t = tuition.text[tuitionstart:tuitionstart + 6]
                logging.warning( "===tuition section===")
                logging.info( t )
                tuitions.append( t )
            for setting in soup1.findAll('span', attrs={'class': 'heading-small text-black text-tight block-flush display-block-for-large-up'}):
                settings.append(str.strip(setting.text))
            usettings.append(settings)
            for acceptance in soup1.findAll('span', attrs={'data-test-id': 'r_c_accept_rate'}):
                uacceptances.append(str.strip(acceptance.text))
                break
#end parsing each university page                
logging.warning( names )
        
print( "element len", len(ranks1), len(names), len(locations), len(uurls), len(umajors), len(usettings), len(uacceptances), len( tuitions ))
#print( "colleges", names )
d['Title'] = columns + list(rankingUrls.keys())+ intPeople
for i in range(len(ranks1)):
    logging.warning( i )
    logging.info( names[i] )
    if( d[names[i]] ):
        continue
    d[names[i]].append(names[i])
    d[names[i]].append(ranks1[i])
    d[names[i]].append(locations[i])
    d[names[i]].append(uurls[i])
    d[names[i]].append(umajors[i])
    d[names[i]].append(usettings[i][0])
    d[names[i]].append(usettings[i][1])
    d[names[i]].append(usettings[i][2])
    d[names[i]].append(usettings[i][3])
    d[names[i]].append(usettings[i][4])
    d[names[i]].append(usettings[i][5])
    d[names[i]].append(uacceptances[i])
    d[names[i]].append(tuitions[i])
    d[names[i]] += [defaultRanking]*len(rankingUrls)
    d[names[i]] += [defaultInt]*numberPeople
    logging.info( d['Princeton University'] )

#School rankings
def parseRanking( rankurl ):
    er = requests.get(rankurl, headers={'User-Agent':'test'})
    souper = BeautifulSoup(er.text, "lxml")
    erankcolls = []
    erankings = []
    for erank in souper.findAll('h3', attrs={'class': 'heading-large block-tighter'}):
        coll=str.strip(erank.text)
        erankcolls.append(coll)
        
    for eranking in souper.findAll('div', attrs={'style': 'margin-left: 2.5rem;'}): 
        if( "#" in eranking.text ):
            erankings.append(int(re.findall('\d+', eranking.text)[0]))
    return( erankcolls, erankings )
#End School Rankings


j = 0
for k, rurls in rankingUrls.items():
    srankcolls, srankings = parseRanking( rurls )
    logging.warning( "===School Rankings 1===" )
    logging.info( srankcolls )
    logging.info( srankings )
    for i in range(len(srankings)):
        if( d[srankcolls[i]]):
            logging.warning( "===School Rankings===" )
            values = d[srankcolls[i]]
            logging.warning( values )
            values[len(columns) + j] = srankings[i]
            logging.warning( values )
            d[srankcolls[i]] = values
    j+=1

for collname, interests in intDict.items():
    if( d[collname]):
        values = d[collname]
        values = values[:-1*numberPeople] + interests
        d[collname] = values

logging.info(d)
for k,v in d.items():
    writer.writerow(v)
