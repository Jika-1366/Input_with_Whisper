import keyboard
import logging
import os
import requests
import pyautogui
import pyperclip

from dotenv import load_dotenv

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
    """日本語を入力する場合、英数字モードである必要があるので、泥臭く確認"""
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
        for char in text:
            keyboard.write(char)

def transcribe_audio(API_KEY, audio_file_path):
    if API_KEY:
        sub_transcribe_audio1(API_KEY, audio_file_path)
    else:
        sub_transcribe_audio2()

def sub_transcribe_audio1(API_KEY, audio_file_path):
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
            "prompt": "Input with Whisper, Open Interpreter, Dキャン、大輝(ひろき)、清川 大輝(きよかわ ひろき)というサッカー選手がいます, 統合開発環境, Cursor, Gemini, Claude" #By adding proper nouns, Whisper-1 recognize the sound of them.
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
    audio_file_path = "recordings/recording.mp4"
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio_file': audio_file}
        response = requests.post(SERVER_URL, files=files)
    return response.text
