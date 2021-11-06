from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from stocks import stock
from flask_migrate import Migrate
import twstock


# initialization
twstock.__update_codes()
db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object('instance.config.DevelopmentConfig')
db.init_app(app)
app.register_blueprint(stock, url_prefix='/stock')

# migration
migrate = Migrate(app, db)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p><br>{}".format(app.url_map)


if __name__ == '__main__':
    app.run()
