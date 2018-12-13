#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google翻訳用にクリップボードを操作する
"""

import sys
import re
import pyperclip

MAX_BYTES = 80
DELIMITER = [u'。', u'、']


def copy_clip():
    """
    クリップボードの改行を削除
    """
    # クリップボードのテキストを取得
    org_text = pyperclip.paste()
    print("<<<", org_text)

    if org_text:
        # 改行を削除
        mod_text = re.sub(r'\r', '', org_text)
        mod_text = re.sub(r'\n', '', mod_text)
        print(">>>", mod_text)

        # クリップボードのテキストを更新
        pyperclip.copy(mod_text)


def paste_clip():
    """
    訳文を整える
    """
    # クリップボードのテキストを取得
    org_text = pyperclip.paste()
    print("<<<", org_text)

    if org_text:
        mod_text = u''
        length = 0
        for char in org_text:
            length += len(char.encode())
            mod_text += char

            if length > MAX_BYTES and char in DELIMITER:
                length = 0
                mod_text += '\r\n'

        print(">>>", mod_text)

        # クリップボードのテキストを更新
        pyperclip.copy(mod_text)


if __name__ == '__main__':
    ARGS = sys.argv

    if ARGS[1] == 'copy':
        copy_clip()
    elif ARGS[1] == 'paste':
        paste_clip()
