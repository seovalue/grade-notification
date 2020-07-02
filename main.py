import os
from slack import post_to_channel as post_message_to_slack
from khuis import get_grade as get_grade_from_khuis
from apscheduler.schedulers.blocking import BlockingScheduler
import time

'''
Todo.

1. selenium 자동화 & soup 크롤링해서 성적이 나왔는지 확인하기
2. slack bot 만들기
3. slack bot과 프로그램 연동하기
4. 성적이 나오면, slack bot을 통해 알림 가도록

'''
print("Check for chrome driver...")
#현재 로컬 폴더에서 chromedriver 가져오기
path = os.environ.get("CHROMEDRIVER_PATH")
#path = os.getcwd() + "/chromedriver.exe"
#path = path.replace("\\","/")


sched = BlockingScheduler()

@sched.scheduled_job('interval',hours = 2)
def startProgram():
    print("Running Program")
    gradeInfo = get_grade_from_khuis(path)
    post_message_to_slack(gradeInfo)


#startProgram()
sched.start()







