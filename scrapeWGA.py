from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup

url = "https://www.wga.hu/cgi-bin/artist.cgi?Profession=painter&School=any&Period=any&Time-line=any&from=0&max=9999999999&Sort=Name"
header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = BeautifulSoup(urlopen(Request(url,headers=header)),'html.parser')
linkList = []
for r in soup.find_all("tr"):
    ls = r.find_all('td', attrs={"class": "ARTISTLIST"})
    if len(ls) > 0:
        artistName = str(ls[0].find_all('b')[0].next).replace(',','')
        years = str(ls[1].next.replace('c,', 'c.').replace(',',''))
        style = str(ls[2].next)
        tp = str(ls[3].next)
        if "painter" in tp.lower():
            print("(see" not in str(ls[0]))
            if "(see" not in str(ls[0]):
                link = ls[0].find_all('a')[0]['href']
                linkList.append((link, artistName, years, style, tp))

ptgs = open('paintings.csv','a', encoding='utf-8')

count_init = 1457
count = count_init
miss = open('missing.csv','a')
for lnk in linkList[count_init:-1]:
    print(count)
    curLink = lnk[0]
    url = curLink
    soup = BeautifulSoup(urlopen(Request(url,headers=header)),'html.parser')
    ctr = 0
    first = True
    imgList = []
    for a in soup.find_all("td"):
        if first:
            first = False
        elif ctr == 0:
            elem = a.find('a')
            if not(elem is None):
                if len(a.find('a')) != 0:
                    newImg = a.find('a')['href']
            ctr = ctr + 1
        elif ctr == 1:
            info = str(a).split('<br/>')
            elem = a.find('b')
            if not(elem is None):
                if len(elem) != 0:
                    imgName = str(a.find('b').next).replace(',', ';')
            miscInfo = ''
            for inf in info[1:-2]:
                cur = inf.replace('\r', '').replace('\n', '').replace(',', '')
                miscInfo = miscInfo + cur + "|"
            ctr = ctr + 1
        elif ctr == 2:
            filInf = str(a).split('<br/>')
            fileInfo = ''
            for inf in filInf[1:-2]:
                cur = inf.replace('\r', '').replace('\n', '').replace(',', '').replace('<center>', '').replace('c,', 'c.')
                fileInfo = fileInfo + cur + "|"
            ctr = ctr + 1
        elif ctr == 3:
            imgList.append((newImg, imgName, miscInfo, fileInfo))
            ctr = 0
        else:
            ctr = ctr + 1
    if len(imgList) == 0:
        miss.write(str(lnk[0]) + '\n')
    for img in imgList:
        url = "https://www.wga.hu" + str(img[0])
        imgName = str(img[0]).split('/')[-2] + '_' + str(img[0]).split('/')[-1]
        newRow = imgName + ',' + img[1] + ',' + lnk[1] + ',' + lnk[2] + ',' + lnk[3] + ',' + lnk[4] + ',' + img[2] + ',' + img[3] + '\n'
        print(newRow)
        ptgs.write(newRow)
    count = count + 1
ptgs.close()
miss.close()