import pymysql
import json
import os

DOC_JSON_PATH = r'detail/older/'
connector = pymysql.connect("rm-bp1uk5g6qxw3mqpeevo.mysql.rds.aliyuncs.com", "root", "Doc123456", "DocRetrieval")
cursor = connector.cursor()

doc_items = []
for i in os.listdir(DOC_JSON_PATH):
    with open(DOC_JSON_PATH + i, "r", encoding="utf-8") as detail:
        doc_items += json.loads(detail.read())
print(len(doc_items))

sql = "insert RetrievalCore_document values({0}, '{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}', {8}, {9})"
doc_id = 9001
for doc in doc_items[:6000]:
    insert_sql = sql.format(doc_id, pymysql.escape_string(doc["title"]), -1,
                            pymysql.escape_string(json.dumps(doc["authors"], ensure_ascii=False)),
                            pymysql.escape_string(doc["abstract"]), pymysql.escape_string(doc["doi_url"]),
                            pymysql.escape_string(json.dumps(doc["references"], ensure_ascii=False)),
                            pymysql.escape_string(doc["publication"]), -1, 2)
    print(doc_id)
    doc_id += 1
    cursor.execute(insert_sql)
    connector.commit()

cursor.close()
connector.close()
