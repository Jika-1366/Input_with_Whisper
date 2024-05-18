"""
type_speed_test.py
このファイルは、日本語のテキストを速度比較するためのものです。
`write_japanese_original` 関数は与えられたテキストを一度にキーボードに入力します。
`write_japanese_by_char` 関数は与えられたテキストを一文字ずつキーボードに入力します。
`test_write_speed` 関数はこれらの関数の実行時間を計測し、比較結果を出力します。
これにより、どの方法がより効率的かを判断することができます。
"""

import time
import keyboard


def write_japanese_original(text):
    keyboard.write(text)

def write_japanese_by_char(text):
    for char in text:
        keyboard.write(char)

# テストコード
def test_write_speed():
    text = "これは速度比較のためのテキストです。wow" * 10  # テキストを10倍に増やして長くする
    print("5秒後測定開始します...")
    time.sleep(5)
    start_time = time.time()
    write_japanese_original(text)
    original_duration = time.time() - start_time

    start_time = time.time()
    write_japanese_by_char(text)
    by_char_duration = time.time() - start_time

    print(f"Original method duration: {original_duration} seconds")
    print(f"By char method duration: {by_char_duration} seconds")

# テスト関数を実行
test_write_speed()