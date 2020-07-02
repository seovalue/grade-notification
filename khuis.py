from selenium import webdriver
from bs4 import BeautifulSoup
import threading
import time
import os

def settings():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    return options

def get_grade(path):
    print("Get info from khuis")
    # 현재 로컬 폴더에서 chromedriver 가져오기,chrome_options=options
    options = settings()
    driver = webdriver.Chrome(path,chrome_options=options)

    # 종정시 페이지 열기
    driver.get('https://khuis.khu.ac.kr')
    driver.implicitly_wait(30)

    # 알림창 닫기
    try:
        driver.find_element_by_xpath('/html/body/div[7]/div[1]/button').click()
    except:
        print("알림창이 사라졌어요!")

    # 아이디, 비밀번호 로그인하기
    id = os.environ.get("khuisId")
    pw = os.environ.get("khuisPw")

    driver.find_element_by_id('userId').send_keys(id)
    driver.find_element_by_id('userPw').send_keys(pw)
    driver.find_element_by_xpath('//*[@id="loginFrm"]/div/div[2]/div[1]/div[2]/button').click()

    # 로그인 후 포탈 접속
    # 포탈 접속 후 코로나 알림창 닫기
    driver.implicitly_wait(30)

    try:
        driver.find_element_by_xpath('//*[@id="introPopup2"]/div[2]/a').click()
    except:
        print("코로나 알림창이 사라졌어요!")


    #코로나 알림창 대신 새로운 알림창이 생김...
    try:
        driver.find_element_by_xpath('/html/body/div[10]/div[1]/a').click()
    except:
        print("정전 알림창이 사라졌어요!")

    # 수업/성적 클릭
    driver.find_element_by_xpath('//*[@id="gnb"]/ul/li[2]/a').click()

    # 금학기 성적 조회 클릭
    driver.find_element_by_xpath('//*[@id="gnb"]/ul/li[2]/ul/li[3]/ul/li[1]/a[1]').click()

    # slack bot에게 전달할 메세지
    message = []

    gradeCheck = True
    # 성적보기 조회 클릭
    try:
        driver.find_element_by_xpath('//*[@id="baseForm"]/div[1]/div[2]/table/tbody/tr[1]/td[6]/a').click()
    except:
        gradeCheck = False
        message.append("성적조회기간이 아닙니다.")

    # 성적 내역이 존재하는지 확인
    if(gradeCheck):
        pageSource = driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')
        emptyList = soup.find('td', class_="NO_RESULT")
        #gradeList = soup.find_all('tr', class_="first last").find_all('td',class_="first")
        gradeList = soup.select('td.first')

        if emptyList is None:
            inputMessage = "[마감된 성적 내역]"
            for i in range(len(gradeList)):
                if(gradeList[i].text != "성적공시(정정)기간" and gradeList[i].text != "성적열람기간"):
                    inputMessage += "\n" + gradeList[i].text
            message.append(inputMessage)
        else:
            message.append("마감된 성적이 없습니다.")

    driver.close()
    return message
