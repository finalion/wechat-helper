#!/bin/sh

if ps -p `cat /home/scripts/wechat-helper/pid.txt` > /dev/null
then
    echo "wechat robot is running."
else
    echo "wechat robot starts to run."
    nohup python /home/scripts/wechat-helper/wechat-robot.py > /home/scripts/wechat-helper/my.log 2>&1 &
    echo $! > /home/scripts/wechat-helper/pid.txt
fi
