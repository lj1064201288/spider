'''
编写MySQL通用Demo
创建数据库，查询，插入，删除，更新
'''

from pymysql import connect

class MySQLDome(object):
    # 初始化
    def __init__(self, host, user, password, database):
        self.db = connect(host=host, user=user, password=password, db=database, port=3306)
        self.cursor = self.db.cursor()

    # 查询所有数据,需要传入sql语句
    def get_all(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e.args)
            return False

    # 获取单条数据, 需要传入sql语句
    def get_one(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(e.args)
            return False

    # 插入数据
    def insert_data(self, table, data):
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) valuse %s'%(table, keys, values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
            print(data, "插入成功！！！")
        except Exception as e:
            print('插入失败！！！',e.args)
            self.db.rollback()
            return False
    # 更新数据
    def updata_data(self, table, data, condition):
        data_str = ''
        for item in data.items():
            data_str = '{}="{}", '.format(item[0], item[1])
        values = data_str[:-1]
        sql = 'updata {} set{} where {}'.format(table, values, condition)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.rowcount
        except Exception as e :
            self.db.rollback()
            print("插入失败!!!", e.args)
            return False
    # 删除数据
    def delete_data(self, table, condition):
        sql = 'delete from {} where {}'.format(table, condition)
        try:
            self.cursor.execute(sql)
            return self.cursor.rowcount
        except Exception as e:
            print(e.args)
            self.db.rollback()
    # 删除表格
    def delete_table(self, table):
        sql = "drop table {}".format(table)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            self.db.rollback()

    # 格式化表格
    def format_table(self, table):
        sql = 'trncate table {}'.format(table)
        try:
            self.cursor.execute(sql)
            return self.cursor.rowcount
        except Exception as e:
            print(e.args)
            self.db.rollback()

    # 执行一条sql语句
    def query(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return int(self.cursor.lastrowid)
        except Exception as e:
            print(e.args)
            self.db.rollback()
            return False





