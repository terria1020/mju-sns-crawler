import schedule
import time
import subprocess
import yaml

from utils.mail_manager import MailManager

def main():
    schedule.every(1).minutes.do(run_fb_crawl)
    schedule.every(1).minutes.do(run_insta_crawl)
    schedule.every(1).minutes.do(run_mail_manager)
    loop()

def loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_fb_crawl():
    subprocess.run(["python", "facebook_post_crawler.py"])

def run_insta_crawl():
    subprocess.run(["python", "crawl.py", "-f", "-n", "10"])

def run_mail_manager():
    with open("querylist.yaml", 'r') as file:
        sendto = yaml.safe_load(file)["Sendto"]
        sendto = sendto[0]
    mailmgr = MailManager(_to=sendto)
    mailmgr.add_title("새 알림이 있습니다.")
    mailmgr.add_facebook_contents("페이스북 콘텐츠 테스트")
    mailmgr.add_image("/Users/jaehan1346/Documents/캡처/test.png", 1)
    mailmgr.add_insta_contents("인스타 콘텐츠 테스트", 1)
    mailmgr.send()

if __name__ == '__main__':
    main()