# -*- coding: utf-8 -*-
# @Time    : 2020/4/4 22:59
# @Author  : Mr.Robot
# @Site    : 
# @File    : detail_cleaner.py
# @Software: PyCharm
import json
import os


def clean_detail(detail_path):
    detail_cleaned = list()
    detail_files = os.listdir(detail_path)
    for detail_file in detail_files:
        json_content = None
        with open(r"{0}\{1}".format(detail_path, detail_file), "r", encoding="utf-8") as file:
            json_content = json.loads(file.read())
        for doc_item in json_content:
            doc_item["year"] = int(detail_file.split("_")[2].split(".")[0])
            for author_idx in range(len(doc_item["authors"])):
                if "\n" in doc_item["authors"][author_idx]:
                    doc_item["authors"][author_idx] = doc_item["authors"][author_idx].split("\n")[0]
            doc_item["abstract"] = doc_item["abstract"].replace("ABSTRACT\n", "")
        detail_cleaned.extend(json_content)
    return detail_cleaned


if __name__ == '__main__':
    detail_list = clean_detail(r"C:\Users\Mr.Robot\Desktop\workspace\SmartDocRetrieval-master\apps\PreComputeModule\Spider\detail")
    with open(r"../all_detail.json", "w", encoding="utf-8") as details:
        details.write(json.dumps(detail_list, ensure_ascii=False))
