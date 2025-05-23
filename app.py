from flask import Flask, request, abort
import os
import json
import requests

app = Flask(__name__)

# あなたのチャンネルアクセストークン（LINE Developersで発行したものに置き換えてください）
ACCESS_TOKEN = "+LC0heqsGGGxyIW0jWl/r1vOZGba4qk1tJjr2Zzb/ABB1DEbUR434mn54jyc1FTdUdcjUTqyDtz0hipkKNmSfDlU8TZiRhqCIpCuJ3JrqdWqwtNRCLIw6rHfczb90HnIAUAeTQJU6kOIRzhNH3KFLwdB04t89/1O/w1cDnyilFU="

# ルートURL確認用
@app.route('/')
def home():
    return "Flask Webhook Ready!"

# LINEからのWebhook受信
@app.route('/callback', methods=['POST'])
def webhook():
    try:
        body = request.json
        print("受信:", json.dumps(body, indent=2))

        # 応答送信（テスト）
        reply_token = body['events'][0]['replyToken']
        send_text_message(reply_token, "メッセージ受け取りました！")

        return 'OK', 200
    except Exception as e:
        print("エラー:", e)
        abort(400)

# LINEへの返信メッセージ送信関数
def send_text_message(reply_token, text):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    data = {
        'replyToken': reply_token,
        'messages': [{
            'type': 'text',
            'text': text
        }]
    }
    res = requests.post(url, headers=headers, data=json.dumps(data))
    print("送信結果:", res.status_code, res.text)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
