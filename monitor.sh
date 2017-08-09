#!/bin/sh
cmd=`cat /root/scripts/wechat-helper/cmd | tr -s ["\n"]`
if [ $cmd = '1' ]
then
    if ps -p `cat /root/scripts/wechat-helper/pid.txt` > /dev/null
    then
       echo "run" > /dev/null
    else
       /root/scripts/wechat-helper/run.sh
    fi
else
    /root/scripts/wechat-helper/stop.sh

fi

