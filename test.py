import requests

SERVER_URL = 'http://cool-hiji-1700.schoolbus.jp/programs/whisper/upload.php'

def transcribe_audio_from_server(audio_file_path: str) -> str:
    """音声ファイルをサーバーに送信し、文字起こし結果を取得する。

    Args:
        audio_file_path (str): 音声ファイルのパス

    Returns:
        str: 文字起こし結果
    """
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio_file': audio_file}
        response = requests.post(SERVER_URL, files=files)
    return response.text

if __name__ == "__main__":
    audio_file_path = "recordings/recording.mp4"
    transcription_result = transcribe_audio_from_server(audio_file_path)
    print(f"文字起こし結果: {transcription_result}")
