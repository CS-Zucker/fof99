# -*- coding: utf-8 -*-
import time
import pymysql


class fundDatabase:
    # 获取当前时间
    def getcurrenttime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    # 数据库初始化 修改对应的连接信息
    def __init__(self, host='127.0.0.1', user='root', passwd='1234', db='fund', port=10306, charset='utf8'):
        pymysql.install_as_MySQLdb()
        try:
            self.charset = charset
            self.connect = pymysql.connect(
                host=host, user=user, passwd=passwd, db=db, port=10306, charset='utf8')
            self.connect.ping(True)  # 使用mysql ping来检查连接,实现超时自动重新连接
            # print(self.getcurrenttime(), u"MySQL DB Connect Success:",
                #   user + '@' + host + ':' + str(port) + '/' + db)
            self.cur = self.connect.cursor()
        except Exception as e:
            print(self.getcurrenttime(), u"MySQL DB Connect Error :%d: %s" %
                  (e.args[0], e.args[1]))

   # 建数据表
    def createTable(self):
        try:
            # self.db.set_character_set('utf8')
            # 创建fund_list表
            create_fund_list_sql = """
                CREATE TABLE IF NOT EXISTS `fund_list`(
                    `code` varchar(255) NOT NULL COMMENT '基金代码',
                    `name` varchar(255) NOT NULL COMMENT '基金名称',
                    `type` varchar(255) NOT NULL COMMENT '基金类型',
                    `name_short` varchar(255) DEFAULT NULL COMMENT '基金简称',
                    PRIMARY KEY(`code`, `name`)
                ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
            """
            # 创建fund_value表
            create_fund_value_sql ="""
                CREATE TABLE IF NOT EXISTS `fund_value`(
                    `fund_code` VARCHAR(255) NOT NULL COMMENT '基金代码',
                    `fund_name` VARCHAR(255) NOT NULL COMMENT '基金名称',
                    `value_date` DATE NOT NULL COMMENT '净值日期',
                    `unit_value` DECIMAL(10, 4) NOT NULL COMMENT '单位净值',
                    `acml_value` DECIMAL(10, 4) NOT NULL COMMENT '累计净值',
                    `daily_rate` VARCHAR(255) NOT NULL COMMENT '日增长率',
                    `subscrp_status` VARCHAR(255) DEFAULT NULL COMMENT '申购状态',
                    `redempt_status` VARCHAR(255) DEFAULT NULL COMMENT '赎回状态',
                    `dividend` VARCHAR(255) DEFAULT NULL COMMENT '分红送配',
                    PRIMARY KEY (`fund_code`, `fund_name`, `value_date`),
                    FOREIGN KEY (`fund_code`) REFERENCES `fund_list`(`code`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                """
            create_table_statements = [create_fund_list_sql, create_fund_value_sql]
            try:
                for sql in create_table_statements:
                    result = self.cur.execute(sql)
                self.connect.commit()
                # 判断是否执行成功
                if result:
                    # print (self.getCurrentTime(), u"Create Table Sucess")
                    pass
                else:
                    return 0
            except Exception as e:
                # 发生错误时回滚
                self.connect.rollback()
                print(self.getcurrenttime(), u"Create Table Failed: %s" % e)
                return 0
        except Exception as e:
            print(self.getcurrenttime(), u"MySQLdb Error: %s" % e)
            return 0
        
    # 插入数据
    def insertData(self, table, my_dict):
        try:
            # self.db.set_character_set('utf8')
            cols = ', '.join(my_dict.keys())
            values = '","'.join(my_dict.values())
            sql = "replace into %s (%s) values (%s);" % (
                table, cols, '"' + values + '"')
            # print (sql)
            try:
                result = self.cur.execute(sql)
                insert_id = self.connect.insert_id()
                self.connect.commit()
                # 判断是否执行成功
                if result:
                    # print (self.getcurrenttime(), u"Data Insert Sucess")
                    return insert_id
                else:
                    return 0
            except Exception as e:
                # 发生错误时回滚
                self.connect.rollback()
                print(self.getcurrenttime(), u"Data Insert Failed: %s" % e)
                return 0
        except Exception as e:
            print(self.getcurrenttime(), u"MySQLdb Error: %s" % e)
            return 0


    # 搜索数据
    def selectData(self, table, my_key):
        try:
            # self.db.set_character_set('utf8')
            sql = f"""
                    SELECT code, name, type, name_short
                    FROM {table}
                    WHERE code LIKE '%{my_key}%' OR name LIKE '%{my_key}%';
                """ 
            # print (sql)
            try:
                result = self.cur.execute(sql)
                search_list=[]
                # 判断是否执行成功
                if result:
                    # print (self.getcurrenttime(), u"Data Select Sucess")
                    for item_search in self.cur.fetchall():
                        search_list.append(item_search)    
                    return search_list
                else:
                    return 0
            except Exception as e:
                # 发生错误时回滚
                self.connect.rollback()
                print(self.getcurrenttime(), u"Data Select Failed: %s" % e)
                return 0
        except Exception as e:
            print(self.getcurrenttime(), u"MySQLdb Error: %s" % e)
            return 0
