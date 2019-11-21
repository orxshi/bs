from bs4 import BeautifulSoup
import urllib.request
import time
import math
import sys
from post import *
import os.path
import argparse
from progress.bar import Bar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#bineqedi: 1
#nerimanov: 3
#nesimi: 4

def post_url_yeniemlak(table):
    rows = table.findAll('tr')
    cols = rows[1].findAll('td')
    for col in cols:
        aa = col.find('a', href=True)
        if aa is not None:
            return aa['href']

def read_from_existing(of, nroom, post):
    ff = open(of,"r")
    aa = ff.read().split('--------------------------------')
    for p in aa:
        if p != "\n":
            append_post(p.strip(), nroom, post[nroom-1])

def number_of_pages(url, post_per_page, site):

    if site == 'yeniemlak':
        source_root = urllib.request.urlopen(url).read()
        soup_root = BeautifulSoup(source_root,'html.parser',from_encoding="iso-8859-1")
        ee = soup_root.find('div', class_='count').find('b')
        npost = [int(s) for s in ee.string.split() if s.isdigit()][0]
        return npost, math.ceil((npost / post_per_page))
    elif site == 'bina':
        pagesource = page_source(url)
        soup_root = BeautifulSoup(pagesource, 'html.parser')
        ee = soup_root.find_all('span', class_='page')
        return -1, int(ee[-1].find('a').string)


def page_url(site, url, page):
    if site == 'yeniemlak':
        return url+'=&page='+str(page)
    elif site == 'bina':
        return url+'&page='+str(page)
    

def get_preurl(site):
    if site == 'yeniemlak':
        return 'https://yeniemlak.az' 
    elif site == 'bina':
        return 'https://bina.az'


def page_source(url):

    CHROME_PATH = '/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 0)
    page_source = driver.page_source
    driver.close()
    return page_source


def read_post_yeniemlak(npage, url, sleep, preurl, f, nroom, post, rayon, npost, site):

    bar = Bar(rayon+'-otag-'+str(nroom), max=npost, suffix='%(index)d/%(max)d eta: %(eta)d elapsed: %(elapsed)d')

    for page in range(1,npage+1):

        pageurl = page_url(site, url, page)
        source = urllib.request.urlopen(pageurl).read()
        soup = BeautifulSoup(source,'html.parser',from_encoding="iso-8859-1")

        tables = soup.find_all('table', {'class': 'list'})

        for it, t in enumerate(tables):
            time.sleep(sleep)
            source2 = urllib.request.urlopen(preurl+post_url_yeniemlak(t)).read()
            soup2 = BeautifulSoup(source2,'lxml')
            for paragraph in soup2.find('div', class_='text'):
                #print("post: " + str(it))
                f.write(paragraph.string + '\n' + '--------------------------------' + '\n')
                #print(paragraph.string,'\n')
                append_post(paragraph.string, nroom, post[nroom-1])
                bar.next()
    bar.finish()


def read_post_bina(npage, url, sleep, preurl, f, nroom, post, rayon, post_per_page, site):
    
    # bina does not provide total number of posts.
    # so we assume that npost = npage * post_per_page.
    # therefore the bar might end up earlier.
    bar = Bar(rayon+'-otag-'+str(nroom), max=npage * post_per_page, suffix='%(index)d/%(max)d eta: %(eta)d elapsed: %(elapsed)d')

    for page in range(1,npage+1):

        pageurl = page_url(site, url, page)

        soup = BeautifulSoup(page_source(pageurl), 'html.parser')

        div = soup.find_all('div', {'class': 'items_list'})

        for dd in div:
            if len(dd.get('class', '')) == 1:
                div2 = dd.find_all('div', {'class': 'items-i'})
                for e in div2:
                    aa = e.find('a', href=True)

                    soup2 = BeautifulSoup(page_source(preurl + aa['href']),'html.parser')
                    bb = soup2.find("meta", property="og:description")
                    f.write(bb['content'] + '\n' + '--------------------------------' + '\n')
                    bar.next()
    bar.finish()


