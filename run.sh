#!/bin/sh

if ps -p `cat /root/scripts/wechat-helper/pid.txt` > /dev/null
then
    echo "wechat robot is running."
else
    echo "wechat robot starts to run."
    nohup python /root/scripts/wechat-helper/robot.py > /root/scripts/wechat-helper/my.log 2>&1 &
    echo $! > /root/scripts/wechat-helper/pid.txt
fi
