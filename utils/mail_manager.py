import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from string import Template
import os

host = {
    'id': 'sampleid',
    'pw': 'samplepw'
}

server = 'smtp.naver.com'
port = 587

class MailManager():
    CID_NUMBERING = 0
    def __init__(self, _to) -> None:
        self._from = host['id'] + "@naver.com"
        self._to = _to
        self.data = MIMEMultipart()
        self.data['From'] = self._from
        self.data['To'] = self._to
        self.template_contents = Template("""
        <html>
        <head>
        </head>
        <body>
            <h1>새 알림이 있습니다.</h1>
            <h3> 이 메일은 명지대학교 크롤러에 의해 자동 작성된 글입니다.</h3>
            <br>
            <hr>
            <p>${contents}</p>
            <hr>
        </body>
        </html>
        """)
        self.contents = ""

        self.smtp = smtplib.SMTP(server, port) 
        self.smtp.ehlo()
        self.smtp.starttls()

    def add_facebook_contents(self, content: str):
        self.contents = content
        return self
    
    def add_insta_contents(self, content: str, cid_numbering: int):
        self.contents = self.contents + "<hr>" + f"<br><img src='cid:capture{cid_numbering}'><br>" + content
        return self

    def add_title(self, title: str):
        self.data['Subject'] = title
        return self

    def add_image(self, path: str, cid_numbering: int = 0):
        with open(path, "rb") as file:
            image = MIMEImage(file.read(), Name="image.jpg")
            image.add_header('Content-ID', f'<capture{cid_numbering}>')
            self.data.attach(image)

    # def add_contents(self):
    #     text = MIMEText(self.template_contents.substitute(fb_contents=self.fb_contents, insta_contents=self.insta_contents), _subtype='html', _charset='utf-8')
    #     self.data.attach(text)

    def send(self) -> None:
        #self.add_contents()
        text = MIMEText(self.template_contents.substitute(contents=self.contents), _subtype='html', _charset='utf-8')
        self.data.attach(text)
        self.smtp.login(host['id'], host['pw'])
        self.smtp.sendmail(self._from, self._to, self.data.as_string())

class DataReader():
    @staticmethod
    def insta_read(tasklist: list, mailmgr: MailManager):
        content = ""
        for task in tasklist:
            file_list = os.listdir(f"data/{task}")
            if ".DS_Store" in file_list:
                file_list.remove(".DS_Store")

            for seed in file_list:
                mailmgr.add_image(f"data/{task}/{seed}/image.jpg", MailManager.CID_NUMBERING)
                with open(f"data/{task}/{seed}/info.txt", "r", encoding='UTF8') as f:
                    lines = f.readlines()
                content = lines[1] + "<br>" + lines[4] + "<br>" + lines[10]
                mailmgr.add_insta_contents(content, MailManager.CID_NUMBERING)
                MailManager.CID_NUMBERING += 1