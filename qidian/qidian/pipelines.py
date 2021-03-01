# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class QidianPipeline:

    def __init__(self) -> None:
        self.db = pymysql.connect(host="localhost",
                                  user="root",
                                  password="123456",
                                  port=3306,
                                  db="qidian",
                                  charset="utf8mb4")

        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        sql_check = """select * from qidian where title=%s and url=%s"""
        sql_add = """insert into qidian(title,url,author,category,status,bref)
                VALUES (%s,%s,%s,%s,%s,%s)"""
        sql_update = """update qidian set author=%s,category=%s,status=%s,bref=%s  where title=%s and url=%s"""
        data_add = (item["title"], item["url"], item["author"], item["category"], item["status"], item["bref"])
        data_update = (item["author"], item["category"], item["status"], item["bref"], item["title"], item["url"])
        title = item["title"]
        url = item['url']
        try:
            result = self.cur.execute(sql_check, (title, url))
            if result:
                self.cur.execute(sql_update, data_update)
            else:
                self.cur.execute(sql_add, data_add)
            self.db.commit()
        except Exception as e:
            print(e)
        else:
            self.db.commit()
        return item

    def __del__(self):
        self.cur.close()
        self.db.close()
