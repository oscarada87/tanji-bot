import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'), os.getenv('POSTGRES_HOST'), os.getenv('POSTGRES_PORT'), os.getenv('POSTGRES_DB'))
    JSON_AS_ASCII = False
    FINMIND_TOKEN = os.getenv('FINMIND_TOKEN')
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
    GOOGLE_CHROME_BIN = os.getenv('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
    SCHEDULER_TIMEZONE = "Asia/Taipei"
    ENV = os.getenv('ENVIRONMENT')
    if os.getenv('ENVIRONMENT') == 'development':
        SCHEDULER_API_ENABLED = True
        DEVELOPMENT = True
        DEBUG = True 
        SQLALCHEMY_TRACK_MODIFICATIONS = True   