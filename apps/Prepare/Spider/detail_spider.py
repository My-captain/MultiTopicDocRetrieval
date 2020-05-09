# -*- coding: utf-8 -*-
# @Time    : 2020/3/15 15:14
# @Author  : Mr.Robot
# @Site    : 
# @File    : detail_spider.py
# @Software: PyCharm

import json
import time
from selenium import webdriver
from random import uniform


def alert():
    print("\a")


def get_empty_doc():
    return {
        "title": None,
        "authors": None,
        "publication": None,
        "abstract": None,
        "references": None,
        "doi_url": None
    }


def save_detail(href_list, year):
    with open(r"./detail/doc_detail_{0}.json".format(year), "w", encoding="utf-8") as file:
        file.write(json.dumps(href_list, ensure_ascii=False))


prefers = {
    'profile.default_content_setting_values': {
        'images': 2,
        'javascript': 2,
    }
}
option = webdriver.ChromeOptions()
option.add_experimental_option('prefs', prefers)
driver = webdriver.Chrome(executable_path='./browser_driver/chromedriver.exe', options=option)
# driver = webdriver.Firefox(executable_path='./geckodriver.exe')
# driver = webdriver.Firefox()


def get_links(year):
    href_list = None
    with open(r"./link_list/detail_links_{0}.json".format(year), "r", encoding="utf-8") as file:
        file_content = file.read()
        href_list = json.loads(file_content)
    return href_list


def crawl_detail(year):
    link_list = get_links(year)
    detail_list = list()
    detail_idx = 0
    for url in link_list:
        try:
            detail_idx += 1
            print("{0}年{1}条".format(year, detail_idx))
            driver.get(url)
            # try:
            #     show_more_items = driver.find_element_by_class_name("show-more-items__btn-holder")
            #     button = show_more_items.find_element_by_class_name("btn--inverse")
            #
            #     button.click()
            # except Exception as e:
            #     print("点击按钮时出现异常,{0}".format(e))
            title = driver.find_element_by_class_name("citation__title").text
            authors = list()
            author_card = driver.find_element_by_id("sb-1")
            for i in author_card.find_elements_by_class_name("loa__item"):
                authors.append(i.text)
            publication = driver.find_element_by_class_name("epub-section__title").text
            abstract = driver.find_element_by_class_name("hlFld-Abstract").text
            references = list()
            refers = driver.find_elements_by_class_name("references__item")
            for refer in refers:
                if len(refer.text) > 0:
                    references.append(refer.text)
        except Exception as e:
            print("出现异常")
            alert()
            continue
        doc = get_empty_doc()
        doc["title"] = title
        doc["authors"] = authors
        doc["publication"] = publication
        doc["abstract"] = abstract
        doc["references"] = references
        doc["doi_url"] = url
        detail_list.append(doc)
        save_detail(detail_list, year)

        sleep_duration = uniform(0.1, 1)
        print("sleep for {0}s".format(sleep_duration))
        time.sleep(sleep_duration)


if __name__ == '__main__':
    # year = 2017
    # for i in range(2):
    #     crawl_detail(year+i)
    crawl_detail(2019)
