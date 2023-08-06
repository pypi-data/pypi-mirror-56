#-*-coding:utf-8-*-
import  pymysql

class create_connection():
    '''
    主要用来对数据库进行建立链接，使用with as 方式，避免主动提交和关闭链接操作
    '''

    def __init__(self,**kwargs):
        self.host = kwargs.get('host',None)
        self.port = kwargs.get('port',None)
        self.user = kwargs.get('user',None)
        self.passwd = kwargs.get('passwd',None)
        self.db = kwargs.get('db',None)

        if self.host is None or self.port is None or self.user is None or self.passwd is None or self.db is None:
             raise  Exception('链接数据库缺少参数,host,port,user,passwd,db请确认这几个')

    def __enter__(self):
        self.conn = pymysql.connect(host=self.host, port = self.port, user=self.user, passwd = self.passwd, db = self.db)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()