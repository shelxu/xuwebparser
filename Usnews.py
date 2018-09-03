import requests
from bs4 import BeautifulSoup
import re
import csv
from collections import defaultdict

csv_file = open('../temp/USnewsRanking.csv', 'w', newline='')
writer = csv.writer(csv_file)


urls = ['https://www.usnews.com/best-colleges/rankings/national-universities?_mode=table']
# ,\
        # 'https://www.usnews.com/best-colleges/rankings/national-universities?_page=2&_mode=table',
        # 'https://www.usnews.com/best-colleges/rankings/national-universities?_page=3&_mode=table',
        # 'https://www.usnews.com/best-colleges/rankings/national-universities?_page=4&_mode=table',
        # 'https://www.usnews.com/best-colleges/rankings/national-universities?_page=5&_mode=table']

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

columns = ['University','Univ Rank', 'Locations', 'URLs', 'Top Majors', 'Sector', 'Founding', 'Religion', 'Calendar', 'Setting', 'Endorsement', 'Acceptance Rate']
 
defaultRanking = 888

d = defaultdict(list)
ranks1 = []
names = []
locations = []
uurls = []
umajors = []
usettings = []
uacceptances = []

#national rankings
for url in urls:
    r = requests.get(url, headers={'User-Agent':'test'})
    soup = BeautifulSoup(r.text, "lxml")
    #print(soup)
    for rank in soup.findAll('span', attrs={'class': 'text-strong'}):
        if( "#" in rank.text ):
            ranks1.append(int(re.findall('\d+', rank.text)[0]))
    for college in soup.findAll('div', attrs={'class': 'text-strong text-large block-tighter'}):
        #print("names", college)
        names.append(str.strip(college.text))
        for uurl in college.findAll('a', href=True):
            if( "best-colleges" in uurl['href']):
                uurl1="http://colleges.usnews.rankingsandreviews.com"+str.strip(uurl['href'])
                uurls.append(uurl1)

#parsing each university page               
                majors = []
                settings = []
                acceptances = []
                r1 = requests.get(uurl1, headers={'User-Agent':'test'})
                soup1 = BeautifulSoup(r1.text, "lxml")
                for major in soup1.findAll( 'span', attrs={'class': 'flex-medium text-muted'}):
                    majors.append(str.strip(major.text))
                umajors.append(majors)
                for setting in soup1.findAll('span', attrs={'class': 'heading-small text-black text-tight block-flush display-block-for-large-up'}):
                    settings.append(str.strip(setting.text))
                usettings.append(settings)
                for acceptance in soup1.findAll('span', attrs={'data-test-id': 'r_c_accept_rate'}):
                    uacceptances.append(str.strip(acceptance.text))
                    break
#end parsing each university page                
 
    for location in soup.findAll('div', attrs={'class': 'text-small block-tight'}):
        locations.append(str.strip(location.text))
        #print ("locations", location.text)

        
        
print( "element len", len(ranks1), len(names), len(locations), len(uurls), len(umajors), len(usettings), len(uacceptances))
#print( "colleges", names )

d['Title'] = columns + list(rankingUrls.keys())
for i in range(len(ranks1)):
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
    d[names[i]] += [defaultRanking]*len(rankingUrls)

print("dict len", len(d))

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
    for i in range(len(srankings)):
        if( d[srankcolls[i]]):
            values = d[srankcolls[i]]
            values[len(columns) + j] = srankings[i]
            d[srankcolls[i]] = values
    j+=1

for k,v in d.items():
    writer.writerow(v)
