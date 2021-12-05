from flask import Blueprint

# 定義
stock = Blueprint('stock', __name__)

# 關聯
from . import views