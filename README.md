# Whisper_Typing
Enable voice input with Whisper anywhere on your PC (with a few seconds of lag)

まだ以下の説明は準備段階です。

WhisperTypingは、Whisper APIを使用して音声を録音し、その音声をテキストに変換し、Pythonを使用して変換されたテキストを自動的に入力するプロジェクトです。windows向けです。


##機能
音声録音: 音声を録音し、.wavファイルとして保存します。
文字起こし: .wavファイルを.mp4に変換し、Whisper APIに送信して文字起こしを行います。
自動入力: Pythonを使用して、文字起こしされたテキストをキーボードライブラリで入力します。


##前提条件
*Python 3以降
*OPENAI API KEY

##準備
###準備1（インストール）
'''
git clone https://github.com/your-username/WhisperTyping.git
cd WhisperTyping
'''

依存関係
'''
pip install pyaudio 
'''
など


###準備2(環境変数の登録)
環境変数にOpenAI APIキーを設定します:
export OPENAI_API_KEY='your_openai_api_key'


##使い方
#準備
1. プログラムを起動する前に、テキストを入力したい場所をクリックして入力待ち状態にします。
2. Main.pyを起動

#ショートカットキーによる使用(windows)
プログラムをキーボードショートカットで起動するのが便利です。以下の手順で設定できます:
1. Pythonプログラムを起動するショートカットを作成します。
2. ショートカットのプロパティを開き、「ショートカットキー」欄に Shift + Ctrl + V と入力します（VはVoiceのVです）。

##操作方法
入力待ち状態にする場所をクリックしてから、キーボードショートカット（例: Shift + Ctrl + V）でプログラムを起動します。
Deleteキーで録音を開始します。
再度Deleteキーを押して録音を停止します。停止後、文字起こしされたテキストが自動で入力されます。
再度録音したい場合は、Deleteキーを再度押して録音を開始・停止します。
注意点
短い録音の場合、Deleteキーを2回押すことで録音を停止し、すぐに文字起こしと入力を行うことができます。
ファイルの説明
Main.py: 音声録音、文字起こし、入力を管理する中央スクリプト。
Head.py: Main.pyで使用されるヘルパー関数が含まれています。
コミュニティ募集
オープンAIのDISPA機能のように、固有名詞や特殊な単語を登録して聞き取り精度を向上させる機能を開発していただける方を募集しています。興味のある方はご連絡ください。

貢献
貢献は歓迎します！プルリクエストを提出してください。

ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。
