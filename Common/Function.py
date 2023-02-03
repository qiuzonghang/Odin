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
import os
import time

log = MyLog()


class OpenWebDr:
    def __init__(self):
        pass

    def start_dr(self, url, dr_type='edge', over_time=30):
        """
        :param url:
        :param dr_type:
        :param over_time:
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
            log.error('web框架目前仅支持Chrome/Firefox/Edge')
            raise

        self.dr.get(url)
        self.dr.maximize_window()
        log.info('打开url，窗口最大化，隐式等待%ss' % over_time)
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
        log.info("正在对:{} 元素实行点击事件".format(loc))
        el = self.base_find(loc)
        # time.sleep(3)
        el.click()

    # 输入元素方法
    def base_input(self, loc, value):
        log.info("正在对:{} 元素输入{}".format(loc, value))
        el = self.base_find(loc)
        # el.clear()
        el.send_keys(value)

    # 获取文本信息
    def base_get_text(self, loc):
        log.info("正在获取:{} 元素文本值".format(loc))
        a = self.base_find(loc).text
        return a


test = OpenWebDr()

test.start_dr(url='https://testapply.qintelligence.cn/#/')

time.sleep(5)