def midurl(site, minfloor, maxfloor, nroom, rayon_num, rayon, yenitikili):
    if site == 'yeniemlak':
        if yenitikili == 1:
            return '/elan/axtar?elan_nov=1&emlak=1&menzil_nov=' + str(1) + '&qiymet=&qiymet2=&mertebe=' + str(minfloor) +'&mertebe2=' + str(maxfloor) + '&otaq=' + str(nroom) + '&otaq2=' + str(nroom) + '&sahe_m=&sahe_m2=&sahe_s=&sahe_s2=&seher=7&rayon=' + str(rayon_num) + '&menteqe=0&metro=0'
        else:
            return '/elan/axtar?elan_nov=1&emlak=1&menzil_nov=' + str(2) + '&qiymet=&qiymet2=&mertebe=' + str(minfloor) +'&mertebe2=' + str(maxfloor) + '&otaq=' + str(nroom) + '&otaq2=' + str(nroom) + '&sahe_m=&sahe_m2=&sahe_s=&sahe_s2=&seher=7&rayon=' + str(rayon_num) + '&menteqe=0&metro=0'

    elif site == 'bina':
        if yenitikili == 1:
            return '/baki/' + rayon + '/alqi-satqi/menziller/yenitikili/' + str(nroom) + '-otaqli?floor_from=' + str(minfloor) + '&floor_to=' + str(maxfloor)
        else:
            return '/baki/' + rayon + '/alqi-satqi/menziller/kohnetikili/' + str(nroom) + '-otaqli?floor_from=' + str(minfloor) + '&floor_to=' + str(maxfloor)


def rayon_num_yeniemlak(rayon):
    if rayon == 'bineqedi':
        return 1
    elif rayon == 'nerimanov':
        return 3
    elif rayon == 'nesimi':
        return 4

def outfilename(site, rayon, nroom, yenitikili):
    if yenitikili == 1:
        return site + '_' + rayon + '_otag' + str(nroom) + '_yenitikili' + '.txt'
    else:
        return site + '_' + rayon + '_otag' + str(nroom) + '_kohnetikili' + '.txt'


def main():

    CLI = argparse.ArgumentParser()
    CLI.add_argument(
      "--rayon",
      nargs="*",
      type=str,
      default=['bineqedi', 'nerimanov', 'nesimi'],
    )
    CLI.add_argument(
      "--nroom",
      nargs="*",
      type=int,
      default=[1, 2, 3, 4],
    )
    CLI.add_argument(
      "--site",
      type=str,
      default='yeniemlak',
    )
    CLI.add_argument(
      "--yenitikili",
      type=int,
      default=1,
    )

    args = CLI.parse_args()

    site = args.site
    rayons = args.rayon
    nrooms = args.nroom
    yenitikili = args.yenitikili
    minfloor = 3
    maxfloor = 8
    sleep = 5
    if site == 'yeniemlak':
        post_per_page = 25
    elif site == 'bina':
        post_per_page = 24

    for rayon in rayons:

        rayon_num = rayon_num_yeniemlak(rayon)
        print("rayon: " + rayon)

        post = [[] for i in range(len(nrooms))]

        for nroom in nrooms:

            print("room: " + str(nroom))

            of = outfilename(site, rayon, nroom, yenitikili)

            if os.path.isfile(of) == True:
                read_from_existing(of, nroom, post)
                print('reading from existing file: ' + of)
                continue

            f = open(of,"w+")

            preurl = get_preurl(site)
            url = preurl + midurl(site, minfloor, maxfloor, nroom, rayon_num, rayon, yenitikili)

            [npost, npage] = number_of_pages(url, post_per_page, site)

            if site == 'yeniemlak':
                read_post_yeniemlak(npage, url, sleep, preurl, f, nroom, post, rayon, npost, site)
            elif site == 'bina':
                read_post_bina(npage, url, sleep, preurl, f, nroom, post, rayon, post_per_page, site)

            f.close()


    #categorize(post[0])


if __name__== "__main__":
    main()
