import pymysql


class ConnectMySQL:

    def __init__(self):
        self.db = pymysql.connect(host="localhost", user="root", password="123456", port=3306)
        self.cur = self.db.cursor()

    def sql_execute(self,sql):
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            if result:
                return result
            else:
                if sql:
                    return "未查询到任何数据"
                else:
                    return "sql语句无效"
        except Exception as e:
            return e
