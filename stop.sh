pid=`cat /home/scripts/wechat-helper/pid.txt`
if ps -p $pid > /dev/null
then 
    kill -9 $pid
    echo 'wechat robot is stopped.'
else 
    echo 'wechat robot is not running.' 
    
# rm pid.txt
fi


