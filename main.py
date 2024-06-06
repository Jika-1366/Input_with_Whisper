"""

このプログラムのセクションでは、ユーザーがdeleteキーを操作して録音を制御します。deleteキーを一回押すと録音が開始され、もう一度押すと録音が停止します。
録音が開始されると、グローバル変数 `recording` は True に設定され、音声データは `frames` というリストに追加されます。
録音が停止すると、`recording` は False に設定され、`frames` に格納された音声データはMP4形式でファイルに出力されます。
最終的に、この録音ファイルは自動的に文字起こしされ、結果が日本語で表示されます。

"""

import keyboard
import pyaudio
import wave
import traceback
import os
import threading
import time
from head import logging_error, write_japanese, get_API_KEY, transcribe_audio

# 録音設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# 録音開始フラグ
recording = False

# 録音データを保存するリスト
frames = []

# PyAudioのインスタンスを作成
audio = pyaudio.PyAudio()

global converted_filename
converted_filename = "recordings/recording.mp4"


global transcription, write_switch, running
running = True
write_switch = False


API_KEY = get_API_KEY()
    
# 録音を開始する関数
def start_recording():
    global recording, frames
    recording = True
    frames = []
    print("Recording started...")

# 録音を停止する関数
def stop_recording():
    global recording
    recording = False
    print("Recording stopped.")

    # 録音データを.wavファイルに保存
    filename = "recordings/recording.wav"
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    

    os.system(f"ffmpeg -y -i {filename} {converted_filename}")
    
    try:
        global write_switch
        
        write_switch = True
        
    except Exception as e:
        logging_error(f"Error during transcription: {e}")  # エラーメッセージをログファイルに記録
        traceback.print_exc()
        return "error"
    
# 録音の制御
def toggle_recording(event):
    global recording
    if recording:
        stop_recording()
    else:
        start_recording()

# shiftキーのイベントリスナーを登録
keyboard.on_press_key("shift", toggle_recording)

def exit_program(event):
    global running  # メインループの実行を制御するグローバル変数
    running = False  # メインループを終了させる

# escキーのイベントリスナーを登録
keyboard.on_press_key("esc", exit_program)


def main_transcription(audio_file_path):
    result = transcribe_audio(API_KEY, audio_file_path)
    if result is None or result == "":
        print("何も聞こえませんでした。")
    else:
        return result


def write_after_recording():
    global running, write_switch, transcription
    while running:  # runningがTrueの間はループを続ける
        if write_switch:
            print("write")
            transcription = main_transcription(converted_filename)
            write_japanese(transcription)
            write_switch = False  # 次の更新のためにリセット
        time.sleep(1)  # 1秒ごとにチェック
    print("Transcription watcher terminated.")  # スレッド終了時にメッセージを表示


def main():
    global running
    running = True

    # ストリームを開始
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Press the delete key to start/stop recording, esc to exit.")
    
    # メインループ
    try:
        while running:
            if recording:
                data = stream.read(CHUNK)
                frames.append(data)
    except KeyboardInterrupt:
        pass
    finally:
        # ストリームと音声入力を閉じる
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Program terminated safely.")

if __name__ == "__main__":
    try:
        # transcription監視スレッドを開始
        watcher_thread = threading.Thread(target=write_after_recording)
        watcher_thread.start()

        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
