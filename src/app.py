import os
from pathlib import Path
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage, ImageSendMessage, 
    TemplateSendMessage, ConfirmTemplate, PostbackAction, PostbackEvent
)

from valuation.gino.crawler import RevenueCrawler
import re

from cloud_image.cloud_image import CloudImage
from stock_lib.stock_info import StockInfo
import json

app = Flask(__name__)
app.config.from_object('instance.config.Config')

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['LINE_CHANNEL_SECRET'])

@app.route('/')
def home():
    return '(^=◕ᴥ◕=^)'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body               
    try:
        print(body)
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # print(event.source)
    user_input = event.message.text
    if '營收' in user_input:
        crawler = RevenueCrawler(re.findall('\d+', user_input)[0])
        msg = crawler.send()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )
    elif any(x in user_input for x in ['喵', '探吉', '咪魯']):
        url = CloudImage().meow()
        msg = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(event.reply_token, msg)
    elif any(x in user_input for x in ['汪']):
        url = CloudImage().wang()
        msg = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(event.reply_token, msg)
    elif '融資' in user_input:
        try:
            stock_info = StockInfo()
            margin_purchase = stock_info.margin_purchase(re.findall('\d+', user_input)[0])
            msg = margin_purchase.message()
        except:
            msg = '查無此股票'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )
    elif '通關密語' in user_input:
        try:
            msg = CloudImage().create_auth(user_input.split()[1], event.source.user_id)
        except Exception as e:
            print(e)
            msg = '密碼錯誤 - 請洽管理員' + str(e)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    if not CloudImage().auth(event.source.user_id):
       return
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    file_path = os.path.join(Path(__file__).parent, './tmp/sent_img.png')
    file = open(file_path, 'w+b')
    for chunk in message_content.iter_content():
        file.write(chunk)
    file.close
    file_public_id = CloudImage().upload(file_path)

    postback_dog_payload = json.dumps({ 'action': 'move_image', 'folder': 'doggy', 'file_public_id': file_public_id, 'tags': ['dog']})
    postback_cat_payload = json.dumps({ 'action': 'move_image', 'folder': 'miru', 'file_public_id': file_public_id, 'tags': ['cat'] })
    which_species_msg = TemplateSendMessage(
        alt_text='奇怪的生物增加了！這是一隻：',
        template=ConfirmTemplate(
            text='奇怪的生物增加了！這是一隻：',
            actions=[
                PostbackAction(
                    label='卯貓',
                    data=postback_cat_payload
                ),
                PostbackAction(
                    label='狗勾',
                    data=postback_dog_payload
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        which_species_msg
    )

@handler.add(PostbackEvent)
def handle_postback_event(event):
    if not CloudImage().auth(event.source.user_id):
      return
    payload = json.loads(event.postback.data)
    if payload['action'] == 'move_image':
      text = CloudImage().move(payload['file_public_id'], payload['folder'], tags=payload['tags'])
      line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(text=text)
      )
    print(event)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
