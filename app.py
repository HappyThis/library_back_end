from datetime import datetime

from flask import Flask
from flask_login import login_user, login_required, logout_user
from db.orm_db import sqlite_db
from login.manager import login_manager
import book.query_book
import book.borrow_book
import seat.query_seat
import seat.appoint_seat
from seat.seat_url import seat
from book.book_url import book
from flask import request


def create_app(cfg_file):
    app = Flask(__name__)
    app.config.from_pyfile(cfg_file)
    sqlite_db.init_app(app)
    login_manager.init_app(app)
    app.secret_key = 'yigeluobobale'
    from db.connector import close_db
    app.teardown_appcontext(close_db)
    from db.init_table import init_db_command
    app.cli.add_command(init_db_command)
    from db.init_orm import orm_db_command
    app.cli.add_command(orm_db_command)
    return app


library_app = create_app("configure.py")

library_app.register_blueprint(seat, url_prefix="/seat")
library_app.register_blueprint(book, url_prefix="/book")


# 登录
@library_app.route("/login", methods=["POST"])
def login():
    try:
        login_data = request.json
        user_id = login_data['user_id']
        password = login_data['password']
        from model.models import User
        user = User.get(user_id)
        if not user:
            print("user", user_id, "not found")
        elif user.verify_password(password):
            if not user.activate:
                if datetime.now() > user.time_to_activate:
                    user.activate = True
                    sqlite_db.session.commit()
                else:
                    return {"result": "freeze!"}
            login_user(user)

            return {"result": "Login Successful"}
        else:
            print("password and username mismatch")
    except Exception as e:
        print(e.__str__())
        return {"result": "Login Failed"}
    return {"result": "Login Failed"}


@library_app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return {"result": "Logout Successful"}


if __name__ == '__main__':
    library_app.run()
