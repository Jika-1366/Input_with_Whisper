import pyautogui
import time
import pyperclip

def cut_and_display():
    # 'space' キーを押す 
    pyautogui.press('space')
    # シフトキーを押しながら左矢印キーを押して選択
    pyautogui.keyDown('shift')
    pyautogui.press('left')
    pyautogui.keyUp('shift')
    # 選択したテキストを切り取る
    pyautogui.hotkey('ctrl', 'x')
    # クリップボードからテキストを取得
    cut_text = pyperclip.paste()
    # 切り取ったテキストが半角かどうかを判定
    if cut_text.isascii():
        print("切り取ったテキストは半角です。")
    else:
        print("切り取ったテキストに全角文字が含まれています。")

# 関数を実行
cut_and_display()
