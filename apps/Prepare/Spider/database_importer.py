# -*- coding: utf-8 -*-
# @Time    : 2020/4/6 19:04
# @Author  : Mr.Robot
# @Site    : 
# @File    : database_importer.py
# @Software: PyCharm

import pymysql
import json

connector = pymysql.connect("rm-bp1uk5g6qxw3mqpeevo.mysql.rds.aliyuncs.com", "root", "Doc123456", "DocRetrieval")
cursor = connector.cursor()

doc_items = None
with open(r"./all_detail.json", "r", encoding="utf-8") as all_detail:
    doc_items = json.loads(all_detail.read())

sql = "insert RetrievalCore_document values({0}, '{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}', {8}, null)"
doc_id = 1
for doc in doc_items:
    insert_sql = sql.format(doc_id, pymysql.escape_string(doc["title"]), doc["year"],
                            pymysql.escape_string(json.dumps(doc["authors"], ensure_ascii=False)),
                            pymysql.escape_string(doc["abstract"]), pymysql.escape_string(doc["doi_url"]),
                            pymysql.escape_string(json.dumps(doc["references"], ensure_ascii=False)),
                            pymysql.escape_string(doc["publication"]), -1)
    doc_id += 1
    cursor.execute(insert_sql)

connector.commit()
cursor.close()
connector.close()
