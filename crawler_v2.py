import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"  #  interactive
driver = webdriver.Chrome(executable_path="./chromedriver",desired_capabilities=caps)
driver.minimize_window()
url = "https://www.wikipedia.org"
visited = set() # visited hash_set


def find_all_outgoing_links(v):
    driver.get(v)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    links = soup.find_all('a')
    outgoingLinks = [a['href'] for a in links]
    return outgoingLinks



def crawl(url):
    Q = []
    titles = []
    links = []
    Q.append(url)
    visited.add(url)
    while len(Q) > 0:
        v = Q.pop(0)
        print(v)
        driver.get(v)
        titles.append(driver.title)
        links.append(v)
        print(driver.title,v,sep="   -------   ",end="\n")
        newLinks = find_all_outgoing_links(v)
        for link in newLinks:
            if link not in visited:
                Q.append(link)
                visited.add(link)
    driver.close()
    return titles,links

crawl(url)