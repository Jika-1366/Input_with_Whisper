import keyboard
import logging
import os
import requests
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
            pass
        
    return API_KEY

def write_japanese(text):
    for char in text:
        keyboard.write(char)
    


def transcribe_audio(API_KEY, audio_file_path):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    
    with open(audio_file_path, "rb") as audio_file:
        files = {
            "file": (audio_file_path, audio_file, "audio/webm"),
        }
        data = {
            "model": "whisper-1",
            "response_format": "json",
            "prompt": "user will speak in English and Japanese."
            
        }
        
        response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code != 200:
        logging_error(f"Error sending request: {response.status_code}")  # エラーメッセージをログファイルに記録
        return "nothing"
    
    response_data = response.json()
    transcript = response_data["text"]
    
    return transcript
