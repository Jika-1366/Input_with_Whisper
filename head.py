import keyboard
import logging
import os
import requests
import pyautogui
import pyperclip
import json
from dotenv import load_dotenv
import time

# ロギング設定
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def logging_error(error_message):
    """エラーメッセージをログファイルに記録する関数"""
    logging.error(error_message)


def get_API_KEY():
    load_dotenv()
    API_KEY = os.getenv('OPENAI_API_KEY')
    if API_KEY:
        print("環境変数からのOpenAI APIキーの取得ができました。")
        print(API_KEY)
    else:
        print(f"環境変数からAPIキーの取得に失敗しました。\n")
        try:
            print("OPENAI_API_KEY = {API_KEY}")
        except:
            print("環境変数登録されていません。")
            return None
        
    return API_KEY


def write_japanese(text):
    """日本語を入力する場合、英数字モードである必要があるので、泥臭く確認
    現在のクリップボードを書き換えてしまうので、残しておいてもいいかもしれない。"""
    def change_to_alphab_mode():
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
            pass
        else:
            print("ひらがな全角入力だと判断しましたので、英字半角入力に切り替えます。")
            pyautogui.press('kanji')

    change_to_alphab_mode()
    if text and isinstance(text, str):
        for char in text: #この書き方の方が速かった。
            keyboard.write(char)

# JSONファイルから単語リストを読み込む関数  
def load_word_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        word_list = json.load(file)
    return word_list


# 音声データを文字起こしする関数
def main_transcription(c):
    audio_file_path = c.converted_filename
    result = transcribe_audio(c.API_KEY, audio_file_path, c.word_list)
    if result is None or result == "":
        print("何も聞こえませんでした。")
    else:
        return result
def transcribe_audio(API_KEY, audio_file_path, word_list):
    if API_KEY:
        return sub_transcribe_audio1(API_KEY, audio_file_path, word_list)
    else:
        return sub_transcribe_audio2(audio_file_path)
def sub_transcribe_audio1(API_KEY, audio_file_path, word_list):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    
    with open(audio_file_path, "rb") as audio_file:
        files = {
            "file": (audio_file_path, audio_file, "audio/mp4"),
        }
        data = {
            "model": "whisper-1",
            "response_format": "json",
            "prompt": " ".join(word_list) #By adding proper nouns, Whisper-1 recognize the sound of them.
        }
        
        
        response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code != 200:
        logging_error(f"Error sending request: {response.status_code}")  # エラーメッセージをログファイルに記録
        return "none"
    
    response_data = response.json()
    transcript = response_data["text"]
    
    return transcript

def sub_transcribe_audio2(audio_file_path):
    """音声ファイルをサーバーに送信し、文字起こし結果を取得する。
    Args:
        audio_file_path (str): 音声ファイルのパス
    Returns:
        str: 文字起こし結果
    """
    SERVER_URL = 'http://cool-hiji-1700.schoolbus.jp/programs/whisper/upload.php'
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio_file': audio_file}
        response = requests.post(SERVER_URL, files=files)
    return response.text

