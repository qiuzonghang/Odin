# -*- coding: utf-8 -*-
# @Time   : 2022/8/1 11:36
# @Author : qiuzonghang
# @File   : params.py
import random

from Common.Log import MyLog
from Conf.Config import Config
from Params.get_yaml import GetPages
import time
import re

log = MyLog()
get_data = GetPages()


def arr_sql_param(sql_title, sql_data_list):
    arr_result = []
    try:
        for sql_data in sql_data_list:
            arr_dict = {}
            for sql_num in range(len(sql_data)):
                arr_dict[sql_title[sql_num]] = sql_data[sql_num]
            arr_result.append(arr_dict)
        return arr_result
    except TypeError:
        arr_dict = {}
        for sql_num in range(len(sql_data_list)):
            arr_dict[sql_title[sql_num]] = sql_data_list[sql_num]
        return arr_dict


def arr_sql_title(sql_title):
    sql_title_list = []
    [sql_title_list.append(title[0]) for title in sql_title]
    return sql_title_list


def param_id_desc(list_data, sort_param='id'):
    for num1 in range(len(list_data)):
        for num2 in range(len(list_data) - num1 - 1):
            if list_data[num2][sort_param] < list_data[num2 + 1][sort_param]:
                list_data[num2], list_data[num2 + 1] = list_data[num2 + 1], list_data[num2]
    return list_data


def get_login_page_element():
    log.info("获取招生端各个招生项目元素。")
    return get_data.get_page_list().get('login_element')[0].get('apply_login_page')


def get_login_element():
    log.info("获取招生端各个招生项目元素。")
    return get_data.get_page_list().get('login_element')[0]
