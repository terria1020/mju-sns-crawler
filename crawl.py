import html
import os
import platform
import time

import requests
from docopt import docopt
from tqdm import tqdm

import yaml

from utils.browser import Browser



# python crawl.py -q #hello -n 7

# 이미지 저장. 이미지 url, 저장할 경로 매개변수로 받음.
def downloadImage(imageUrl, imagePath):
    # get은 http 요청. requests.get(url) 형식
    # 이미지의 url의 bytes(바이너리) 타입 데이터
    img_data = requests.get(imageUrl).content
    # imagePath경로에 바이너리 모드로 쓰기
    with open(imagePath, 'wb') as handler:
        handler.write(img_data)


# 파일 경로와 데이터를 매개변수로 받아서 파일 작성.
def writeToFile(filePath, data):
    # 텍스트 모드로 쓰기
    file = open(filePath, 'w', encoding='utf8')
    for i in data:
        if type(i) is list:  # i가 리스트이면 즉 data가 [[], []] 이차원 리스트
            i = "\n".join(i)  # 원소 구분자를 '\n'으로. 줄 구분. 문자열
        try:
            file.write(str(i) + "\n")  # i를 문자열로 변환 후 작성.
        except Exception as e:
            pass
    file.close()


# 디렉토리 만들기.
def makeDir(dirPath):
    # 매개변수로 받은 경로가 존재하지 않을 때
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)  # 그 경로 생성
    else:  # 존재 한다면
        # dirPath에 있는 모든 파일 리스트의 수가 3개면
        if len(os.listdir(dirPath)) == 3:
            return False  # False 반환
    return True  # 3개가 아니면 True 반환


# 언어 추출
def extractLang(data):
    result = ""
    try:  # lang=" 다음에 오는 것 예) en"이라면 result는 en
        result = data.split('lang="')[1].split('"')[0]
    except Exception as e:
        pass
    return result


# 좋아요 수 추출
def extractLikes(data, lang="en"):
    result = ""
    try:
        if lang == "en":  # 언어가 en일때
            result = data[0][1:]  # 슬라이싱. [0][1]부터 [0][끝까지]
        else:  # en 아니면
            result = data[1][:-2]  # [1][0]부터 [1][뒤에서 2번째까지]
    except Exception as e:
        pass
        result = ""
    return result


# 댓글 추출
def extractComments(data, lang="en"):
    result = ""
    try:
        if lang == "en":
            result = data[2]
        else:
            result = data[3][:-1]
    except Exception as e:
        pass
        result = ""
    return result


# 날짜, 시간 추출
def extractDateTime(data):
    result = ""
    try:  # data가 datetime="2021.11.13" 라고 하면 result는 2021.11.13.
        result = data.split('datetime="')[1].split('"')[0]
    except Exception as e:
        pass
        result = ""
    return result


# 댓글 출력
def extractCommentsMessage(data):
    results = []
    try:
        # <a class="sqdOP yWX7d     _8A5w5   ZIAjV " href="/dailygrindmag/" tabindex="0">dailygrindmag</a>
        # 사용자 아이디 클래스명
        sp = data.split("sqdOP yWX7d     _8A5w5   ZIAjV")  # 기준으로 자르고 앞 뒤로 리스트
        if len(sp) > 2:  # data에 두번 이상 나오면
            for i in range(len(sp)):  # sp의 길이만큼 반복
                if i > 1:
                    name = sp[i].split(">")[1].split("<")[0]
                    message = sp[i].split(">")[5].split("<")[0]
                    results.append(name + ": " + message)
    except Exception as e:
        pass
        results = []
    return results


# 캡션 출력
def extractCaption(data):
    result = ""
    try:
        splitData = data.split('<img alt="')
        if len(splitData) > 1:
            result = splitData[1].split('"')[0]
        else:
            # only english?
            result = data.split('{"node":{"text":"')[1].split('"}')[0]
            # 파이썬에서 문자열은 유니코드. 인코딩의 의미는
            # 유니코드를 utf-8, ascii형식의 byte코드로 변환하는것.
            result = result.encode('utf-8').decode('unicode-escape')
    except Exception as e:
        pass
        result = ""
    return result

