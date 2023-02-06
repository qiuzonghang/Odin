# -*- coding: utf-8 -*-
# @Time   : 2023/2/3 17:02
# @Author : qiuzonghang
# @File   : test_emba_register.py

from Common.Function import OpenWebDr
from Params.params import get_login_element
from selenium.webdriver.common.by import By
from Common.Assert import Assertions
import unittest
import HTMLTestRunner
import os
import time

report_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + '/Report'
test = Assertions()


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dr = OpenWebDr()
        cls.dr.start_dr(url='https://testapply.qintelligence.cn/#/')
        cls.embaLoginElement = get_login_element().get('emba_login')
        cls.embaPhoneRegisterElement = get_login_element().get('emba_phone_register')

    @classmethod
    def tearDownClass(cls) -> None:
        time.sleep(5)
        cls.dr.dr_close()

    def test_01_register_emailInvalid(self):
        """
        注册输入无效邮箱
        """
        self.dr.open_emba_login()
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('chinese_phone_register_element')))
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_input_element')), value='123456')
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('first_name_element')))
        text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_tips_element')))
        test.assert_text(text, '请输入正确的邮箱')

    def test_02_register_emailThere(self):
        """
        注册输入已存在邮箱
        """
        self.dr.base_clean(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_input_element')))
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_input_element')), value='2448140961@qq.com')
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('first_name_element')))
        time.sleep(3)
        text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('email_tips_element')))
        test.assert_text(text, '邮箱已存在')

    def test_03_register_cardCnIdInvalid(self):
        self.dr.open_emba_login()
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('chinese_phone_register_element')))
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_type_element')))
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_cnId_element')))
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_number_element')), value='123456')
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('first_name_element')))
        text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_tips_element')))
        test.assert_text(text, '请输入18位证件号码')

    def test_04_register_cardCnIdThere(self):
        self.dr.base_clean(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_number_element')))
        self.dr.base_input(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_number_element')), value='123456789098765432')
        self.dr.base_click(loc=(By.XPATH, self.embaPhoneRegisterElement.get('first_name_element')))
        time.sleep(3)
        text = self.dr.base_get_text(loc=(By.XPATH, self.embaPhoneRegisterElement.get('card_tips_element')))
        test.assert_text(text, '证件号已存在')


    # def test_emba_login(self):
    #     self.dr.open_emba_login()
    #     self.dr.base_input(loc=(By.XPATH, self.embaLoginElement.get('user_element')), value='18210690318')
    #     self.dr.base_input(loc=(By.XPATH, self.embaLoginElement.get('pw_element')), value='qwer1234')
    #     self.dr.base_click(loc=(By.XPATH, self.embaLoginElement.get('ps_element')))


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
