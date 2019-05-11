from pymysql import connect



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

    def create_table(self, table):
        sql = 'CREATE TABLE IF NOT EXISTS {} (' \
              'id INT UNSIGNED AUTO_INCREMENT, ' \
              'title VARCHAR(225) NOT NULL,' \
              ' price VARCHAR(50) NOT NULL, ' \
              'commit VARCHAR(50) NOT NULL, ' \
              'store VARCHAR(50) NOT NULL, ' \
              'href VARCHAR(225) NOT NULL, PRIMARY KEY (id)) DEFAULT CHARSET=UTF8;'.format(self.table)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e.args)

    def insert_data(self, items):
        for item in items:
            data = dict(item)
            keys = ', '.join(data.keys())
            values = ', '.join(['%s']*len(data))
            sql = 'INSERT INTO %s (%s) values (%s)'%(self.table, keys, values)

            try:
                self.cursor.execute(sql, tuple(data.values()))
                self.db.commit()
                print('插入{}成功!'.format(data['title']))

            except Exception as e:
                self.db.rollback()
                print('插入失败!')
                print(e.args)

    def close_db(self):
        self.cursor.close()
        self.db.close()



