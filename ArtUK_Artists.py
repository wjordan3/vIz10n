from urllib.request import Request, urlopen, urlretrieve
import json
from bs4 import BeautifulSoup
import urllib
import os

cnt = 0
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')]
urllib.request.install_opener(opener)
url = 'https://artuk.org/discover/artists/search/popular:on/page/6'
header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = BeautifulSoup(urlopen(Request(url,headers=header)),'html.parser')
#print(soup)
artistList = []
for r in soup.find_all('li', {'class': "item track"}):
    # print(r.find('a')['href'])
    artistList.append(r.find('a')['href'])
    # print('next')

#print(artistList)
#print(len(artistList))

artistLinks = []

for artist in artistList:
    startPos = artist.find('artists')
    endPos = artist.find('search')
    print(artist[startPos+8:endPos])
    artistLinks.append(artist[startPos+8:endPos])


for name in artistLinks:
    url = 'https://artuk.org/discover/artworks/search/actor:' + name + 'page/20'
    print(url)
    #url ='https://artuk.org/discover/artworks/view_as/grid/search/works:sea-piece/page/2'
    #print(url)
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = BeautifulSoup(urlopen(Request(url,headers=header)),'html.parser')
    #print(soup)
    print('extracted')
    linkList = []
    for r in soup.find_all('li', {'class': "item artwork icons "}):
        #print(r.find('a')['href'])
        linkList.append(r.find('a')['href'])
        #print('next')

    ptgs = open('paintings_UK_artists.csv', 'a', encoding='utf-8')
    print(len(linkList))
    for lnk in linkList:
        #print(cnt)
        try:
            url = lnk
            soup = BeautifulSoup(urlopen(Request(url,headers=header)),'html.parser')
            title = soup.find('h1', {'class': 'artwork-title'}).next.strip().replace(',','')
            if title.find('(') != -1:
                title = title[0:title.find('(')].strip().replace(',','')
            #print(title)
            artist = str(soup.find('h2', {'class': 'artist'}).next.next.next).strip().replace(',','')
            artistYears = ''
            if artist.find('(') != -1:
                artistYears = artist[artist.find('('):len(artist)+1]
                artist = artist[0:artist.find('(')].strip()
            #print(artist)
            name = title[0:15].replace(' ', '-') + '_' + artist[0:10].replace(' ', '-') + '_UK'
            #print(name)
            #print(soup.find('div', {'class': 'artwork'}).find('img')['alt'])
            #print(title)
            alt = soup.find('div', {'class': 'artwork'}).find('img')['alt']
            if alt.find('(') != -1:
                alt = alt[0:alt.find('(')].strip()
            #print(alt)
            #print(soup.find('div', {'class': 'artwork'}).find('img')['alt'])
            details = soup.find('ul', {'class': 'details'}).contents
            #print(details)
            date = ''
            loop = 1
            elems = 0
            misc = ''
            while(loop <= 7):
                curDetail = str(details[loop])
                if elems < 3:
                    dateIndex = curDetail.find('<h5>Date</h5>')
                    if dateIndex != -1:
                        p_start = curDetail.find('<p>')
                        p_end = curDetail.find('</p>')
                        date = curDetail[p_start+3:p_end].replace(',','')
                    else:
                        p_start = curDetail.find('<p>')
                        p_end = curDetail.find('</p>')
                        misc = misc + curDetail[p_start+3:p_end].replace(',','') + '|'
                        elems = elems + 1
                loop = loop + 2
            #print(title)
            #print(alt)
            newRow = name + '.jpg,' + title + ',' + artist + ',' + artistYears + ',,,' + misc + ',,' + lnk + ',' + date + '\n'
            print(newRow)
            if alt == title:
                imgAdr = soup.find('div', {'class': 'artwork'}).find('img')['src']
                urlretrieve(imgAdr, os.path.basename(name + '.jpg'))
                ptgs.write(newRow)
            else:
                print('No image')
        except:
            print("bad image: " + lnk)
        cnt = cnt + 1

    #ptgs.close()