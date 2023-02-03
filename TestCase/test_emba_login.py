# -*- coding: utf-8 -*-
# @Time   : 2023/2/3 17:02
# @Author : qiuzonghang
# @File   : test_emba_login.py

from Common.Function import OpenWebDr
import unittest


class TestLogin(unittest.TestCase):

    def setUp(self) -> None:
        self.dr = OpenWebDr()
        self.dr.start_dr(url='https://testapply.qintelligence.cn/#/')

    def tearDown(self) -> None:
        self.dr.dr_close()

    def test_emba_login(self):
        self.dr.open_mba_login()
        assert 1 == 1


if __name__ == '__main__':
    unittest.main(verbosity=2)
    suite = unittest.TestSuite()
    suite.addTest(TestLogin('test_emba_login'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
