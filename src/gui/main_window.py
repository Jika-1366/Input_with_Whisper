import tkinter as tk
from tkinter import ttk
import json
from src.logic.audiorecorder import AudioRecorder


class MainWindow:
    def __init__(self, g):
        self.g = g
        self.root = tk.Tk()
        self.root.title("音声録音 & 文字起こし")
        self.root.attributes('-topmost', True)  # 常に前面に表示

        self.status_canvas = tk.Canvas(self.root, width=100, height=20)  # キャンバスサイズを大きくする
        self.status_canvas.pack()
        self.update_status()

        self.word_entry = ttk.Entry(self.root)
        self.word_entry.pack()

        self.add_button = ttk.Button(self.root, text="単語を追加", command=self.add_word)
        self.add_button.pack()

        self.pause_button = ttk.Button(self.root, text="一時停止", command=self.toggle_pause)
        self.pause_button.pack()

        self.root.mainloop()

    def toggle_pause(self):
        self.g.pause = not self.g.pause
        if self.g.pause:
            self.pause_button.config(text="再開")
        else:
            self.pause_button.config(text="一時停止")

    def update_status(self):
        self.status_canvas.delete("all")  # 既存の描画をクリア
        if self.g.recording == True:
            self.status_canvas.create_oval(5, 5, 15, 15, fill="red")  # 赤丸を描画
        else:
            self.status_canvas.create_oval(5, 5, 15, 15, fill="black")  # 黒丸を描画

        if self.g.pause == True:
            self.status_canvas.create_text(70, 10, text="Pausig now....", anchor="center")  # テキストの位置をずらす

        if not self.g.running:
            print("main_windows終了")
            self.exit_program()
        self.root.after(200, self.update_status)  # 0.2秒ごとに状態を更新

    def exit_program(self):
        self.root.destroy()


    def add_word(self):
        word = self.word_entry.get()
        if word:
            try:
                with open("config/word_list.json", "r+", encoding="utf-8") as f:
                    data = json.load(f)
                    data.append(word)
                    f.seek(0)
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    f.truncate()
                self.word_entry.delete(0, tk.END)  # 入力欄をクリア
                print(f"単語:{word}を追加しました")
            except Exception as e:
                print(f"単語の追加中にエラーが発生しました: {e}")
    def exit_program(self):
        self.root.destroy()


if __name__ == "__main__":
    #window = MainWindow(recorder)
    pass