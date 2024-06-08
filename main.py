"""
このプログラムは、ユーザーがshiftキーで録音を制御し、自動で文字起こしを行うプログラムです。

- deleteキーを一回押すと録音が開始され、もう一度押すと録音が停止します。
- 録音データはwavファイルに一時保存された後、mp4に変換されます。
- 変換されたmp4ファイルは自動的に文字起こしされ、結果が日本語で表示されます。
- escキーを押すとプログラムが終了します。
"""

import keyboard
import pyaudio
import wave
import traceback
import os
import threading
import time

from head import logging_error, write_japanese, get_API_KEY, transcribe_audio
from audiorecorder import AudioRecorder
from transcriptionhandler import TranscriptionHandler

# グローバル変数を格納するクラス
class GlobalVars:
    def __init__(self):
        self.frames = []         # 録音データのフレームを格納するリスト
        self.running = True      # プログラムの実行状態を示すフラグ
        self.write_switch = False  # 文字起こし処理を開始するフラグ
        self.transcription = ""    # 文字起こし結果を格納する変数

# 定数を格納するクラス
class Constants:
    FORMAT = pyaudio.paInt16  # 音声データのフォーマット
    CHANNELS = 1              # 録音チャンネル数
    RATE = 44100             # サンプリングレート
    CHUNK = 1024              # チャンクサイズ
    converted_filename = "recordings/recording.mp4"  # 変換後のファイル名
    # APIキーを取得
    API_KEY = get_API_KEY()

# メイン処理
if __name__ == "__main__":
    try:
        # グローバル変数と定数のインスタンスを作成
        g = GlobalVars()
        c = Constants()

        # AudioRecorder と TranscriptionHandlerのインスタンスを作成
        recorder = AudioRecorder(g, c)
        transcription_handler = TranscriptionHandler(g, c)
        
        # 文字起こしスレッドを開始
        watcher_thread = threading.Thread(target=transcription_handler.start)
        watcher_thread.start()

        # イベントリスナーを登録
        keyboard.on_press_key("shift", recorder.toggle_recording)
        keyboard.on_press_key("esc", recorder.exit_program)
        keyboard.on_press_key("esc", transcription_handler.exit_program)

        # 録音のメインループを開始
        recorder.main()

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()