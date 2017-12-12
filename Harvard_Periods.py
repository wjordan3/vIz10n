import urllib3
import os
from urllib.request import Request, urlopen, urlretrieve
import certifi
import json

http = urllib3.PoolManager()

text_file = open("Output.txt", "w", encoding='utf-8')
# Find all of the objects with the word "cat" in the title and return only a few fields per record
for i in range(1,10001):
    print(i)
    r = http.request('GET', 'https://api.harvardartmuseums.org/person',
        fields = {
            'apikey': 'c05e0c20-cede-11e7-b7e7-65d0225fa802',
            'size': 100,
            'page': i,
            #'displayname': 'Van Gogh'
            #'title': 'cat',
            #'fields': 'objectnumber,title,dated'
        })

    #print(r.data)
    #print(str(r.data))
    #print(r.status, r.data)
    #cnt = 0
    j = json.loads(r.data.decode("utf-8"))
    for elem in j['records']:
        text_file.write(elem['displayname'] + ', ' + str(elem['personid']) + '\n')
text_file.close()