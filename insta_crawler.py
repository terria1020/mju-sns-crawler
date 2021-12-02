import time
import os
import tkinter
from bs4 import BeautifulSoup
import requests
from utils.browser import Browser
from docopt import docopt
from tqdm import tqdm
import html
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


# python crawl.py -n 3

# https://hyebit.tistory.com/49
 # 파일 경로와 데이터를 매개변수로 받아서 파일 작성.

def writeToFile(filePath, data):
    # 텍스트 모드로 쓰기
    file = open(filePath, 'w', encoding='utf8')
    for i in data:
        if type(i) is list: # i가 리스트이면 즉 data가 [[], []] 이차원 리스트
            i = "\n".join(i) # 원소 구분자를 '\n'으로. 줄 구분. 문자열
        try:
            file.write(str(i)+"\n") # i를 문자열로 변환 후 작성.
        except Exception as e:
            pass
    file.close()

 # 디렉토리 만들기.
def makeDir(dirPath):
    # 매개변수로 받은 경로가 존재하지 않을 때
    if not os.path.exists(dirPath):
        os.makedirs(dirPath) # 그 경로 생성
    else: # 존재 한다면 
        # dirPath에 있는 모든 파일 리스트의 수가 3개면
        if len(os.listdir(dirPath)) == 3: 
            return False # False 반환
    return True # 3개가 아니면 True 반환

# 날짜, 시간 추출
def extractDateTime(data):
    result = ""
    try: # data가 datetime="2021.11.13" 라고 하면 result는 2021.11.13.
        result = data.split('datetime="')[1].split('"')[0]
    except Exception as e:
        pass
        result = ""
    return result

# 본문 추출
def extractMainText(data):
    soup = BeautifulSoup(data)
    try:
        result = soup.select('div.C4VMK > span')[0].text
    except:
        result = ""
    return result

# 좋아요 수 추출
def extractLikes(data):
    soup = BeautifulSoup(data)
    try: # https://www.jungyin.com/168
        result = soup.select('div.Nm9Fw > a.zV_Nj > span')[0].text
    except:
        result = 0
    return result

# 포스트 링크 주소 추출
def extractUrl(data):
    soup = BeautifulSoup(data)
 
    result = soup.select("div.v1Nh3 a")[0]['href']
    return result

 # 이미지 링크 추출
def extractImgUrl(data):
    soup = BeautifulSoup(data)
    result = soup.select("div.KL4Bh img")[0]['srcset'].split(" ")[0]
    return result

# 이미지 저장. 이미지 url, 저장할 경로 매개변수로 받음.
def downloadImage(imageUrl, imagePath):
    # get은 http 요청. requests.get(url) 형식
    # 이미지의 url의 bytes(바이너리) 타입 데이터
    img_data = requests.get(imageUrl).content
    # imagePath경로에 바이너리 모드로 쓰기
    with open(imagePath, 'wb') as handler:
        handler.write(img_data)



def runCrawl(browser, queryList, limitNum):
    #browser = Browser("driver/chromedriver")
    
    # ==========================================================================
    # =============================================================================
    # tklnter GUI

    #tkinterSep.GUIstart(browser)
    

    # ====================================================================
    # ====================================================================



    # GUIstart가 계정 목록 리턴하게 만듬.
    #queryList = list(tkinterSep.GUIstart(browser)) # 계정 목록들 GUI에서 가져옴

    for query in queryList:
        browser.clearLink() # urlList 초기화
        makeDir("data") # data 디렉토리 생성
        makeDir("data/"+query) # data 내부에 query 생성
        
        mUrl = ""
        # query에 python / #python 들어옴.
        if query[0] == "#": # 해시태그 검색일 경우             python
            mUrl = "https://www.instagram.com/explore/tags/"+query[1:]+"/?hl=en"
        else: # 사용자 검색일 경우               pytohn
            mUrl = "https://www.instagram.com/"+query+"/?hl=en"
        
            
        browser.goToPage(mUrl) # driver.get(murl) # 주소로 이동

        print("collecting url of " + query + "...")
        browser.scrollPageToBottomUntilEnd(browser.collectDpageUrl, limitNum) # 입력 횟수만큼 페이지 전체 스크롤
        print("finish scoll collecting!")

        print("collecting data...")
        slist = list(set(browser.urlList)) # 각 포스트 url 리스트 저장




        for url in tqdm(slist): # 프로세스 바
            dirName = url.split("/")[4]
            # skip if already crawled 
            if not makeDir("data/"+query+"/"+dirName):
                continue

            browser.goToPage(url) # 포스트 하나마다 url 이동

            time.sleep(1)

            cur = browser.getPageSource() # return self.driver.page_source # 한 포스트 전체 html
           
            time.sleep(1)
            
            # extract data
            
            dateTime = extractDateTime(cur) # 날짜 추출
            mainText = extractMainText(cur) # 본문 글 추출
            likes = extractLikes(cur) # 좋아요 수 추출
            url = extractUrl(cur) # 링크 추출
            imgUrl = extractImgUrl(cur) # 이미지 링크 추출

            writeToFile(
                "data/"+query+"/"+dirName+"/info.txt", 
                [   
                    "dateTime: ", dateTime, "",
                    "mainText: ", mainText, "",
                    "likes: ", likes, "",
                    "url: ", "https://www.instagram.com" + url, ""
                ]
            )

            # download image
            imageUrl = html.unescape(imgUrl)
            downloadImage(imageUrl,"data/"+query+"/"+dirName+"/image.jpg")
            time.sleep(1)


        print("query " + query + " collecting finish")

    time.sleep(2)
    #browser.driver.quit()
    print("FINISH!")

def main(browser, queryList, limitNum):
    args = docopt("""
    Usage:
        insta_crawler.py [-n NUMBER] [--a] [-h HELP]
    
    Options:
        -n NUM    number of returned posts [default: 1000]
    """)
    hasChromeDriver = False
    for i in os.listdir("./driver"):
        if "chromedriver" in i:
            hasChromeDriver = True
            break
    if not hasChromeDriver:
        print("ERROR! NO 'chromedriver' Found")
        print("Please install chromedriver at https://sites.google.com/a/chromium.org/chromedriver/")
        return

    runCrawl(browser, queryList, limitNum)

#main()