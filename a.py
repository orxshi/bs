from bs4 import BeautifulSoup
import urllib.request
import time
import math
import sys
from post import *
import os.path



#binegedi: 1
#nerimanov: 3
#nesimi: 4

rayons = [1, 3, 4]
nrooms = [1, 2, 3, 4]
minfloor = 3
maxfloor = 8
sleep = 4
totalnroom = 4
post_per_page = 25


def lis(table):
    rows = table.findAll('tr')
    cols = rows[1].findAll('td')
    for col in cols:
        aa = col.find('a', href=True)
        if aa is not None:
            return aa['href']

def read_from_existing(outfilename, nroom, post):
    ff = open(outfilename,"r")
    aa = ff.read().split('--------------------------------')
    for p in aa:
        if p != "\n":
            append_post(p.strip(), nroom, post[nroom-1])

def number_of_pages(url):
    source_root = urllib.request.urlopen(url).read()
    soup_root = BeautifulSoup(source_root,'html.parser',from_encoding="iso-8859-1")

    ee = soup_root.find('div', class_='count').find('b')
    npage = math.ceil([int(s) for s in ee.string.split() if s.isdigit()][0])
    return npage


for rayon in rayons:

    if rayon == 1:
        srayon = 'binegedi'
    elif rayon == 3:
        srayon = 'nerimanov'
    elif rayon == 4:
        srayon = 'nesimi'

    post = totalnroom * [[]]

    print("rayon: " + srayon)

    for nroom in nrooms:

        print("room: " + str(nroom))

        outfilename = srayon + '_otag' + str(nroom) + '.txt'

        if os.path.isfile(outfilename) == True:
            read_from_existing(outfilename, nroom, post)
            print('reading from existing file: ' outfilename)
            continue

        f = open(outfilename,"w+")

        url = 'https://yeniemlak.az/elan/axtar?elan_nov=1&emlak=1&menzil_nov=&qiymet=&qiymet2=&mertebe=' + str(minfloor) +'&mertebe2=' + str(maxfloor) + '&otaq=' + str(nroom) + '&otaq2=' + str(nroom) + '&sahe_m=&sahe_m2=&sahe_s=&sahe_s2=&seher=7&rayon=' + str(rayon) + '&menteqe=0&metro=0'

        npage = number_of_pages(url)

        npost = 0

        start = time.time()

        for page in range(1,npage+1):
            print("page: " + str(page))
            pageurl = url+'=&page='+str(page)
            source = urllib.request.urlopen(pageurl).read()
            soup = BeautifulSoup(source,'html.parser',from_encoding="iso-8859-1")

            tables = soup.find_all('table', {'class': 'list'})

            for t in tables:
                time.sleep(sleep)
                source2 = urllib.request.urlopen('https://yeniemlak.az'+lis(t)).read()
                soup2 = BeautifulSoup(source2,'lxml')
                for paragraph in soup2.find('div', class_='text'):
                    f.write(paragraph.string + '\n' + '--------------------------------' + '\n')
                    npost = npost + 1
                    #print(paragraph.string,'\n')
                    append_post(paragraph.string, nroom, post[nroom-1])

        f.close()

        end = time.time()


total = end - start
perpost = total / npost
print(perpost)
