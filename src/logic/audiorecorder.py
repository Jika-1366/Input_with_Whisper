import pyaudio
import wave
import traceback
import os
from src.logic import head 
from src.logic.head import logging_error

# 音声録音処理を行うクラス
class AudioRecorder:
    def __init__(self, g, c):
        self.g = g              # グローバル変数クラスのインスタンス
        self.c = c              # 定数クラスのインスタンス
        self.audio = pyaudio.PyAudio()  # PyAudioのインスタンス
    

    # 録音を開始する関数
    def start_recording(self):
        self.g.recording = True
        self.g.frames = []
        print("Recording started...")

    # 録音を停止する関数
    def stop_recording(self):
        self.g.recording = False
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
        if self.g.recording:
            self.stop_recording()
        elif not self.g.pause:
            self.start_recording()
        else:
            pass

    # プログラムを終了する関数
    #def exit_program(self, event):
        #self.g.

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
                if self.g.recording:
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