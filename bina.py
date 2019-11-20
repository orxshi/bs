from bs4 import BeautifulSoup
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

start = time.time()

CHROME_PATH = '/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

url = 'https://bina.az/baki/nesimi/alqi-satqi/menziller/4-otaqli?floor_from=3&floor_to=8'
npage = 5
sleep = 4

f= open("output.txt","w+")

npost = 0

for src in range(1,npage+1):
    print("reading page " + str(src))
    #hdr = {'User-Agent': 'Chrome/6.0.472.63'}
    #req = urllib.request.Request(url+'?page='+str(src),headers=hdr)
    #source = urllib.request.urlopen(req).read()

    driver1 = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver1.get(url+'&page='+str(src))

    wait1 = WebDriverWait(driver1, 0)
    page_source1 = driver1.page_source

    driver1.close()

    soup = BeautifulSoup(page_source1,'html.parser')
    #soup = BeautifulSoup(source,'html.parser')

    div = soup.find_all('div', {'class': 'items_list'})

    for dd in div:
        if len(dd.get('class', '')) == 1:
            div2 = dd.find_all('div', {'class': 'items-i'})
            for e in div2:
                aa = e.find('a', href=True)

                driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
                driver.get('https://bina.az'+aa['href'])

                wait = WebDriverWait(driver, 0)
                page_source = driver.page_source

                driver.close()

                soup2 = BeautifulSoup(page_source,'html.parser')
                bb = soup2.find("meta", property="og:description")
                #print(bb['content'],'\n')
                f.write(bb['content']+'\n\n')
                npost = npost + 1

f.close()

end = time.time()

total = end - start
perpost = total / npost

print(total)
print(perpost)
