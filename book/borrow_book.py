from flask import request
from flask_login import current_user, login_required

from book.book_url import book
from model.models import Borrow


@book.route("/borrow", methods=["POST"])
@login_required
def borrow_book():
    from model.models import sqlite_db
    from sqlalchemy import text
    sqlite_db.session.execute(text("pragma foreign_keys=ON"))
    try:
        json_data = request.json
        book_id = json_data['book_id']
        borrow = Borrow.query.filter_by(book_id=book_id).first()
        if borrow:
            return {"error": "Borrow Failed"}
        else:
            new_appoint = Borrow(book_id=book_id, user_id=current_user.get_id())
            sqlite_db.session.add(new_appoint)
            sqlite_db.session.commit()
    except Exception as e:
        return {"error": e.__str__()}
    return {"error": None}


@book.route("/cancel_borrow", methods=["POST"])
@login_required
def cancel_borrow():
    from model.models import sqlite_db
    try:
        json_data = request.json
        borrow_id = json_data['borrow_id']
        count = Borrow.query.filter_by(id=borrow_id).delete()
        sqlite_db.session.commit()
        if count < 1:
            return {"error": "borrow not found."}
        else:
            return {"error": None}
    except Exception as e:
        return {"error": e.__str__()}
