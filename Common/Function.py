# -*- coding: utf-8 -*-
# @Time   : 2023/2/3 15:01
# @Author : qiuzonghang
# @File   : Function.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as chromeService
from selenium.webdriver.firefox.service import Service as firefoxService
from selenium.webdriver.edge.service import Service as edgeService
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from Common.Log import MyLog
from selenium.webdriver.support import expected_conditions as EC
from Conf.Config import Config
from selenium.webdriver.support.wait import WebDriverWait
from Params.params import get_login_page_element
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
import os
import time
import pymssql
import sys

log = MyLog()


class OpenWebDr:
    def __init__(self):
        login_page_element = get_login_page_element()
        self.emba_login_element = (By.XPATH, login_page_element.get('emba'))
        self.mba_login_element = (By.XPATH, login_page_element.get('mba'))
        self.mbax_login_element = (By.XPATH, login_page_element.get('mbax'))
        self.dba_login_element = (By.XPATH, login_page_element.get('dba'))
        self.mbao_login_element = (By.XPATH, login_page_element.get('mbao'))
        self.pm_login_element = (By.XPATH, login_page_element.get('pm'))
        self.camp_login_element = (By.XPATH, login_page_element.get('camp'))

    def start_dr(self, url, dr_type='edge', over_time=30):
        """
        :param url: 网址
        :param dr_type: 浏览器，仅支持火狐、谷歌、edge
        :param over_time: 隐式等待时间，实际未使用，忽略
        :return:
        """
        dr_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/DriverFile/'
        if dr_type == 'chrome':
            self.dr = webdriver.Chrome(service=chromeService(dr_path + 'chromedriver.exe'))
            log.info('open chrome...')
        elif dr_type == 'firefox':
            self.dr = webdriver.Firefox(service=firefoxService(dr_path + 'geckodriver.exe'))
            log.info('open firefox...')
        elif dr_type == 'edge':
            self.dr = webdriver.Edge(service=edgeService(dr_path + 'msedgedriver.exe'))
            log.info('open edge...')
        else:
            log.error('框架目前仅支持Chrome/Firefox/Edge')
            raise

        self.dr.get(url)
        self.dr.maximize_window()
        log.info('打开%s，窗口最大化，隐式等待%ss' % (url, over_time))
        return self.dr

    # 显式等待
    def base_find(self, loc, timeout=30, poll=0.5, dr=None):
        log.info('正在定位:{}元素'.format(loc))
        if dr is None:
            dr = self.dr
        try:
            location = WebDriverWait(dr, timeout=timeout, poll_frequency=poll).until(
                EC.presence_of_element_located(loc))
            return location
        except selenium.common.exceptions.TimeoutException:
            log.error('元素定位超时！')
        except selenium.common.exceptions.StaleElementReferenceException:
            log.error('未定位到元素！')

    # 点击元素方法
    def base_click(self, loc):
        el = self.base_find(loc)
        log.info("正在对:{} 元素进行行点击事件".format(loc))
        el.click()

    # 输入元素方法
    def base_input(self, loc, value):
        el = self.base_find(loc)
        log.info("正在对:{} 元素输入{}".format(loc, value))
        el.send_keys(value)

    # 获取文本信息
    def base_get_text(self, loc):
        a = self.base_find(loc).text
        log.info("正在获取:{} 元素文本值".format(loc))
        return a

    # 清空输入框
    def base_clean(self, loc):
        self.base_find(loc).clear()
        log.info("正在清空:{} 元素文本值".format(loc))

    def base_select(self, loc_a, loc_b):    # 无调用
        ActionChains(self.dr).move_to_element(self.base_find(loc_a)).perform()
        self.base_click(loc_b)
        time.sleep(3)

    def dr_close(self):
        self.dr.quit()
        log.info("关闭浏览器.....")

    def open_emba_login(self):
        self.base_click(self.emba_login_element)
        log.info("进入EMBA登录页")

    def open_mba_login(self):
        self.base_click(self.mba_login_element)
        log.info("进入MBA登录页")

    def open_mbax_login(self):
        self.base_click(self.mbax_login_element)
        log.info("进入MBAX登录页")

    def open_dba_login(self):
        self.base_click(self.dba_login_element)
        log.info("进入DBA登录页")

    def open_mbao_login(self):
        self.base_click(self.mbao_login_element)
        log.info("进入MBA海外登录页")

    def open_pm_login(self):
        self.base_click(self.pm_login_element)
        log.info("进入专业硕士登录页")

    def open_camp_login(self):
        self.base_click(self.camp_login_element)
        log.info("进入学术夏令营登录页")


class ConnectSql:
    """
    数据库操作
    """

    def __init__(self, host, user, pw, database):
        try:
            self.conn = pymssql.connect(host, user, pw, database, charset='cp936')
            self.cur = self.conn.cursor()
            log.info("连接数据库" + host)
        except:
            log.error("连接数据库失败。")
            raise

    def select_sql(self, sql):
        try:
            self.cur.execute(sql)
            log.info("查询数据，sql=%s" % sql)
            return self.cur.fetchall()
        except:
            log.error("查询错误，sql=%s" % sql)
            raise

    def insert_sql(self, sql):
        try:
            self.cur.execute(sql)
            log.info("插入数据，sql=%s" % sql)
            return True
        except pymssql._pymssql.OperationalError as e:
            log.error("插入错误，错误信息：%s，sql=%s" % (e, sql))
            raise
        except:
            log.error("插入错误，sql=%s" % sql)
            raise

    def close_sql(self):
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            log.info("断开数据库连接。")
        except:
            log.error("断开数据库失败。")


def get_env():
    """
    :return: 执行环境
    """
    conf = Config('dev')
    cnt_sql = ConnectSql(host=conf.sql_host, user=conf.sql_user, pw=conf.sql_pw, database=conf.test_database)
    env = cnt_sql.select_sql("select env from flask_db.function_env where function_type = 'webAutoTest'")
    cnt_sql.close_sql()
    return env


def get_conf(env=get_env()[0][0]):
    """
    :param env: 默认从数据库中获取执行环境
    :return: 环境配置
    """
    return Config(env)


print(type(sys.platform))
