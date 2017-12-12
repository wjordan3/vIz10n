import urllib3
import os
from urllib.request import Request, urlopen, urlretrieve
import certifi
import json

artistList = []
cnt = 0
with open('HarvardCodes.txt') as f:
    artistList = f.readlines()

artistList = [x.strip() for x in artistList]
print(artistList)
http = urllib3.PoolManager()

# Find all of the objects with the word "cat" in the title and return only a few fields per record
for elem in artistList:
    r = http.request('GET', 'https://api.harvardartmuseums.org/object',
        fields = {
            'apikey': 'c05e0c20-cede-11e7-b7e7-65d0225fa802',
            'classification': 'Paintings',
            #'periodid': 6322,
            'size': 100,
            'page': 1,
            'person' : int(elem)
            #'yearmade': 1989,
            #'culture': 37527759
            #'color': '#ffffff'
            #'title': 'cat',
            #'period': 'Modern'
            #'fields': 'objectnumber,title,dated'
        })


    #print(str(r.data))
    #print(r.status, r.data)
    j = json.loads(r.data.decode("utf-8"))
    #print(j['records'])
    #print(j['records'][1])
    for elem in j['records']:
        #print(elem['colors'])
        try:
            #print(elem['images'][0]['iiifbaseuri'])
            title = elem['title']
            #print(title)
            period = ''
            #period = ' ' + elem['period']
            artist = 'Unknown Artist'
            if 'people' in elem:
                artist = elem['people'][0]['name']

            #department = elem['department']
            #print(department)
            #artist = elem[]
            #print(elem)
            baseuri = elem['images'][0]['iiifbaseuri']
            colors = elem['colors']
            colorList = []
            for c in colors:
                colorList.append(c['hue'].lower())
            #print(colorList)
            not_bw = False
            for c in colorList:
                #print(c)
                if c.find('white') == -1 and c.find('grey') == -1 and c.find('black') == -1:
                    #print('NOT GREYSCALE')
                    not_bw = True
            if not_bw:
                urlretrieve(baseuri + '/full/full/0/native.jpg',
                            os.path.basename("HVR_" + artist[0:6] + "_" + title[0:6] + ".jpg"))
                print(title + ' by ' + artist + period)
                cnt = cnt + 1
                print(cnt)
            #artist = elem['people'][0]['name']
            #title = elem['title']

            #cnt = cnt + 1
        except:
            err = 0
#for elem in j['records']:
    #print(elem)
#print(len(j['records']))
#urlretrieve('https://ids.lib.harvard.edu/ids/iiif/43534218/full/full/0/native.jpg', os.path.basename("test.jpg"))