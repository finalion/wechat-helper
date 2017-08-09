#-*- coding:utf-8 -*-
import os
import itchat
from itchat.content import *
import pytz
import datetime
import db
import json
import subprocess

instance = itchat.new_instance()

shell_mode = False

def my_current_time(timezone='Europe/Helsinki'):
    tz = pytz.timezone(timezone)
    t = datetime.datetime.now(tz)
    return t


def save_msg(msg):
    to_store = msg['FromUserName'], msg.get('ActualNickName',None), msg['ToUserName'], msg['Text'] if msg[
        'Type'] == 'Text' else msg['Type'], msg['Type'], msg['CreateTime']
    db.insert(to_store)

def is_me(sender_id):
    return instance.loginInfo['User']['UserName'] == sender_id

@instance.msg_register([TEXT, VIDEO, RECORDING, PICTURE, ATTACHMENT], isGroupChat=False)
def reply_msg_untime(msg):
    print msg['FromUserName']
    if is_me(msg['FromUserName']):
        global shell_mode
        if msg['Text'].lower() == 'shell':
            shell_mode = True
            return (u'enter shell mode')
        if msg['Text'].lower() == 'exit shell':
            shell_mode = False
            return (u'exit shell mode')
        if not shell_mode:
            return
        output = run_cmd(msg['Text'])
        if output:
            return output
   
    if db.connection: save_msg(msg)
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

def run_cmd(cmd):
    args = cmd.split(' ')
    args = [arg for arg in args if arg.strip()]
    if not args:
        return 
    def _format(s):
        return s.split('\n')
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        return output
    except OSError as e:
        # commands with no output
#         print str(e)
        if len(args)>1 and args[0]=='cd':
            os.chdir(args[1])
            output = 'Switch directory: {}'.format(os.getcwd())
            return output
    except subprocess.CalledProcessError as e:
        print str(e)
        print e.returncode
        print e.output
    except Exception as e:
        print str(e)

if __name__ == '__main__':
    instance.auto_login(hotReload=True, #enableCmdQR=2,
                  picDir="/tmp/QR.png",
                  statusStorageDir='/root/scripts/wechat-helper/itchat.pkl')  # deploy on digital ocean
    save_friends_data()
    instance.run()
