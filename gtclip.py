#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google翻訳結果をクリップボードにコピー
"""

import sys
import re
import tkinter as tk
import pyperclip
from googletrans import Translator
from janome.tokenizer import Tokenizer

MAX_BYTES = 80
DELIMITER_JA = [u'句点', u'読点', u'並立助詞', u'格助詞', u'係助詞']
DELIMITER_EN = [u',', u'.', u' ']


def main():
    """
    クリップボードのテキスト操作
    """
    if len(sys.argv) != 1:
        usage()

    # テキストを取得
    clip_text = pyperclip.paste()

    # テキストの翻訳言語を決める
    translator = Translator()
    detect = translator.detect(clip_text)
    translate_lang = 'en' if detect.lang == 'ja' else 'ja'

    # 改行を削除
    mod_text = remove_return_code(clip_text)

    # 翻訳する
    print("<<<", mod_text)

    try:
        translated_text = translator.translate(mod_text, dest=translate_lang).text
    except:
        translated_text = '*** 翻訳できませんでした。 ***'

    # 訳文を整える
    result_text = u''

    if translate_lang == 'ja':
        result_text = fix_line_length_ja(translated_text, MAX_BYTES, DELIMITER_JA)
    else:
        result_text = fix_line_length_en(translated_text, MAX_BYTES, DELIMITER_EN)

    print(">>>", result_text)

    # クリップボードのテキストを置き換える
    pyperclip.copy(result_text)

    # GUI表示
    gtclip_window(sys.argv[0], 'Original', clip_text, 'Translated', result_text)


def usage():
    """
    使用方法
    """
    print("Usage : python", sys.argv[0])
    sys.exit(1)


def remove_return_code(text):
    """
    テキストの改行を削除
    """
    mod_text = text

    if mod_text:
        # 改行を削除
        mod_text = re.sub(r'\r', '', mod_text)
        mod_text = re.sub(r'\n', '', mod_text)

    return mod_text


def fix_line_length_ja(text, max_bytes, delimiter):
    """
    和訳文を整える
    """
    tokenizer = Tokenizer()

    mod_text = u''
    if text:
        length = 0

        for token in tokenizer.tokenize(text):
            char = token.surface
            speech = token.part_of_speech.split(',')[1]
            length += len(char.encode())
            mod_text += char

            if length > max_bytes and speech in delimiter:
                length = 0
                mod_text += '\r\n'

    mod_text = re.sub(r'\r\n$', '', mod_text)

    return mod_text


def fix_line_length_en(text, max_bytes, delimiter):
    """
    英訳文を整える
    """
    text = re.sub(r'\s+', ' ', text)
    mod_text = u''

    if text:
        length = 0

        for char in text:
            length += len(char.encode())
            mod_text += char

            if length > max_bytes and char in delimiter:
                length = 0
                mod_text += '\r\n'

    mod_text = re.sub(r'\s+\r\n', '\r\n', mod_text)
    mod_text = re.sub(r'\r\n\s+', '\r\n', mod_text)
    mod_text = re.sub(r'\r\n$', '', mod_text)

    return mod_text


def gtclip_window(title, label1, text1, label2, text2):
    """
    GUI表示
    """
    root = tk.Tk()
    root.title(title)

    label_wedget1 = tk.Label(root, text=label1)
    label_wedget1.grid()

    text_wedget1 = tk.Text(root)
    text_wedget1.grid()
    text_wedget1.insert('1.0', text1)

    label_wedget2 = tk.Label(root, text=label2)
    label_wedget2.grid()

    text_wedget2 = tk.Text(root)
    text_wedget2.grid()
    text_wedget2.insert('1.0', text2)

    root.mainloop()


if __name__ == '__main__':
    main()
