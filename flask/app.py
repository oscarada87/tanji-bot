from flask import Flask, request, abort, render_template
from extensions import scheduler, db
from stocks import stock
from tasks import worker

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)

from valuation.gino.crawler import RevenueCrawler
import re

from cloud_image.cloud_image import CloudImage
from stock_lib.stock_info import StockInfo

app = Flask(__name__)
app.config.from_object('instance.config.Config')
db.init_app(app)
scheduler.init_app(app)
scheduler.start()
app.register_blueprint(stock, url_prefix='/stock')

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['LINE_CHANNEL_SECRET'])

@app.route('/')
def home():
    return '(^=◕ᴥ◕=^)'

@app.route("/line/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')