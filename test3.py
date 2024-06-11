from openai import OpenAI

def sub_transcribe_audio1( audio_file_path):
    client = OpenAI()

    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return transcription.text

print(sub_transcribe_audio1("recordings/recording.mp3"))
