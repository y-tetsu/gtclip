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


def main():
    """
    クリップボードのテキスト操作
    """
    args = sys.argv

    if args[1] == 'copy':
        clip_text = pyperclip.paste()
        mod_text = remove_return_code(clip_text)
        pyperclip.copy(mod_text)

    elif args[1] == 'paste':
        clip_text = pyperclip.paste()
        mod_text = fix_line_length(clip_text, MAX_BYTES, DELIMITER)
        pyperclip.copy(mod_text)


def remove_return_code(text):
    """
    テキストの改行を削除
    """
    mod_text = text
    print("<<<", mod_text)

    if mod_text:
        # 改行を削除
        mod_text = re.sub(r'\r', '', mod_text)
        mod_text = re.sub(r'\n', '', mod_text)

    print(">>>", mod_text)
    return mod_text


def fix_line_length(text, max_bytes, delimiter):
    """
    訳文を整える
    """
    print("<<<", text)

    mod_text = u''
    if text:
        length = 0
        for char in text:
            length += len(char.encode())
            mod_text += char

            if length > max_bytes and char in delimiter:
                length = 0
                mod_text += '\r\n'

    print(">>>", mod_text)
    return mod_text


if __name__ == '__main__':
    main()
