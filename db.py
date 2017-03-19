import pymysql

connection = 0
try:
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='fengliang',
                             db='wechatmsg',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
except:
    pass

def insert(data):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `msg` (`FromUserName`, `ActualNickName`, `ToUserName`,`Text`,`Type`,`CreateTime`) VALUES (%s, %s,%s,%s,%s,%s)"
            cursor.execute(sql, data)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
        connection.commit()
    finally:
        # connection.close()
        pass


def query():
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()


def update_friends():
    pass    
if __name__ == '__main__':
    update_friends()
   
