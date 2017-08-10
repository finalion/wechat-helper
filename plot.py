import pymysql
connection = pymysql.connect(host='104.236.16.224',
                             user='root',
                             password='fengliang',
                             db='wechatmsg',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

sql = "SELECT `id`, `FromUserName`,`Text` FROM `msg`"
sql = "SELECT `FromUserName`, COUNT(*) FROM `msg` WHERE `FromUserName` NOT LIKE '@@%' GROUP BY `FromUserName` ORDER BY COUNT(*) DESC "
cursor.execute(sql)
results = cursor.fetchall()
print results[0]
import matplotlib.pyplot as plt
results = results[:20]
plt.bar(range(0, len(results)), [each['COUNT(*)'] for each in results])
plt.xticks(range(0, len(results)), [
           each['FromUserName'] for each in results], rotation=90)
plt.grid(axis='y')
plt.show()
