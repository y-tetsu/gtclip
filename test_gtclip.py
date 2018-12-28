#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unittest
"""

import unittest
import gtclip


class TestGtClip(unittest.TestCase):
    "gtclip test"
    delimiter_ja = [u'句点', u'読点', u'並立助詞', u'格助詞', u'係助詞']
    delimiter_en = [u',', u'.', u' ']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_remove_return_code(self):
        """
        改行を削除
        """
        text = "test\r\ntest\rtest\n"
        result = gtclip.remove_return_code(text)
        self.assertEqual(result, "testtesttest")

    def test_fix_line_length1(self):
        """
        訳文を整える
        """
        text = "おはよう、こんにちは、こんばんは。"
        result = gtclip.fix_line_length_ja(text, 3, self.delimiter_ja)
        self.assertEqual(result, "おはよう、\r\nこんにちは、\r\nこんばんは。")

    def test_fix_line_length2(self):
        """
        訳文を整える
        """
        text = "おはよう、こんにちは、こんばんは。"
        result = gtclip.fix_line_length_ja(text, 20, self.delimiter_ja)
        self.assertEqual(result, "おはよう、こんにちは、\r\nこんばんは。")

    def test_fix_line_length3(self):
        """
        訳文を整える
        """
        text = "おはよう、こんにちは、こんばんは。"
        result = gtclip.fix_line_length_ja(text, 80, self.delimiter_ja)
        self.assertEqual(result, "おはよう、こんにちは、こんばんは。")

    def test_fix_line_length4(self):
        """
        訳文を整える
        """
        text = "Good  morning. Hello.    Good afternoon."
        result = gtclip.fix_line_length_en(text, 3, self.delimiter_en)
        self.assertEqual(result, "Good\r\nmorning.\r\nHello.\r\nGood\r\nafternoon.")

    def test_fix_line_length5(self):
        """
        訳文を整える
        """
        text = "Good  morning. Hello.    Good afternoon."
        result = gtclip.fix_line_length_en(text, 10, self.delimiter_en)
        self.assertEqual(result, "Good morning.\r\nHello. Good\r\nafternoon.")

    def test_fix_line_length6(self):
        """
        訳文を整える
        """
        text = "Good  morning. Hello.    Good afternoon."
        result = gtclip.fix_line_length_en(text, 80, self.delimiter_en)
        self.assertEqual(result, "Good morning. Hello. Good afternoon.")


if __name__ == '__main__':
    unittest.main()
