import pymysql
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='fengliang',
                             db='wechatmsg',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def insert(data):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `msg` (`from_username`, `to_username`,`content`,`type`,`create_time`) VALUES (%s, %s,%s,%s,%s)"
            cursor.execute(sql, data)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()


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
