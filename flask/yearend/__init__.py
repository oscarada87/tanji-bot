from flask import Blueprint

# 定義
yearend = Blueprint('yearend', __name__)

# 關聯
from . import views