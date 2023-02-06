# -*- coding: utf-8 -*-
# @Time   : 2023/2/6 16:27
# @Author : qiuzonghang
# @File   : Assert.py

from Common import Log
import json


class Assertions:
    def __init__(self):
        self.log = Log.MyLog()

    def assert_text(self, text, expected_text):
        """
        :param text:
        :param expected_text:
        :return:
        """
        try:
            assert text == expected_text
            self.log.info("expected_text is %s, text is %s" % (expected_text, text))
            return True

        except:
            self.log.error("expected_text is %s, text is %s" % (expected_text, text))

            raise
