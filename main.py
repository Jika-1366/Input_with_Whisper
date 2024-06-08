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

# 音声録音処理を行うクラス
class AudioRecorder:
    def __init__(self, g, c):
        self.g = g              # グローバル変数クラスのインスタンス
        self.c = c              # 定数クラスのインスタンス
        self.audio = pyaudio.PyAudio()  # PyAudioのインスタンス
        self.recording = False  # 録音状態を示すフラグ

    # 録音を開始する関数
    def start_recording(self):
        self.recording = True
        self.g.frames = []
        print("Recording started...")

    # 録音を停止する関数
    def stop_recording(self):
        self.recording = False
        print("Recording stopped.")

        # 録音データをwavファイルに保存
        filename = "recordings/recording.wav"
        wf = wave.open(filename, "wb")
        wf.setnchannels(self.c.CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(self.c.FORMAT))
        wf.setframerate(self.c.RATE)
        wf.writeframes(b"".join(self.g.frames))
        wf.close()

        # wavファイルをmp4ファイルに変換
        os.system(f"ffmpeg -y -i {filename} {self.c.converted_filename}")
        
        try:        
            self.g.write_switch = True
        except Exception as e:
            logging_error(f"Error during transcription: {e}")
            traceback.print_exc()
            return "error"
        
    # 録音の制御を行う関数
    def toggle_recording(self, event):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    # プログラムを終了する関数
    def exit_program(self, event):
        self.g.running = False

    # 音声録音のメインループ
    def main(self):
        self.g.running = True

        # ストリームを開始
        stream = self.audio.open(format=self.c.FORMAT, channels=self.c.CHANNELS,
                                rate=self.c.RATE, input=True,
                                frames_per_buffer=self.c.CHUNK)

        print("Press the delete key to start/stop recording, esc to exit.")
        
        # メインループ
        try:
            while self.g.running:
                if self.recording:
                    data = stream.read(self.c.CHUNK)
                    self.g.frames.append(data)
        except KeyboardInterrupt:
            pass
        finally:
            # ストリームと音声入力を閉じる
            stream.stop_stream()
            stream.close()
            self.audio.terminate()
            print("Program terminated safely.")

# 文字起こし処理を行うクラス
class TranscriptionHandler:
    def __init__(self, g, c):
        self.g = g              # グローバル変数クラスのインスタンス
        self.c = c              # 定数クラスのインスタンス
        self.running = True      # 文字起こしスレッドの実行状態を示すフラグ

    # 文字起こし処理のメインループ
    def start(self):
        while self.running:
            if self.g.write_switch:
                print("write")
                self.g.transcription = main_transcription(self.c.converted_filename)
                write_japanese(self.g.transcription)
                self.g.write_switch = False
            time.sleep(0.5)
        print("Transcription watcher terminated.")

    # 文字起こしスレッドを終了する関数
    def exit_program(self, event):
        self.running = False

# 音声データを文字起こしする関数
def main_transcription(audio_file_path):
    result = transcribe_audio(API_KEY, audio_file_path)
    if result is None or result == "":
        print("何も聞こえませんでした。")
    else:
        return result


# メイン処理
if __name__ == "__main__":
    try:
        # グローバル変数と定数のインスタンスを作成
        g = GlobalVars()
        c = Constants()

        # AudioRecorder と TranscriptionHandlerのインスタンスを作成
        recorder = AudioRecorder(g, c)
        transcription_handler = TranscriptionHandler(g, c)
        
        # APIキーを取得
        API_KEY = get_API_KEY()

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