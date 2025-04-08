from __init import app
from data import db_session
from main_wb.main_page import main
from reg_form.register_group_form import register_form
from flask_talisman import Talisman


def start():
    db_session.global_init("db/live.db")
    app.register_blueprint(main)
    app.register_blueprint(register_form)
    app.run(debug=True)


if __name__ == '__main__':
    start()