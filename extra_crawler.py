import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

DATA_FILE = 'mju.txt'

options = webdriver.ChromeOptions()
options.headless = True
    
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

def crawlMju():
    response = requests.get("http://www.mju.ac.kr/mjukr/257/subview.do")
    html = response.text
    soup = BeautifulSoup(html,'html.parser')

    links = soup.find_all(class_="artclLinkView",limit=2)
    
    print()
    print("학사 공지")
    print()

    for link in links:
        url = link.attrs['href']
        title = link.find('strong').text
        str = title +"\t\t"+ "https://mju.ac.kr" + url
        print(title,url)
        write_to_text(str)

def crawlCom(driver):
    driver.goToPage("http://jw4.mju.ac.kr/user/cs/index.action")
    driver.switch("index_frame")
    #driver.implicitly_wait(3)
    time.sleep(3.0)
    driver.driver.find_element_by_xpath("""//*[@id="menuli5"]/a""").click()
    #driver.implicitly_wait(3)
    time.sleep(3.0)
    req = driver.getPageSource()
    soup = BeautifulSoup(req, 'html.parser')
    link1 = soup.select_one("#board-container > div.list > form:nth-child(2) > table > tbody > tr:nth-child(7) > td.title > a")
    link2 = soup.select_one("#board-container > div.list > form:nth-child(2) > table > tbody > tr:nth-child(8) > td.title > a")
    date1 = soup.select_one("#board-container > div.list > form:nth-child(2) > table > tbody > tr:nth-child(7) > td:nth-child(4)")
    date2 = soup.select_one("#board-container > div.list > form:nth-child(2) > table > tbody > tr:nth-child(8) > td:nth-child(4)")

    print()
    print("학과 공지")
    print()

    url1 = link1.attrs['href']
    url2 = link2.attrs['href']
    title1 = link1.text
    title2 = link2.text
    dateof1 = date1.text
    dateof2 = date2.text
    print(title1.strip(),url1,dateof1.strip())
    print(title2.strip(),url2,dateof2.strip())
    str1 = title1.strip() +"\t"+ "https://jw4.mju.ac.kr/user/" + url1 +"\t"+ dateof1.strip()
    str2 = title2.strip() +"\t"+ "https://jw4.mju.ac.kr/user/" + url2 +"\t"+ dateof2.strip()
    write_to_text(str1)
    write_to_text(str2)


def crawlNews():
    response = requests.get("http://www.mju.ac.kr/mjukr/496/subview.do")
    html = response.text
    soup = BeautifulSoup(html,'html.parser')    
    link1 = soup.select_one("#relateSite3 > li:nth-child(1) > a")
    link2 = soup.select_one("#relateSite3 > li:nth-child(2) > a")
    number1 = soup.select_one("#relateSite3 > li:nth-child(1) > a > div.artclInfo > div.artclTitle > strong")
    number2 = soup.select_one("#relateSite3 > li:nth-child(2) > a > div.artclInfo > div.artclTitle > strong")

    print()    
    print("명대 신문")    
    print()

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

def main(driver, tuple):
    print("1: 학사 공지  2:학과 공지   3:명대 신문")
    if (0 in tuple):
        crawlMju()
    if (1 in tuple):
        crawlCom(driver)
    if (2 in tuple):
        crawlNews()