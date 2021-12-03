import time
from tkinter import *
from tkinter import messagebox

from PIL import ImageTk

import extra_crawler
import facebook_crawler
import insta_crawler
from utils.browser import Browser
from utils.mail_manager import DataReader, MailManager
from utils.yamlmanager import YamlManager




def complete_func(entEmail): # 완료 버튼 눌렀을 때 함수
    print("완료 버튼 클릭됨")
    mailmgr = MailManager(entEmail.get())

    mailmgr.add_title("새 알림이 있습니다.")

    mailmgr.data_append(DataReader.insta_read(mailmgr))
    mailmgr.data_append(DataReader.facebook_read(mailmgr))
    mailmgr.data_append(DataReader.extra_read(mailmgr))
    
    mailmgr.send()

def newTask(entAddAccount, lb): # add task 버튼 눌렀을 때 함수
    task = entAddAccount.get()
    if task != "":
        lb.insert(END, task)
        YamlManager.write("Tasklist", task)
        entAddAccount.delete(0, "end")
    else:
        messagebox.showwarning("warning", "Please enter some task.")

def deleteTask(lb): # delete task 버튼 눌렀을 때 함수
    YamlManager.remove("Tasklist", lb.get(ANCHOR))
    lb.delete(ANCHOR)

def printList(listbox, lb, browser): # 추가 사이트 선택한것들 출력 (listBtn 눌렀을때)
    print(listbox.curselection())
    extra_crawler.main(browser, listbox.curselection())

