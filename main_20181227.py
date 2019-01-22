# -*- coding: utf8 -*-
# coding: utf8

'''
THIS IS FOR NSRRC TPS FRONT-END MONITORING
THE CHATBOT IS MADE BY Y.Z. LIN @ NSRRC VACUUM GROUP
IF THIS CODE IS HELP FOR YOUR WORK
PLEASE CITED:
"Development of a Task-Oriented Chatbot Application for Monitoring Taiwan Photon Source Front-End System" PCaPAC 2018

Yu-Zheng Lin
2019.1.22
'''

import time
from datetime import datetime

import mysql.connector as mysql
import pytz
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (ImageSendMessage, MessageEvent,
                            TemplateSendMessage, TextMessage, TextSendMessage)

from module.RuleBasedEngine import Rule_Based_Engine

app = Flask(__name__, static_url_path='/static')

line_bot_api = LineBotApi('***YOUR CHANNEL ACCESS TOKEN***')
handler = WebhookHandler('***YOUR CHANNEL SECRET***')


def Log_to_SQL(userID, NickName, messageType, messageID, message, timestamp):
    db = mysql.connect(
        host="127.0.0.1",
        user='root',
        passwd='',
        database='')
    # Transfer to DateTime
    ts = str(timestamp)
    ts = datetime.utcfromtimestamp(int(ts[0:10])).strftime('%Y-%m-%d %H:%M:%S')
    dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
    dt = dt.astimezone(pytz.timezone('Asia/Taipei'))
    ts = dt.strftime("%Y-%m-%d %H:%M:%S")

    cursor = db.cursor()
    query = "INSERT INTO message (userid, NickName, messageType, messageID, message, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (userID, NickName, messageType, messageID, message, ts)
    cursor.execute(query, values)
    db.commit()
    db.close()


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    start = time.time()  # Start time
    # =================== User Profile ========================
    try:
        profile = line_bot_api.get_profile(event.source.user_id)
        print("**Send by %s" % profile.display_name)
    except:
        print("**Not a friend of the Bot")
    '''
    # Uncomment to enable message logging
    # ======Log to SQL======
    try:
        Log_to_SQL(userID=event.source.user_id, NickName=profile.display_name, messageType=event.message.type,
                   messageID=event.message.id, message=event.message.text, timestamp=event.timestamp)
        print("Log to SQL sucessful")
    except:
        print("Log to SQL Error!")
    '''
    # =================== Change Richmenu ======================
    if "&Back" == event.message.text:
        RichMenu1 = "richmenu-"  # !!!!
        line_bot_api.link_rich_menu_to_user(event.source.user_id, RichMenu1)
        profile = line_bot_api.get_profile(event.source.user_id)
        print("Set RichMenu1 to %s" % profile.display_name)
    if "&Next" == event.message.text:
        RichMenu2 = "richmenu-"  # !!!!
        line_bot_api.link_rich_menu_to_user(event.source.user_id, RichMenu2)
        print("Set RichMenu2 to %s" % profile.display_name)

    Reply_Result = Rule_Based_Engine(event)
    if Reply_Result == 0:
        return 0
    line_bot_api.reply_message(event.reply_token, Reply_Result)
    end = time.time()
    print(end-start)


# ==================================================================
if __name__ == "__main__":
    print("--------------------------------------------------------------------------------")
    print("NSRRC Line Chatbot Service by YZ Lin")
    print("Version:20181227")
    print("Service Start Time:")
    print(time.strftime("%Y/%d/%m %H:%M:%S"))
    print("--------------------------------------------------------------------------------")
    app.run(port=5001, debug=True)
