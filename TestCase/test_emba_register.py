# -*- coding: utf-8 -*-
# @Time   : 2023/2/3 17:02
# @Author : qiuzonghang
# @File   : test_emba_register.py

from Common.Function import OpenWebDr, get_conf, ConnectSql
from Params.params import get_login_element
from selenium.webdriver.common.by import By
from Common.Assert import Assertions
import unittest
import HTMLTestRunner
import os
import time

report_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/Report'
test = Assertions()
conf = get_conf()


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dr = OpenWebDr()
        cls.dr.start_dr(url=conf.apply_url)
        cls.cnt_sql = ConnectSql(host=conf.sql_host, user=conf.sql_user, pw=conf.sql_pw, database=conf.apply_database)
        cls.embaLoginElement = get_login_element().get('emba_login')
        cls.embaPhoneRegisterElement = get_login_element().get('emba_phone_register')

    @classmethod
    def tearDownClass(cls) -> None:
        time.sleep(5)
        cls.cnt_sql.close_sql()
        cls.dr.dr_close()

    def test_01_register_emailInvalid(self):
        """
        emba手机号注册输入无效邮箱
        """
        self.dr.open_emba_login()
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('chinese_phone_register_element')))
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_input_element')), value='123456')
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('first_name_element')))
        time.sleep(1)
        text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_tips_element')))
        test.assert_text(text, '请输入正确的邮箱')

    def test_02_register_emailThere(self):
        """
        emba手机号注册输入已存在邮箱
        """
        self.dr.base_clean(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_input_element')))
        sql_rst = self.cnt_sql.select_sql(sql="select Email from AbpUsers order by CreationTime desc")
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_input_element')), value=sql_rst[0][0])
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('first_name_element')))
        time.sleep(3)
        text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_tips_element')))
        test.assert_text(text, '邮箱已存在')

    def test_03_register_cardCnIdInvalid(self):
        """
        emba手机号注册身份证不足18位
        """
        self.dr.base_click(loc=(By.CLASS_NAME, self.embaPhoneRegisterElement.get('card_type_element')))
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_cnId_element')))
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_number_element')), value='123456')
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('first_name_element')))
        time.sleep(1)
        text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_tips_element')))
        test.assert_text(text, '请输入18位证件号码')

    def test_04_register_cardCnIdThere(self):
        """
        emba手机号注册身份证已存在
        """
        self.dr.base_clean(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_number_element')))
        sql_rst = self.cnt_sql.select_sql(sql="select IDCardNo from GSMRegisterInfos where CardType like '72' and ProjectCode = 'emba'  order by Id desc")
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_number_element')), value=sql_rst[0][0])
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('first_name_element')))
        time.sleep(3)
        text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_tips_element')))
        test.assert_text(text, '证件号已存在')

    def test_05_register_phoneInvalid(self):
        """
        emba手机号注册手机号格式不正确
        """
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('phone_input_element')), value='123456')
        time.sleep(1)
        tips_text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('phone_tips_element')))
        test.assert_text(tips_text, '请输入正确的手机号')

    def test_06_register_phoneThere(self):
        """
        emba手机号注册手机号已存在
        """
        self.dr.base_clean(loc=(By.XPATH, self.embaPhoneRegisterElement.get('phone_input_element')))
        sql_rst = self.cnt_sql.select_sql(sql="select PhoneNumber from AbpUsers where PhoneNumber is not NULL order by CreationTime desc")
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('phone_input_element')), value=sql_rst[0][0])
        time.sleep(3)
        tips_text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('phone_tips_element')))
        test.assert_text(tips_text, '手机号已存在')


if __name__ == '__main__':
    # report_abspath = os.path.join(report_path, "result.html")
    # fp = open(report_abspath, "wb")
    # # 报告详情
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
    #                                        title=u'自动化测试报告,测试结果如下：',
    #                                        description=u'用例执行情况：')
    unittest.main()
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLogin))
    runner = unittest.TextTestRunner()
    runner.run(suite)
