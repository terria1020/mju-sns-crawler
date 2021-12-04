import os
import platform
import re
import shutil
from random import randint
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from insta_crawler import downloadImage, makeDir, writeToFile

# Made by 7heKnight

# ========================== Pre-Declare==========================
'''if platform.system() == "Darwin": # Mac OS
    DRIVER = 'driver/chromedriver'
elif platform.system == "Windows": # Windows
    DRIVER = 'driver\\chromedriver.exe'''

DRIVER = 'driver/chromedriver' # 위도우 맥 같음
URL = 'https://facebook.com'
DATA_FILE = 'data.txt'
QUERY_FILE = 'querylist.yaml'

# Input user and password here will not ask user to input uname and password
USER = ''
PASSWORD = ''

# ========================== File Process ==========================
def is_file_exist():
    try:
        open(DATA_FILE, 'r')
        return True
    except:
        return False

def write_to_text_for_n(list_links, n):
    if not is_file_exist():
        open(DATA_FILE, 'w').close()

    with open(DATA_FILE, 'a') as file:
        for i in range(n):
            file.write(list_links[i] + '\n')

# ========================== Browser Process ==========================
def chrome_options():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # This will disable print the console information
    # 크롬 드라이버에 추가 옵션을 설정 해 주는 메소드, 인자: key, value로 제공되어 있다.
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2}) # Disable the asking allow notification or block
    # 특정 사이트에서 크롬이 '알림을 표시하겠습니까?'라고 하는 메시지를 disable 하게 추가 옵션을 설정한다.
    return options

def page_down(driver):
    actions = ActionChains(driver)
    # ActionChains는 여러 개의 동작을 체인으로 묶어서 저장하고 실행할 수 있다고 한다.
    actions.send_keys(Keys.PAGE_DOWN)
    # 기능키인 PAGEDOWN을 누르라고 함
    actions.perform()
    # 체인 실행

# ========================== Data Process ==========================
def checking_unwantted_link(post):
    if '/announcements/' not in post and 'page_internal' not in post:
        #if '/posts/' in post or '/groups/' in post or '/photos/' in post or '/videos/' in post:
        if '/photos/' in post:
            if 'facebook.com' not in post:
                post = r'https://www.facebook.com' + post # 문자열 앞에 r을 붙이면 raw 문자열, \, $% 등을 치환하지 않고 내용 그대로 문자열로 인식
            post = re.sub(r'[?&]comment_id=.+?\[0\].*[/]{0,1}', '', post) # 정규 표현식 라이브러리 사용하여 문자열을 치환
            post = re.sub(r'[?&]__cft__.*[/]{0,1}', '', post)
            post = re.sub(r'[?&]__xts__.*[/]{0,1}', '', post)
            post = re.sub(r'[?&]type=.*[/]{0,1}', '', post)
            post = re.sub(r'[?&]comment_id=.*[/]{0,1}', '', post)
            return post
    return ''

# ============================= Main Section =============================
def faceCrawl(_browser, queryList, limitNum, user, passwd):
    browser = webdriver.Chrome(DRIVER, chrome_options=chrome_options()) # selenium 객체 생성

    open(DATA_FILE, 'w').close()

    url_list = []
    #browser = _browser.driver
    browser.get(URL) # 해당 url을 브라우저에서 띄운다

    USER = user
    PASSWORD = passwd
    

    # Entering the username
    userID = browser.find_element_by_id('email') # 'email' 아이디를 가진 요소를 찾는다.
    userID.send_keys(USER) # 키보드 입력으로 user 변수의 내용을 보낸다

    # Entering the password
    passwordID = browser.find_element_by_id('pass') # 'pass' 아이디를 가진 요소를 찾는다
    passwordID.send_keys(PASSWORD) # 키보드 입력으로 password 변수의 내용을 보낸다

    # This will get the ID of login button
    loginID = re.search(r'name="login" data-testid="royal_login_button" type="submit" id="(.+?)"',
                        browser.page_source).group(1)
    # 버튼의 id를 정규식으로 찾는다

    # Clicking on login button
    button = browser.find_element_by_id(loginID) # 정규식 텍스트를 기반으로 html요소를 찾는다.
    button.click() # 버튼 요소를 클릭하게 한다
    for query in queryList:
        browser.get(URL)
        sleep(1.5)
        url = f"https://www.facebook.com/search/photos/?q={query}&sde=Abq90qzjNQQ7j6Zii7ABTX7wlmUNJLXIlOTvyY-9HQuVz2D418DJDVyev1fYu_AJrwedeQQYIYWBDSO2G8LFfE1fASfb9IgXZUh42kbczgtO5kZPmnk1aKNWYUYAodeffBo"

        sleep(1) # 페이지 로딩을 위해 기다립니다.
        browser.get(url) # 앞에서 붙인 링크를 띄운다.
        sleep(1.5) # 페이지 로딩을 위해 기다립니다.
        page_down(browser)

        soup = BeautifulSoup(browser.page_source, 'html.parser') # BeautifulSoup 객체 생성

        # Find all tag <a>, and parse each link.
        list_links_post = []
        for link in soup.find_all('a'): # 'a' 태그를 찾아서 배열로 리턴, 배열 요소를 한 개씩 꺼내서 반복
            try:
                get_post = link.get('href') # 'href' 속성을 찾는다.
                post = checking_unwantted_link(get_post) # 제대로 된 링크인지? 
                if post not in list_links_post and post != '': # 빈 문자열이 아니고 링크 리스트에 포스트가 없으면
                    if len(post.split('/')) > 6:
                        list_links_post.append(get_post) # 링크 리스트에 링크를 추가한다.
            except:
                pass

        write_to_text_for_n(list_links_post, limitNum) # 배열을 인자로 하여 파일 입출력을 하는 함수를 호출한다.
        print(f'[+] We got {len(list_links_post)} links')

    with open(DATA_FILE, 'r') as file:
        url_list = file.readlines()

    
    dir_path = "facebookdata/"

    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

    for url in url_list:
        try:
            browser.get(url)
            sleep(2)
            soup2 = BeautifulSoup(browser.page_source, 'html.parser')

            image = soup2.find('img')
            author = soup2.find('a', attrs={'class': 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p'})
            content = soup2.find('span', attrs={'class': 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v b1v8xokw oo9gr5id'})
            if content:
                content = content.text
            else:
                content = ""
            

            image_src = image['src']

            makeDir("facebookdata/"+url.split('/')[3]+"/"+url.split('/')[5][0:10])

            writeToFile(
                "facebookdata/"+url.split('/')[3]+"/"+url.split('/')[5][0:10]+"/info.txt", 
                [   
                    "author: ", author.text, "",
                    "content: ", content, "",
                    "url: ", url
                ]
            )

            downloadImage(image_src,"facebookdata/"+url.split('/')[3]+"/"+url.split('/')[5][0:10]+"/image.jpg")
        except:
            pass

    browser.close()
