# -*- coding: utf-8 -*-
# @Time    : 2020/3/15 13:58
# @Author  : Mr.Robot
# @Site    : 
# @File    : selenium_spider.py
# @Software: PyCharm

import json
import time
from selenium import webdriver
import random


def save_links(detail_links, year_num):
    with open(r"./detail_links_{0}.json".format(year_num), "w", encoding="utf-8") as file:
        file.write(json.dumps(list(detail_links), ensure_ascii=False))


driver = webdriver.Chrome(executable_path="./browser_driver/chromedriver.exe")
url_template = "https://dl.acm.org/action/doSearch?fillQuickSearch=false&ConceptID=80&expand=dl&field1=AllField&AfterMonth=1&AfterYear={0}&BeforeMonth=12&BeforeYear={0}&startPage={1}&pageSize=50"
year = 2015

for y in range(5):
    year = 2013 - y
    this_year_links = set()
    for page_idx in range(40):
        try:
            url = url_template.format(year, page_idx)
            driver.get(url)

            titles = driver.find_elements_by_class_name("hlFld-Title")
            for title in titles:
                title = title.find_element_by_tag_name("a")
                this_year_links.add(title.get_attribute("href"))
            save_links(this_year_links, year)
            duration = random.uniform(0.8, 2)
            time.sleep(duration)
        except Exception as e:
            print("year:{0},page:{1},\nException:{2}".format(year, page_idx, e))
            print('\a')


