#-*- coding:utf-8 -*-
import itchat
from itchat.content import *
import pytz
import datetime


def my_current_time(timezone='Europe/Helsinki'):
    tz = pytz.timezone(timezone)
    t = datetime.datetime.now(tz)
    return t


@itchat.msg_register
def reply_msg_isat(msg):
    my_time = my_current_time()
    if 0 <= my_time.hour <= 23:
        # itchat.send(u'我当前时间为凌晨%d点%d分。您的消息可能不会立即回复。（自动回复）' %
        #             (my_time.hour, my_time.minute))
        return u'我当前时间为凌晨%d点%d分。您的消息可能不会立即回复。（自动回复）' %
            (my_time.hour, my_time.minute)


@itchat.msg_register(TEXT,  isGroupChat=True)
def reply_msg_isat(msg):
    if msg['isAt']:
        itchat.send(u'@%s 您的消息已发送到我的邮箱和个人号，我会及时回复，谢谢。（自动回复）' %
                    msg['ActualNickName'], toUserName=msg['FromUserName'])
        itchat.send(u'收到群聊 %s 中 %s 发来的消息: %s' %
                    (msg['ActualUserName'], msg['ActualNickName'], msg['Content']))
        print u'%s %s: 您的消息已发送到我的邮箱和个人号，我会及时回复。----自动回复' % (msg['ActualNickName'], msg['FromUserName'])
        print u'收到 %s 发来的消息: %s' % (msg['FromUserName'], msg['Content'])
        mail_content(msg)


def mail_content(msg):
    return
itchat.auto_login(hotReload=True, enableCmdQR=2)  # deploy on digital ocean
itchat.run()
