# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3

class Day029Pipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect ("ptt.db") 
        self.cur = self.conn.cursor()
        
        sql = '''Create table ptt(  
                article_id TEXT,
                article_title TEXT,
                article_author TEXT,
                date TEXT,
                article_content TEXT,
                ip TEXT,
                messages TEXT,
                message_count INT,
                url TEXT
                )'''
        self.cur.execute(sql)
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
    def process_item(self, item, spider):
        article_id = item['article_id']
        article_title = item['article_title']
        article_author = item['article_author']
        article_content= item['article_content']
        ip = item['ip']
        messages = item['messages']
        message_count = item['message_count']
        date = item['article_date']
        url = item['url']
        x = (article_id, article_title, article_author, date, article_content, ip, messages, message_count, url)
        sql = '''insert into fastfood_ptt values(?,?,?,?,?,?,?,?,?)'''  
        self.conn.execute(sql,x)
        return item