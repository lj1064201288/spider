from pymysql import connect
import csv


MYSQL_NAME = 'jd'
MYSQL_USER = 'root'
MYSQL_PORT = 3306
MYSQL_LOCAL = 'localhost'
MYSQL_PASSWORD = '123456'
MYSQL_TABLE = 'ipad'

class MySqlDemo(object):
    def __init__(self):
        self.name = MYSQL_NAME
        self.user = MYSQL_USER
        self.port = MYSQL_PORT
        self.password = MYSQL_PASSWORD
        self.local = MYSQL_LOCAL
        self.table = MYSQL_TABLE

        self.db = connect(self.local, user=self.user, password=self.password, port=self.port, db=self.name)
        self.cursor = self.db.cursor()

    def read_db(self):
        sql = 'select * from {}'.format(MYSQL_TABLE)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        with open('ipad.txt', 'w+', encoding='utf-8') as f:
            f.write(str(data))

    def close_db(self):
        self.cursor.close()
        self.db.close()


my = MySqlDemo()
my.read_db()
my.close_db()
