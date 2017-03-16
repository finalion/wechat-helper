#!/bin/sh
cmd=`cat /home/scripts/wechat-helper/cmd | tr -s ["\n"]`
if [ $cmd = '1' ]
then
    if ps -p `cat /home/scripts/wechat-helper/pid.txt` > /dev/null
    then
       echo "run" > /dev/null
    else
       /home/scripts/wechat-helper/run.sh
    fi
else
    /home/scripts/wechat-helper/stop.sh

fi

