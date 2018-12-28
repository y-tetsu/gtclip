# gtclip
クリップボードのテキストをGoogle翻訳の結果に置き換える

## Description
クリップボードのテキストを監視し、更新された場合は
Google翻訳で英⇒和もしくは和⇒英して結果をクリップボードにコピーする。

翻訳時は改行を削除し、結果は1行が80byte程度になるよう改行を入れて成型する。

## Usage
 1. コマンドプロンプトにて python gtclip.py を実行しスクリプトを起動
 2. 翻訳したいテキストをコピー
 3. クリップボードのテキストがGoogle翻訳される
 4. Ctrl + vで任意の箇所に翻訳結果を貼り付ける
 5. コマンドプロンプトにて Ctrl + c でスクリプト終了
