# mju-sns-crawler

## develop branch

### **라이브러리를 합쳐 놓은 브랜치이며, 개발 단계에서 이 브랜치를 기준으로 사용합니다.**

---

### Requirements:

<aside>
💡 프로그램 실행 전 pip를 이용하여 필요한 모듈을 다운로드 받아야 합니다.

</aside>

```bash
pip install -r requirements.txt
```

<aside>
💡 프로그램은 Chrome 웹 브라우저를 사용하는 자동화 도구인 chromedriver 실행 파일을 사용합니다.
프로그램이 원활히 실행되려면 사용자의 pc에 chrome이 깔려 있는지 확인 해 주세요.

</aside>

- chromedriver를 다운로드 하고 요구사항에 맞게 설정 하는 법
    1. chrome 웹 브라우저를 열고 `새 탭` 을 열어주세요.
    2. `chrome://version` 을 입력하여 들어가 주세요.
    3. 상단의 `96.0.4664.55 (공식 빌드)` 버전을 기억 해 두세요. (사람마다 다를 수 있습니다.)
    4. 하단의 링크를 타고 들어가 각자의 chrome 버전에 맞는 `chromedriver` 를 다운로드 받아 주세요.
        
        [ChromeDriver - WebDriver for Chrome - Downloads](https://chromedriver.chromium.org/downloads)
        
    5. 다운로드 받은 `chromedriver` 실행 프로그램을 프로젝트 폴더의 `driver` 폴더에 넣어 주세요.

---

### How to run:

<aside>
💡 프로젝트 파일 경로에서 실행 해 주세요. 필요한 모듈을 다운로드 후 실행 해 주세요.

</aside>

```bash
python mju_sns_crawler.py
```

---

### How to use:

**<img width="398" alt="그림1" src="https://user-images.githubusercontent.com/38485612/144354682-4a5e8ff3-33d5-471f-ba11-99ba7564f2f1.png">**

1. 크롤링 시 인스타그램/페이스북 로그인이 필요해요. 자신의 **아이디를 입력** 해 주세요.
2. 위와 같은 이유로, 자신의 **비밀번호를 입력** 해 주세요.
3. 크롤링 할 **포스팅의 개수**를 입력 해 주세요. 반드시 **숫자만 입력** 해 주세요.
4. 인별을 크롤링 할 지, 얼굴책을 크롤링 할 지 선택 해 주세요. 버튼을 누르면 **크롤링이 시작**돼요.
5. 크롤링을 할 계정 또는 해시태그가 저장되어 있는 리스트에요.
6. 크롤링을 하고 싶은 계정 또는 해시태그를 입력하는 란이에요.
7. 6번의 입력란에 입력 후 추가하거나, 5번의 리스트에서 쿼리를 선택 해 삭제하는 버튼이에요.
8. 추가적인 크롤링 선택을 위한 리스트에요.
9. 8번의 리스트에서 선택한 옵션에 대해 **추가적인 크롤링**을 해 주는 버튼이에요.
10. 보내고 싶은 이메일의 주소를 기입하는 란이에요.
11. 10번의 이메일 주소에 **이메일을 전송**해주는 버튼이에요.