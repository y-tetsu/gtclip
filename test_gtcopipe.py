#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unittest
"""

import unittest
import gtcopipe


class TestGtCopiPe(unittest.TestCase):
    "gtcopipe test"
    delimiter = [u'句点', u'読点', u'並立助詞', u'格助詞', u'係助詞']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_remove_return_code(self):
        """
        改行を削除
        """
        text = "test\r\ntest\rtest\n"
        result = gtcopipe.remove_return_code(text)
        self.assertEqual(result, "testtesttest")

    def test_fix_line_length1(self):
        """
        訳文を整える
        """
        text = "おはよう、こんにちは、こんばんは。"
        result = gtcopipe.fix_line_length(text, 3, self.delimiter)
        self.assertEqual(result, "おはよう、\r\nこんにちは、\r\nこんばんは。\r\n")

    def test_fix_line_length2(self):
        """
        訳文を整える
        """
        text = "おはよう、こんにちは、こんばんは。"
        result = gtcopipe.fix_line_length(text, 20, self.delimiter)
        self.assertEqual(result, "おはよう、こんにちは、\r\nこんばんは。")

    def test_fix_line_length3(self):
        """
        訳文を整える
        """
        text = "おはよう、こんにちは、こんばんは。"
        result = gtcopipe.fix_line_length(text, 80, self.delimiter)
        self.assertEqual(result, "おはよう、こんにちは、こんばんは。")


if __name__ == '__main__':
    unittest.main()
