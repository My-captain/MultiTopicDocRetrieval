# -*- coding:utf-8 -*-
"""
author:mr.robot
@time: 2020-03-15
@file: statistic.py
"""
import json

with open(r"doc_detail1.json", "r", encoding="utf-8") as file:
    a = json.loads(file.read())
    print(len(a))