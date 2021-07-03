from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import sys
import re

# Made by 7heKnight

# ========================== Pre-Declare ==========================
DRIVER = 'chromedriver.exe'
URL = 'https://facebook.com'
DATA_FILE = 'data.txt'

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

def write_to_text(list_links):
    if not is_file_exist():
        open(DATA_FILE, 'w').close()
    data = open(DATA_FILE, 'r').read()
    file = open(DATA_FILE, 'a')
    for link in list_links:
        if link not in data:
            file.write(link + '\n')
        # else:

# ========================== Browser Process ==========================
def block_options():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--headless') # This will make the chrome executed in hidden
    return chrome_options

def page_down(driver):
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN)
    actions.perform()

# ========================== Data Process ==========================
def required_login():
    opinion = input('[*] Do you want to login (Y/N): ')
    opinion = opinion.lower()
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
        return length
    except:
        print('\n[!] Wrong input. Please re-type.')
        return check_length()

def get_links():
    url = input('[*] Enter the link to crawl: ')
    if 'https://' not in url:
        print('[!] The tool need URL to crawl.')
        return get_links()
    return url

def checking_unwantted_link(post):
    if '/announcements/' not in post and 'page_internal' not in post:
        if '/posts/' in post or '/groups/' in post or '/photos/' in post or '/videos/' in post:
            if 'facebook.com' not in post:
                post = r'https://www.facebook.com' + post
            post = re.sub(r'[?&]comment_id=.+?\[0\].*[/]{0,1}', '', post)
            post = re.sub(r'[?&]__cft__.*[/]{0,1}', '', post)
            post = re.sub(r'[?&]__xts__.*[/]{0,1}', '', post)
            post = re.sub(r'[?&]type=.*[/]{0,1}', '', post)
            post = re.sub(r'[?&]?comment_id=.*[/]{0,1}', '', post)
            return post
    return ''

# ============================= Main Section =============================
if __name__ == '__main__':
    if len(sys.argv) == 1:
        link = get_links()
        sys.argv.append(link)
    if len(sys.argv) > 2:
        sys.exit('[-] Too many arguments. Could not parse.')

    # Prepage process
    opinion = required_login()
    length_crawling_post = check_length()
    print('\n[*] Okay! Executing...\n')

    # Declare the driver (Must follow the version of browser)
    # Chrome driver: https://sites.google.com/a/chromium.org/chromedriver/downloads
    # Other driver, get here: https://selenium-python.readthedocs.io/installation.html#drivers
    browser = webdriver.Chrome(DRIVER, chrome_options=block_options())
    browser.get(URL)

    # if user press yes, this option will run
    if opinion:
        # Checking if the Username or Password is entered
        if USER == '' or PASSWORD == '':
            print('======= PLEASE ENTER YOUR INFORMATION =======')
            USER = input('[*] Enter Username: ')
            PASSWORD = input('[*] Enter Password: ')

        # Entering the username
        userID = browser.find_element_by_id('email')
        userID.send_keys(USER)

        # Entering the password
        passwordID = browser.find_element_by_id('pass')
        passwordID.send_keys(PASSWORD)

        # This will get the ID of login button
        loginID = re.search(r'name="login" data-testid="royal_login_button" type="submit" id="(.+?)"',
                            browser.page_source).group(1)

        # Clicking on login button
        button = browser.find_element_by_id(loginID)
        button.click()

    # ============= Get Post links in groups =============
    browser.get(sys.argv[1])
    sleep(1.5)

    # This loop help you roll down 10 times
    for i in range(length_crawling_post):
        page_down(browser)
        sleep(0.1*randint(3, 5))
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # Find all tag <a>, and parse each link.
    list_links_post = []
    for link in soup.find_all('a'):
        try:
            get_post = link.get('href')
            post = checking_unwantted_link(get_post)
            if post not in list_links_post and post != '':
                list_links_post.append(post)
        except:
            pass

    write_to_text(list_links_post)
    print(f'[+] We got {len(list_links_post)} links')

    # Closing the browser
    browser.close()
