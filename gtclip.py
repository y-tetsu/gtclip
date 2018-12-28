#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
クリップボードのテキストをGoogle翻訳結果に置き換える
"""

import sys
import time
import re
import pyperclip
from googletrans import Translator
from janome.tokenizer import Tokenizer

MAX_BYTES = 80
DELIMITER_JA = [u'句点', u'読点', u'並立助詞', u'格助詞', u'係助詞']
DELIMITER_EN = [u',', u'.', u' ']


def main():
    """
    クリップボードを翻訳
    """
    if len(sys.argv) != 1:
        usage()

    # クリップボードを監視する
    clip_text_pre = pyperclip.paste()
    clip_text = clip_text_pre

    while True:
        time.sleep(0.05)

        # テキストを取得
        clip_text = pyperclip.paste()

        if clip_text != clip_text_pre:
            # テキストを翻訳
            translated_text = translate_text(clip_text, MAX_BYTES, DELIMITER_JA, DELIMITER_EN)

            # クリップボードのテキストを置き換える
            pyperclip.copy(translated_text)

            # 前回値を更新
            clip_text_pre = translated_text


def usage():
    """
    使用方法
    """
    print("Usage : python", sys.argv[0])
    sys.exit(1)


def translate_text(text, max_bytes, delimiter_ja, delimiter_en):
    """
    テキストを翻訳
    """
    # テキストの翻訳言語を決める
    translator = Translator()
    detect = ""

    try:
        detect = translator.detect(text)
    except:
        print("Error : Connection Error")
        sys.exit(1)

    translate_lang = 'en' if detect.lang == 'ja' else 'ja'

    print("")
    print("--------------------- [Original] ---------------------")
    print(text)

    # 改行を削除
    mod_text = remove_return_code(text)

    # 翻訳する
    translated_text = u''

    try:
        translated_text = translator.translate(mod_text, dest=translate_lang).text
    except:
        translated_text = u'*** 翻訳できませんでした。 ***'

    # 訳文を整える
    result_text = u''

    if translate_lang == 'ja':
        result_text = fix_line_length_ja(translated_text, max_bytes, delimiter_ja)
    else:
        result_text = fix_line_length_en(translated_text, max_bytes, delimiter_en)

    print("")
    print("-------------------- [Translated] --------------------")
    print(result_text)

    return result_text


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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("")
        print("* 終了 *")
        print("")
