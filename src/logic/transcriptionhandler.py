import time
from head import main_transcription, write_japanese

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
                self.g.transcription = main_transcription(self.c)
                write_japanese(self.g.transcription)
                self.g.write_switch = False
            time.sleep(0.5)
        print("Transcription watcher terminated.")


    # 文字起こしスレッドを終了する関数
    def exit_program(self, event):
        self.running = False

    