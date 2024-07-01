import pymysql

# python3用的是pymysql，python2用的是MySQLdb

class OperationMysql:
    """
    数据库SQL相关操作
    """

    def __init__(self):
        self.conn = pymysql.connect(
            host='192.168.1.60',
            port=3306,
            user='root',
            passwd='fm123456',
            db='fenmi_finance',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.conn.cursor()

    # 查询一条数据
    def search_one(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

    # 更新SQL
    def updata_one(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    op_mysql = OperationMysql()
    res = op_mysql.search_one("SELECT * FROM `fenmi_finance`.`fn_item_detail_202405` where id=1;")
    print(res)
