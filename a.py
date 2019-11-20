from bs4 import BeautifulSoup
import urllib.request
import time

start = time.time()

url = 'https://bina.az/baki/alqi-satqi/menziller'
npage = 7
sleep = 4

def lis(table):
    rows = table.findAll('tr')
    cols = rows[1].findAll('td')
    for col in cols:
        aa = col.find('a', href=True)
        if aa is not None:
            return aa['href']

f= open("output.txt","w+")

npost = 0

for src in range(1,npage+1):
    print("reading page " + str(src))
    source = urllib.request.urlopen(url+'=&page='+str(src)).read()
    soup = BeautifulSoup(source,'html.parser',from_encoding="iso-8859-1")

    tables = soup.find_all('table', {'class': 'list'})

    for t in tables:
        time.sleep(sleep)
        source2 = urllib.request.urlopen('https://yeniemlak.az'+lis(t)).read()
        soup2 = BeautifulSoup(source2,'lxml')
        for paragraph in soup2.find('div', class_='text'):
            #f.write(paragraph.string + '\n\n')
            npost = npost + 1
            print(paragraph.string,'\n')

f.close()

end = time.time()

total = end - start
perpost = total / npost

print(total)
print(perpost)
