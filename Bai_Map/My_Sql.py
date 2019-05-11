'''
MySQL数据库的API
写入创建数据库方法,创建表格方法,插入方法,查找方法,更新与删除方法
'''

from pymysql import connect


# 构建类
class Mysql_API(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = '123456'
        self.db = connect(host=self.host, user=self.user, password=self.password, port=self.port)
        self.cursor = self.db.cursor()

    def create_sql(self, database):
        try:
            self.database = database
            sql = 'create database if not exists ' + database + ' default character set utf8'
            self.cursor.execute(sql)
        except Exception as e:
            print(e.args)

    # 创建数据表
    def create_table(self, table):
        try:
            self.cursor.execute('use ' + self.database)
            sql = 'create table if not exists '  + table + '(park_id INT UNSIGNED AUTO_INCREMENT, ' \
                                                          'uid varchar(200) not null, ' \
                                                          'street_id varchar(200), ' \
                                                          'name varchar(200), ' \
                                                          'address varchar(200), ' \
                                                          'shop_hours varchar(200), ' \
                                                          'detail_url varchar(200) , ' \
                                                          'price varchar(200),' \
                                                          'scope_type varchar(200),' \
                                                          'scope_grade varchar(200),' \
                                                          'content_tag varchar(1000),' \
                                                          'PRIMARY KEY (park_id))'
            self.cursor.execute(sql)
        except Exception as e:
            print(e.args)

    # 插入数据
    def insert_data(self, db, table, data):
        self.cursor.execute('use ' + db)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' %(table, keys, values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            print(data)
            self.db.commit()
        except Exception as e:
            print(e.args)
            self.db.rollback()
    def  db_close(self):
        self.cursor.close()
        self.db.close()

    # @classmethod
    def read_uid(self):
        op = 'use park'
        self.cursor.execute(op)
        sql = 'select uid from park where park_id > 0;'
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        return results

# sql = Mysql_API()
# sql.create_sql('park')
# sql.create_table('particular')
# sql.read_uid()