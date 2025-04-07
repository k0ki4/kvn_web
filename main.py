from flask import Flask
from data import db_session
from main_wb.main_page import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'k0ki4_176'


def start():
    db_session.global_init("db/live.db")
    app.register_blueprint(main)
    app.run(debug=True)


if __name__ == '__main__':
    start()