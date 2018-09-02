import requests
from bs4 import BeautifulSoup
import re
import csv

csv_file = open('ranking_university_USnews.csv', 'w')
writer = csv.writer(csv_file)

urls = ['https://www.usnews.com/best-colleges/rankings/national-universities?_mode=table']
#,\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+2']
#,\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+3',\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+4',\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+5',\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+6',\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+7',\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+8',\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+9',\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+10',\
#        'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/data/page+11']
records = []
ranks1 = []
names = []
locations = []
uurls = []
umajors = []
usettings = []

for url in urls:
    print("shel1")
    r = requests.get(url, headers={'User-Agent':'test'})
    soup = BeautifulSoup(r.text, "lxml")
    #print(soup)
    for rank in soup.findAll('span', attrs={'class': 'text-strong'}):
        #print("shel2",rank)
        if( "#" in rank.text ):
            ranks1.append(int(re.findall('\d+', rank.text)[0]))
            #print(ranks1)
    for college in soup.findAll('div', attrs={'class': 'text-strong text-large block-tighter'}):
        print("names", college)
        names.append(str.strip(college.text))
        for uurl in college.findAll('a', href=True):
            #print("uurl", uurl)
            if( "best-colleges" in uurl['href']):
                uurl1="http://colleges.usnews.rankingsandreviews.com"+str.strip(uurl['href'])
                majors = []
                settings = []
                uurls.append(uurl1)
                print( uurl['href'] )
 #parsing each university page               
                r1 = requests.get(uurl1, headers={'User-Agent':'test'})
                soup1 = BeautifulSoup(r1.text, "lxml")
                #print("HAHAHA", soup1.encode('utf-8'))
                for major in soup1.findAll( 'span', attrs={'class': 'flex-medium text-muted'}):
                    #print("major", major.text)
                    majors.append(str.strip(major.text))
                print( "majors", majors)
                umajors.append(majors)
                for setting in soup1.findAll('span', attrs={'class': 'heading-small text-black text-tight block-flush display-block-for-large-up'}):
                    settings.append(str.strip(setting.text))
                print( "settings", settings)
                usettings.append(settings)
#end parsing each university page                
    for location in soup.findAll('div', attrs={'class': 'text-small block-tight'}):
        locations.append(str.strip(location.text))
        #print ("locations", location.text)
#    for uurl in soup.findAll('a', href=True):
#
#        if( "best-colleges" in uurl['href']):
#            uurl.append(str.strip(location.text))
#            print( uurl.text, uurl['href'] )

print( len(ranks1), len(names), len(locations), len(uurls), len(umajors), len(usettings))
ranks2 = range(203, 281)
ranks = ranks1+list(ranks2)
print(ranks)
#exit()
for i in range(len(ranks1)):
    records.append(i+1)
    records.append(ranks1[i])
    records.append(names[i].encode('utf-8'))
    records.append(locations[i])
    records.append(uurls[i])
    records.append(umajors[i])
    records.append(usettings[i][0])
    records.append(usettings[i][1])
    records.append(usettings[i][2])
    records.append(usettings[i][3])
    records.append(usettings[i][4])
    records.append(usettings[i][5])
    print(records)
    writer.writerow(records)
    records = []
