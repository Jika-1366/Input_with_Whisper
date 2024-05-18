"""
which_audio_file_is_fastest.py
このスクリプトは、異なるオーディオファイル形式のトランスクリプション速度を比較します。
"""

import requests
import os
import time
import matplotlib.pyplot as plt
from head import get_API_KEY

API_KEY = get_API_KEY()

def transcribe_audio(api_key, audio_file_path):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    with open(audio_file_path, "rb") as audio_file:
        files = {
            "file": (audio_file_path, audio_file, "audio/mpeg"),
        }
        data = {
            "model": "whisper-1",
            "response_format": "json",
            "prompt": "これは日本語の音声ファイルです。",
            "language": "ja",
        }
        response = requests.post(url, headers=headers, files=files, data=data)
        if response.status_code != 200:
            print(f"Error sending request: {response.status_code}")
            return "nothing"
        response_data = response.json()
        transcript = response_data["text"]
        return transcript

# 音声ファイル形式のリスト
audio_formats = ["mp3", "mp4", "mpeg", "m4a", "wav", "webm"]

# 各フォーマットでのトランスクリプション処理時間を記録する辞書
transcription_times = {}

# 元のファイルパス
original_file = "recording.mp3"

# 各フォーマットでトランスクリプションを実行
for format in audio_formats:
    # 変換されたファイルのパス
    converted_file = f"recording.{format}"

    # MP3から他のフォーマットへの変換（ffmpegを使用）
    if format != "mp3":
        conversion_command = f"ffmpeg -i {original_file} {converted_file}"
        conversion_result = os.system(conversion_command)
    else:
        converted_file = original_file
        conversion_result = 0

    # 変換が成功した場合のみトランスクリプションを実行
    if conversion_result == 0:
        # トランスクリプション開始時間
        transcription_start_time = time.time()

        for _ in range(10):
            transcript = transcribe_audio(api_key=API_KEY, audio_file_path=converted_file)
            print(transcript)            
        # トランスクリプション終了時間
        transcription_end_time = time.time()

        # トランスクリプション時間を記録
        transcription_time = transcription_end_time - transcription_start_time
        transcription_times[format] = transcription_time

        # 結果を表示
        print(f"Format: {format}, Transcription Time: {transcription_time:.2f} seconds, Transcript: {transcript}")
    else:
        print(f"Conversion failed for format: {format}")

# ヒストグラムで各フォーマットのトランスクリプション時間を表示し、保存する
if transcription_times:
    plt.figure(figsize=(10, 5))
    plt.bar(transcription_times.keys(), transcription_times.values(), color='blue')
    plt.xlabel('Audio Format')
    plt.ylabel('Transcription Time (seconds)')
    plt.title('Transcription Time Comparison Across Different Audio Formats')
    plt.savefig('transcription_time_histogram.png')  # ヒストグラムをファイルに保存
    plt.show()

    # 最も早く処理が完了したフォーマットを見つける
    fastest_format = min(transcription_times, key=transcription_times.get)
    print(f"Fastest format: {fastest_format} with {transcription_times[fastest_format]:.2f} seconds")
else:
    print("No successful transcriptions.")
