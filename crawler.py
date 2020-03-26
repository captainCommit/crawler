import os
import time
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException,InvalidArgumentException

def canonical_url(u):
    u = u.lower()
    if u.startswith("http://"):
        u = u[7:]
    if u.startswith("www."):
        u = u[4:]
    if u.endswith("/"):
        u = u[:-1]
    return u

def getDomain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return canonical_url(domain)

def same_doms(u1, u2):
    return getDomain(u1) == getDomain(u2)

def find_all_outgoing_links(driver,url):
    driver.get(url)
    allLinks = driver.find_elements_by_xpath("//a[@href]")
    links = []
    for x in allLinks:
        try:
            l =  x.get_attribute('href')
            if l == '#' or l == '' :
                continue
            links.append(x.get_attribute('href'))
        except StaleElementReferenceException:
            continue
        except InvalidArgumentException:
            continue
    return links

def initDriver():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  #  interactive
    driver = webdriver.Chrome(executable_path="./chromedriver",desired_capabilities=caps)
    driver.minimize_window()
    return driver

def crawl(driver,url,f):
    count = 0
    Q = []
    Q.append(url)
    visited.add(url)
    while len(Q) > 0:
        v = Q.pop(0)
        dm = getDomain(v)
        print("{dm1} {dm2}".format(dm1 = dom_main,dm2=dm))
        title = ""
        if same_doms(v,url):
            driver.get(v)
            title = driver.title
            print('{title} ========= {link}'.format(title = driver.title,link = v))
            f.write('{title} ========= {link}\n'.format(title = driver.title,link = v))
        else:
            title = "External Page Ignored"
            print('{title} ========= {link}'.format(title = title,link = v))
            f.write('{title} ========= {link}\n'.format(title = title,link = v))
            continue
        newLinks = find_all_outgoing_links(driver,v)
        if len(newLinks) == 0:
            continue
        for link in newLinks:
            if link not in visited:
                count = count+1
                Q.append(link)
                visited.add(link)
    driver.close()
    return count

url = input("Enter Site TO Be Crawled : ")
visited = set() # visited hash_set
#keyword = input("Enter Search Keyword : ")
dom_main = getDomain(url)
driver = initDriver()
f = open(dom_main+".txt",'w')
start = time.time()
count = crawl(driver,url,f)
end = time.time()
f.write('Time Taken : '+str(end-start)+"\n")
f.write("{page} pages traversed.".format(page = count))
f.close()
print("{page} pages traversed.".format(page = count))
print("Done in {time} seconds".format(time = end-start))

