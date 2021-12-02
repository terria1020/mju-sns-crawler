import platform
import re
import sys
from random import randint
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from docopt import docopt

import yaml

# Made by 7heKnight

# ========================== Pre-Declare==========================
if platform.system() == "Darwin": # Mac OS
    DRIVER = 'driver/chromedriver'
elif platform.system == "Windows": # Windows
    DRIVER = 'driver\\chromedriver.exe'
URL = 'https://facebook.com'
DATA_FILE = 'data.txt'
QUERY_FILE = 'querylist.yaml'

# Input user and password here will not ask user to input uname and password
USER = ''
PASSWORD = ''

# ========================== File Process ==========================
def is_query_exist():
    try:
        open(QUERY_FILE, 'r')
        return True
    except:
        return False

def read_from_query():
    with open(QUERY_FILE, 'r') as file:
        query = yaml.safe_load(file)["Facebook"]
    link = URL + "/" + query[0]
    return link

def is_file_exist():
    try:
        open(DATA_FILE, 'r')
        return True
    except:
        return False

def write_to_text(list_links):
    if not is_file_exist():
        open(DATA_FILE, 'w').close()
    data = open(DATA_FILE, 'r').read() # 중복 확인을 위해 data 변수에 데이터 파일의 모든 데이터를 읽어 저장
    file = open(DATA_FILE, 'a') # 추가 모드인 'a'로 열기
    for link in list_links:
        if link not in data: # 구해 온 링크가 중복이 아니면
            file.write(link + '\n')
        # else:

# ========================== Browser Process ==========================
def chrome_options():
    options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox') # This will prevent malicious code, not useful, just note to remember.
    #options.headless = True # This will make the chrome executed in hidden process
    # options.add_argument('--headless') # This is another way of the upper
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
def required_login():
    opinion = input('[*] Do you want to login (Y/N): ')
    opinion = opinion.lower()
    # 소문자로 변경
    if 'yes' in opinion or 'y' in opinion:
        return True
    elif 'no' in opinion or 'n' in opinion:
        return False
    else:
        print('[!] Wrong option.')
        return required_login()

def check_length():
    try:
        length = int(input('[*] Length of post you want to get (Interger Only!): '))
        # 가져오기를 원하는 포스트의 개수를 입력받음
        return length
    except:
        print('\n[!] Wrong input. Please re-type.')
        return check_length() # 재귀 호출로 입력을 다시 받는다

def get_links():
    url = input('[*] Enter the link to crawl: ')
    if 'https://' not in url: # 입력받은 url 변수에 'https://' 문자열이 포함되어 있지 않으면 url로 판단하지 않겠다
        print('[!] The tool need URL to crawl.')
        return get_links() # 재귀 호출로 입력을 다시 받는다
    return url

def checking_unwantted_link(post):
    if '/announcements/' not in post and 'page_internal' not in post:
        if '/posts/' in post or '/groups/' in post or '/photos/' in post or '/videos/' in post:
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
if __name__ == '__main__':
    if len(sys.argv) == 1: # 실행 인자 개수 파악
        if (is_query_exist()):
            link = read_from_query()
        else:
            link = get_links() # url을 입력받는 함수 호출
        sys.argv.append(link) # argv[2]에 url을 붙여줌
    if len(sys.argv) > 2:
        sys.exit('[-] Too many arguments. Could not parse.')
    # Prepage process
    # opinion = required_login() # 로그인을 할 것인지 선택하게 도와주는 함수 호출
    opinion = False
    # length_crawling_post = check_length() # 가져올 포스팅 수를 입력받는 함수 호출
    length_crawling_post = 10
    print('\n[*] Okay! Executing...\n')

    # Declare the driver (Must follow the version of browser)
    # Chrome driver: https://sites.google.com/a/chromium.org/chromedriver/downloads
    # Other driver, get here: https://selenium-python.readthedocs.io/installation.html#drivers
    browser = webdriver.Chrome(DRIVER, chrome_options=chrome_options()) # selenium 객체 생성

    # if user press yes, this option will run
    if opinion: # 로그인 하겠다고 했으면
        # Checking if the Username or Password is entered
        if USER == '' or PASSWORD == '': # user와 password 변수가 공백이면 입력을 받겠다
            print('======= PLEASE ENTER YOUR INFORMATION =======')
            USER = input('[*] Enter Username: ') # username을 입력받는다
            PASSWORD = input('[*] Enter Password: ') # password를 입력받는다

        browser.get(URL) # 해당 url을 브라우저에서 띄운다
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

    # ============= Get Post links in groups =============
    sleep(1) # 페이지 로딩을 위해 기다립니다.
    browser.get(sys.argv[1]) # 앞에서 붙인 링크를 띄운다.
    sleep(1.5) # 페이지 로딩을 위해 기다립니다.

    # This loop help you roll down 10 times
    for i in range(length_crawling_post):
        page_down(browser) # 페이지를 내려주게 도와주는 함수 호출
        sleep(0.1*randint(3, 5)) # 프로그램 방지 솔루션을 우회한다.
    soup = BeautifulSoup(browser.page_source, 'html.parser') # BeautifulSoup 객체 생성

    # Find all tag <a>, and parse each link.
    list_links_post = []
    for link in soup.find_all('a'): # 'a' 태그를 찾아서 배열로 리턴, 배열 요소를 한 개씩 꺼내서 반복
        try:
            get_post = link.get('href') # 'href' 속성을 찾는다.
            post = checking_unwantted_link(get_post) # 제대로 된 링크인지? 
            if post not in list_links_post and post != '': # 빈 문자열이 아니고 링크 리스트에 포스트가 없으면
                list_links_post.append(post) # 링크 리스트에 링크를 추가한다.
        except:
            pass

    write_to_text(list_links_post) # 배열을 인자로 하여 파일 입출력을 하는 함수를 호출한다.
    print(f'[+] We got {len(list_links_post)} links')

    # Closing the browser
    browser.close()
