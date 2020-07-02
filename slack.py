from slacker import Slacker
import os

#슬랙 토큰으로 객체 생성
token = os.environ.get("TOKEN")
channel = '#grade'
slack = Slacker(token)

def post_to_channel(message):
    print("Send message")
    for i in range(len(message)):
        slack.chat.post_message(channel, message[i], as_user=True)