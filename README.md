# azure_speech

Microsoft Azure の Speech Service を利用して音声認識を行うプログラム。基本的に [音声テキスト変換クイックスタート](https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=windowsinstall&pivots=programming-language-python) のチュートリアルをベースに記述しています。

# Demo

Coming soon...

# Features
 
* 音声ファイルを与えると音声認識結果を出力
    * Azure の Speech Service に Speech SDK を通じてアクセス
* 設定ファイルで以下を設定可能
    * 認識対象言語
    * ディクテーションモードの使用の有無
    * フレーズリストファイルの指定
 
# Requirement
 
* Python3 (Python 3.6.9 にて動作確認)
* Azure Speech SDK (azure-cognitiveservices-speech 1.16.0 にて動作確認)
* Azure アカウントと Speech Service のサブスクリプション
    * 無料アカウントの取得方法については [音声サービスとは - Speech Service を無料で試す](https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech-service/overview#try-the-speech-service-for-free) 参照
 
# Installation
 
Speech SDK は以下でインストール可能です。

```bash
pip install azure-cognitiveservices-speech
```
 
# Usage

本リポジトリをクローンし、config.json をサンプルからコピーして作成します。

```bash
git clone https://github.com/yoshimura-shunji/azure_speech.git
cd python
cp config.json.sample config.json
```

config.json の subscription には Azure のサブスクリプションキーを、また region にはサービスを使用するリージョンを指定してください。またディクテーションモード (音声構成インスタンスが句読点など文構造の単語の表現を解釈するモード、詳細は [音声サービスとは - Speech Service を無料で試す](https://docs.microsoft.com/ja-jp/azure/cognitive-services/speech-service/overview#try-the-speech-service-for-free) の「ディクテーションモード」の項を参照) を有効にするには dictation\_mode を true に設定し、さらに認識精度向上のためのフレーズリストを使用する場合は phrase\_list にそのファイル名を指定してください。

フレーズリストには phrase\_list.txt.sample のように、認識させたいフレーズや単語を改行区切りで羅列してください。

入力可能な音声ファイルはサンプリングレート 16kHz の WAV フォーマットです。他の形式のファイルについては何らかのツールで変換してください。

以上の準備が整ったら、以下のコマンドで認識が可能です (入力音声ファイルを input.wav、結果を書き込むファイルを output.txt とします)。

```bash
python3 speech2text.py input.wav output.txt
```

# Note
 
特になし。
 
# Author
  
* 作成者: 吉村俊司 YOSHIMURA Shunji
* E-mail: yoshimura.shunji@gmail.com
 
# License
 
"azure_speech" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
