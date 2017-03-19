#-*- coding:utf-8 -*-
import os
import itchat
from itchat.content import *
import pytz
import datetime
import db
import json

instance = itchat.new_instance()

def my_current_time(timezone='Europe/Helsinki'):
    tz = pytz.timezone(timezone)
    t = datetime.datetime.now(tz)
    return t


def save_msg(msg):
    to_store = msg['FromUserName'], msg.get('ActualNickName',None), msg['ToUserName'], msg['Text'] if msg[
        'Type'] == 'Text' else msg['Type'], msg['Type'], msg['CreateTime']
    db.insert(to_store)


@instance.msg_register([TEXT, VIDEO, RECORDING, PICTURE, ATTACHMENT], isGroupChat=False)
def reply_msg_untime(msg):
    print msg
    if db.connection: save_msg(msg)
    print 'lasdfasdfasd'
    my_time = my_current_time()
    if 0 <= my_time.hour < 7:
        # itchat.send(u'我当前时间为凌晨%d点%d分。您的消息可能不会立即回复。（自动回复）' %
        #             (my_time.hour, my_time.minute))
        return u'我当前时间为凌晨%d点%d分。您的消息可能不会立即回复。（自动回复）' % (my_time.hour, my_time.minute)


@instance.msg_register(TEXT,  isGroupChat=True)
def reply_msg_isat(msg):
    if db.connection: save_msg(msg)
    if msg['isAt']:
        my_time = my_current_time()
        instance.send(u'%s 群聊 %s 中 %s 发来消息: %s' % (my_time.ctime(),
                                                 msg['ActualUserName'], msg['ActualNickName'], msg['Content']))
        if 0 <= my_time.hour < 7:
            # itchat.send(u'我当前时间为凌晨%d点%d分。您的消息可能不会立即回复。（自动回复）' %
            #             (my_time.hour, my_time.minute))
            return u'@%s 我当前时间为凌晨%d点%d分。您的消息可能不会立即回复。（自动回复）' % (msg['ActualNickName'], my_time.hour, my_time.minute)

        return u'@%s 您的消息已发送到我的邮箱和个人号，我会及时回复。（自动回复）' % msg['ActualNickName']

def save_friends_data(update=False):
    friends = instance.get_friends(update=update)
    with open('friends.json','wb') as f:
        json.dump(friends,f)
    return friends

if __name__ == '__main__':
    instance.auto_login(hotReload=True, enableCmdQR=2,
                  picDir="/home/scripts/wechat-helper/QR.png",
                  statusStorageDir='/home/scripts/wechat-helper/itchat.pkl')  # deploy on digital ocean
    save_friends_data()
    instance.run()