# query list file 읽어오기
def get_query_with_file():
    try:
        with open("querylist.yaml", "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        print("please create 'querylist.yaml' or use utils/yamlutil.py!")
        exit(1)


def runCrawl(limitNum = 0, queryList = [], is_all_comments=False):
    #OS check
    if platform.system() == "Darwin": # Mac OS
        DRIVER = 'driver/chromedriver'
    elif platform.system == "Windows": # Windows
        DRIVER = 'driver\\chromedriver.exe'
    browser = Browser(DRIVER)

    # 로그인 먼저 하고 시작
    browser.goToPage("https://www.instagram.com/accounts/login/")
    time.sleep(2.0)
    browser.driver.find_element_by_name("username").send_keys("아이디")
    time.sleep(2.0)
    browser.driver.find_element_by_name("password").send_keys("비밀번호")
    time.sleep(2.0)
    browser.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
    time.sleep(2.0)
    browser.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    time.sleep(8.0)
    browser.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
    time.sleep(8.0)

    for query in queryList:
        browser.clearLink()  # urlList 초기화
        makeDir("data")  # data 디렉토리 생성
        makeDir("data/" + query)  # data 내부에 query 생성

        mUrl = ""
        # query에 python / #python 들어옴.
        if query[0] == "#":  # 해시태그 검색일 경우             python
            mUrl = "https://www.instagram.com/explore/tags/" + query[1:] + "/?hl=en"
        else:  # 사용자 검색일 경우               pytohn
            mUrl = "https://www.instagram.com/" + query + "/?hl=en"

        browser.goToPage(mUrl)  # driver.get(murl)

        print("collecting url of " + query + "...")
        browser.scrollPageToBottomUntilEnd(browser.collectDpageUrl, limitNum)  # 페이지 전체 스크롤
        print("finish scoll collecting!")

        print("collecting data...")
        slist = list(set(browser.urlList))

        for url in tqdm(slist):  # 프로세스 바
            dirName = url.split("/")[4]
            # skip if already crawled
            if not makeDir("data/" + query + "/" + dirName):
                continue

            browser.goToPage(url)

            time.sleep(30)

            if is_all_comments:
                browser.expandComments()  # 모든 댓긓
            cur = browser.getPageSource()  # return self.driver.page_source

            time.sleep(30)

            writeToFile("data/" + query + "/" + dirName + "/raw.html", [cur])  # html파일에는 cur저장

            time.sleep(30)

            infoData = cur.split("<meta content=")[1].split(" ")

            # extract data
            lang = extractLang(cur)
            likes = extractLikes(infoData, lang)
            comments = extractComments(infoData, lang)
            caption = extractCaption(cur)
            dateTime = extractDateTime(cur)
            commentMessages = extractCommentsMessage(cur)

            # print("likes:",likes," comments:", comments," caption:", caption,
            #     "commentMessages:", commentMessages, "dateTime:", dateTime)
            writeToFile(
                "data/" + query + "/" + dirName + "/info.txt",
                [
                    "likes: ", likes, "",
                    "comments: ", comments, "",
                    "caption: ", caption, "",
                    "commentMessages: ", commentMessages, "",
                    "dateTime: ", dateTime, ""
                ]
            )
            # download image
            imageUrl = html.unescape(cur.split('meta property="og:image" content="')[1].split('"')[0])
            downloadImage(imageUrl, "data/" + query + "/" + dirName + "/image.jpg")
            time.sleep(1)
        print("query " + query + " collecting finish")

    time.sleep(2)
    browser.driver.quit()
    print("FINISH!")


def main():
    args = docopt("""
    Usage:
        crawl.py [-q QUERY] [-n NUMBER] [--a] [-f] [-h HELP]

    Options:
        -q QUERY  username, add '#' to search for hashtags, e.g. 'username' or '#hashtag'
                  For multiple query seperate with comma, e.g. 'username1, username2, #hashtag'
        -n NUM    number of returned posts [default: 1000]
        --a       collect all comments
        -f        get query list with file. file type ALWAYS LIKE 'querylist.yaml'
        -h HELP   show this help message and exit
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

    limitNum = int(args.get('-n', 1000))
    query = args.get('-q', "")
    is_all_comments = args.get('--a', False)
    is_have_file = args.get('-f', "")
    if not query:
        if not is_have_file:
            print('Please input query or query file!')
            exit(1)
        else:
            queryList = get_query_with_file()
            print(queryList)
    else:
        queryList = query.replace(" ", "").split(",")
    #runCrawl(limitNum=limitNum, queryList=queryList, is_all_comments=is_all_comments)


main()