def GUIstart(browser):
    
    root = Tk() # 전체 화면
    root.geometry('500x780+850+5') # 가로 x 세로 + x좌표 + y좌표
    root.title('명지대 크롤러')
    root.config(bg='#3c72b5') # background 배경, config 변경
    root.resizable(width=False, height=False)

    width = 100
    height = 100
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    img_path = ImageTk.PhotoImage(file = "img/mju.jpg", master= root)
    shapes = canvas.create_image(width/2, height/2, image = img_path)

    entId = Entry(root, width=30) # 아이디 입력
    entId.insert(0, "sample@sample.com")
    def entryclear(event):
        if entId.get() == "sample@sample.com":    # 초기값인 경우 마우스클릭하면 지워지도록,...
            entId.delete(0,len(entId.get()))
    entId.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
    entId.pack(pady=10)

    entPw = Entry(root, show="*", width=30) # 비밀번호 입력
    entPw.insert(0, "samplepw")
    def entryclear(event):
        if entPw.get() == "samplepw":    # 초기값인 경우 마우스클릭하면 지워지도록,...
            entPw.delete(0,len(entPw.get()))
    entPw.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
    entPw.pack(pady=10)
    entPw.pack()

    entNum = Entry(root, width=30) # 아이디 입력
    entNum.insert(0, "원하는 포스트 수를 입력하세요")
    def entryclear(event):
        if entNum.get() == "원하는 포스트 수를 입력하세요":    # 초기값인 경우 마우스클릭하면 지워지도록,...
            entNum.delete(0,len(entNum.get()))
    entNum.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
    entNum.pack(pady=5)

    sns_button_frame = Frame(root) # 인스타, 페북 버튼 두개 프레임
    sns_button_frame.pack(pady=10) # 위아래로 여백

    insta_btn = Button( # 인스타 버튼
        sns_button_frame, # root 프레임
        text='instagram',
        font=('times 14'),
        bg='#c5f776',
        padx=20, # 버튼 가로 공간
        pady=10, # 버튼 세로 공간
        #command = insta_func # 눌렀을 시 실행 메서드
    )
    # pack 해야 실제 루트에 버튼 포함 됨
    #insta_btn.pack(fill=BOTH, expand=True, side=LEFT)

    face_btn = Button( # 페북 버튼
        sns_button_frame,
        text='facebook',
        font=('times 14'),
        bg='#ff8b61',
        padx=20,
        pady=10,
        #command = lambda: face_func(entId, entPw) # 눌렀을 시 실행 메서드
    )

    frame = Frame(root)
    frame.pack(pady=10)

    lb = Listbox(
        frame,
        width=25,
        height=6,
        font=('Times', 14),
        bd=0,
        fg='#464646', # foreground(글자 색)
        highlightthickness=0,
        selectbackground='#a6a6a6',
        activestyle="none",
        
    )
    lb.pack(side=LEFT, fill=BOTH)

    task_list = YamlManager.read("Tasklist")

    for item in task_list:
        lb.insert(END, item)

    sb = Scrollbar(frame)
    sb.pack(side=RIGHT, fill=BOTH)

    lb.config(yscrollcommand=sb.set)
    sb.config(command=lb.yview)

    entAddAccount = Entry(root, width=30)
    entAddAccount.insert(0, "추가할 계정")
    def entryclear(event):
        if entAddAccount.get() == "추가할 계정":    # 초기값인 경우 마우스클릭하면 지워지도록,...
            entAddAccount.delete(0,len(entAddAccount.get()))
    entAddAccount.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 
    entAddAccount.pack()

    button_frame = Frame(root)
    button_frame.pack(pady=20)

    addTask_btn = Button(
        button_frame, # root
        text='Add Task',
        font=('times 14'),
        bg='#c5f776',
        padx=20, # 버튼 가로 공간
        pady=10, # 버튼 세로 공간
        command = lambda: newTask(entAddAccount, lb)
    )
    # pack 해야 실제 루트에 버튼 포함 됨
    addTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

    delTask_btn = Button(
        button_frame,
        text='Delete Task',
        font=('times 14'),
        bg='#ff8b61',
        padx=20,
        pady=10,
        command = lambda: deleteTask(lb) # 버튼을 동작시킴. 누르면 deleteTask메서드 실행.
    )
    delTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

    listbox = Listbox(root, selectmode="extended", height = 0, font=('Times', 14),)
    listbox.insert(0, "학교공지")
    listbox.insert(1, "컴공공지")
    listbox.insert(2, "명대신문")
    listbox.pack()

    listBtn = Button(root, text="학교 사이트 크롤링", padx=10, pady=10, command=lambda: printList(listbox, lb, browser))
    listBtn.pack(pady=3)

    entEmail = Entry(root, width=30) # 이메일 입력
    entEmail.insert(0, YamlManager.read("Sendto"))
    def entryclear(event):
        if entEmail.get() == "sample@sample.com":    # 초기값인 경우 마우스클릭하면 지워지도록,...
            entEmail.delete(0,len(entEmail.get()))
    entEmail.bind("<Button-1>", entryclear)  # 마우스를 클릭하면 entryclear를 동작시켜라. 

    def editmail(event):
        temp = YamlManager.read("Sendto")[0]
        YamlManager.write("Sendto", entEmail.get())
        YamlManager.remove("Sendto", temp)
    
    entEmail.bind("<Return>", editmail)

    entEmail.pack(pady=20)
    entEmail.pack(pady=10)

    # 완료 버튼 클릭 시 입력한 이메일로 메일 보냄
    complete_btn = Button(root, padx=10, pady=10, text = "완료", command = lambda: complete_func(entEmail))
    complete_btn.pack()

    '''instaEndBtn = Button(root, padx=10, pady=10, text = "인스타완료")
    #instaEndBtn = Button(root, padx=10, pady=10, text = "인스타완료", command = lambda: insta_end_func(root))
    instaEndBtn.pack()'''

    def instaLogin(): # 인스타 로그인 메서드
        browser.goToPage("https://www.instagram.com/accounts/login/")
        time.sleep(2.0)
        browser.driver.find_element_by_name("username").send_keys(entId.get())
        time.sleep(2.0)
        browser.driver.find_element_by_name("password").send_keys(entPw.get())
        time.sleep(2.0)
        browser.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(2.0)
        browser.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(8.0)
        browser.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
        time.sleep(8.0)
        insta_crawler.main(browser, lb.get(0, lb.size()), int(entNum.get())) ########################## 인스타 버튼 누르면 crawl.py 실행

    insta_btn.config(command = instaLogin) # id, pw입력하고 insta버튼 누르면 로그인 실행
    insta_btn.pack(fill=BOTH, expand=True, side=LEFT)

    def face_func(): # face버튼 눌렀을 때 함수
        facebook_crawler.faceCrawl(browser, lb.get(0, lb.size()), int(entNum.get()), entId.get(), entPw.get())

    face_btn.config(command = face_func)
    face_btn.pack(fill=BOTH, expand=True, side=LEFT)
    
    root.mainloop() # 로그인 하고 tkinter 닫으면 크롤링 실행

GUIstart(Browser("driver/chromedriver"))
