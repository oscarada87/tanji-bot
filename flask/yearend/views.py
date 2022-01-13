from . import yearend
from flask import render_template
from .message import MESSAGE

@yearend.route('/<id>')
def temp(id):
    if id in MESSAGE:
        name = MESSAGE[id][0]
        message = MESSAGE[id][1]
        pic = MESSAGE[id][2]
    else:
        name = ''
        message = []
        pic = ''
    return render_template('yearend.html', name=name, message=message, pic=pic)
