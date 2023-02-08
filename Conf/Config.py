# -*- coding: utf-8 -*-
# @Time   : 2022/8/1 11:03
# @Author : qiuzonghang
# @File   : Config.py

import os
import sys

from configparser import ConfigParser
from Common import Log


class Config:
    # titles:
    TITLE_DEV = "env_dev"
    TITLE_UAT = "env_uat"
    TITLE_TEST = "env_test"

    # values:
    # [debug\release]
    VALUE_TESTER = "tester"
    VALUE_ENVIRONMENT = "environment"
    VALUE_VERSION_CODE = "versionCode"
    VALUE_SITE_URL = "site_url"
    VALUE_APPLY_URL = "apply_url"
    VALUE_SQL_HOST = "sql_host"
    VALUE_SITE_DATABASE = 'site_database'
    VALUE_APPLY_DATABASE = 'apply_database'
    VALUE_TEST_DATABASE = 'test_database'
    VALUE_SQL_USER = 'sql_user'
    VALUE_SQL_PW = 'sql_pw'

    # path
    path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def __init__(self, env):
        """
        初始化
        """
        self.config = ConfigParser()
        self.log = Log.MyLog()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")

        self.config.read(self.conf_path, encoding='utf-8')

        self.site_url = self.get_conf(env, Config.VALUE_SITE_URL)
        self.apply_url = self.get_conf(env, Config.VALUE_APPLY_URL)
        self.sql_host = self.get_conf(env, Config.VALUE_SQL_HOST)
        self.site_database = self.get_conf(env, Config.VALUE_SITE_DATABASE)
        self.apply_database = self.get_conf(env, Config.VALUE_APPLY_DATABASE)
        self.sql_user = self.get_conf(env, Config.VALUE_SQL_USER)
        self.sql_pw = self.get_conf(env, Config.VALUE_SQL_PW)

        self.test_database = self.get_conf('dev', Config.VALUE_TEST_DATABASE)

    def get_conf(self, env, value):
        """
        配置文件读取
        :param env:
        :param value:
        :return:
        """
        return self.config.get('env_' + env, value)

    def set_conf(self, title, value, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(title, value, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, title):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(title)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)
