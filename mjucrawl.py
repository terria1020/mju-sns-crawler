import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

DATA_FILE = 'mju.txt'

options = webdriver.ChromeOptions()
options.headless = True

driver = webdriver.Chrome("./driver/chromedriver",options=options)

    
def is_file_exist():
    try:
        open(DATA_FILE, 'r')
        return True
    except:
        return False

def write_to_text(list_links):
    if not is_file_exist():
        open(DATA_FILE, 'w',encoding='utf8').close()
    data = open(DATA_FILE, 'r',encoding='utf8').read()
    file = open(DATA_FILE, 'a',encoding='utf8')
    if list_links not in data:
        file.write(list_links)
        file.write("\n")
  
        # else:

def crawlMju():
    response = requests.get("http://www.mju.ac.kr/mjukr/257/subview.do")
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
   
    #link1 = soup.select_one(".artclLinkView")
    #link2 = soup.select_one("#menu257_obj700 > div._fnctWrap._articleTable > form:nth-of-type(2) > table > tbody > tr:nth-of-type(13) > td._artclTdTitle > a")
    #date1 = soup.select_one("#menu257_obj700 > div._fnctWrap._articleTable > form:nth-child(2) > table > tbody > tr:nth-child(12) > td._artclTdRdate")
    #date2 = soup.select_one("#menu257_obj700 > div._fnctWrap._articleTable > form:nth-child(2) > table > tbody > tr:nth-child(13) > td._artclTdRdate")
    #title1 = soup.select_one("#menu257_obj700 > div._fnctWrap._articleTable > form:nth-child(2) > table > tbody > tr:nth-child(12) > td._artclTdTitle > a > strong")
    #title2 = soup.select_one("#menu257_obj700 > div._fnctWrap._articleTable > form:nth-child(2) > table > tbody > tr:nth-child(13) > td._artclTdTitle > a > strong")
    
    #print()
    #print("학사 공지")
    #print()

    #for link in links:
    #    url = link.attrs['href']
    #    title = link.find('strong').text
    #    li = []
    #    for link1 in links_1:
    #        date = link1.text
    #    print(title,url, date)

    #url1 = link1.attrs['href']
    #url2 = link2.attrs['href']
    #dateof1 = date1.text
    #dateof2 = date2.text
    #titleof1 = title1.text
    #titleof2 = title2.text

    #print(titleof1,dateof1,url1)
    #print(titleof2,dateof2,url2)

 
    links = soup.find_all(class_="artclLinkView",limit=2)
    

    print()
    print("학사 공지")
    print()

    for link in links:
        url = link.attrs['href']
        title = link.find('strong').text
        str = title +"\t\t"+ url
        print(title,url)
        write_to_text(str)


    



def crawlCom():
    driver.get("http://jw4.mju.ac.kr/user/cs/index.action")
    driver.switch_to.frame("index_frame")
    driver.implicitly_wait(3)
    driver.find_element(By.XPATH,"""//*[@id="menuli5"]/a""").click()
    driver.implicitly_wait(3)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    link1 = soup.select_one("#board-container > div.list > form:nth-child(2) > table > tbody > tr:nth-child(7) > td.title > a")
    link2 = soup.select_one("#board-container > div.list > form:nth-child(2) > table > tbody > tr:nth-child(8) > td.title > a")
    date1 = soup.select_one("#board-container > div.list > form:nth-child(2) > table > tbody > tr:nth-child(7) > td:nth-child(4)")
    date2 = soup.select_one("#board-container > div.list > form:nth-child(2) > table > tbody > tr:nth-child(8) > td:nth-child(4)")

    print()
    print("학과 공지")
    print()

    #  for link in links1:
    #    url1 = link.attrs['href']
    #    title = link.text
    #    print(title.strip(),url1)

    url1 = link1.attrs['href']
    url2 = link2.attrs['href']
    title1 = link1.text
    title2 = link2.text
    dateof1 = date1.text
    dateof2 = date2.text
    print(title1.strip(),url1,dateof1.strip())
    print(title2.strip(),url2,dateof2.strip())
    str1 = title1.strip() +"\t"+ url1 +"\t"+ dateof1.strip()
    str2 = title2.strip() +"\t"+ url2 +"\t"+ dateof2.strip()
    write_to_text(str1)
    write_to_text(str2)
    driver.quit()


def crawlNews():
    response = requests.get("http://www.mju.ac.kr/mjukr/496/subview.do")
    html = response.text
    soup = BeautifulSoup(html,'html.parser')    
    link1 = soup.select_one("#relateSite3 > li:nth-child(1) > a")
    link2 = soup.select_one("#relateSite3 > li:nth-child(2) > a")
    number1 = soup.select_one("#relateSite3 > li:nth-child(1) > a > div.artclInfo > div.artclTitle > strong")
    number2 = soup.select_one("#relateSite3 > li:nth-child(2) > a > div.artclInfo > div.artclTitle > strong")

    #links1 = soup.select('.artclTitle>strong')
   
    print()    
    print("명대 신문")    
    print()

    #for link in links:
    #    url = link.attrs['href']
    #    for link1 in links1:
    #        number = link1.text
    #    print(number,url)
    url1 = link1.attrs['href']
    url2 = link2.attrs['href']
    numberof1 = number1.text
    numberof2 = number2.text
    print(numberof1,url1)
    print(numberof2,url2)
    str1 = numberof1 +"\t"+ url1
    str2 = numberof2 +"\t"+ url2
    write_to_text(str1)
    write_to_text(str2)

def main():
    a,b,c = input("1: 학사 공지  2:학과 공지   3:명대 신문").split()
    if(b == None):
        crawlMju()
    if(c == None):
        crawlMju()
        crawlCom()
    else:
        crawlMju()
        crawlCom()
        crawlNews()


if __name__ == "__main__":
    main()
    