import datetime

from flask import request, current_app
from flask_login import login_required
from sqlalchemy import or_
from seat.seat_url import seat


@seat.route("/appoint", methods=['POST'])
@login_required
def appoint_seat():
    from model.models import sqlite_db
    from sqlalchemy import text
    sqlite_db.session.execute(text("pragma foreign_keys=ON"))
    try:
        stool_id = request.json["stool_id"]
    except Exception as e:
        return {"error": e.__str__()}
    try:
        # 应该启动“可重复读”级别的隔离事务等级
        from model.models import Appoint
        from flask_login import current_user
        appoint = Appoint.query.filter(
            or_(Appoint.stool_id == stool_id, Appoint.user_id == current_user.get_id())).first()
        if appoint:
            # 如果存在数据，先检查占座有没有过期
            if datetime.datetime.now() > appoint.create_time + datetime.timedelta(
                    seconds=current_app.config['APPOINT_MAX_KEEPING_TIME']):
                # 如果已经过期,将该数据删除
                sqlite_db.session.delete(appoint)
            else:
                return {"error": "Appoint Failed"}
        new_appoint = Appoint(stool_id=stool_id, user_id=current_user.get_id(), create_time=datetime.datetime.now())
        sqlite_db.session.add(new_appoint)
        sqlite_db.session.commit()
    except Exception as e:
        return {"error": e.__str__()}
    return {"error": None}


@seat.route("/cancel_appoint", methods=['POST'])
@login_required
def cancel_appoint():
    from model.models import Appoint
    from flask_login import current_user
    from model.models import sqlite_db
    try:
        del_count = Appoint.query.filter(Appoint.user_id == current_user.get_id()).delete()
        sqlite_db.session.commit()
    except Exception as e:
        return {"error": e.__str__()}
    if del_count > 0:
        return {"error": None}
    else:
        return {"error": "appoint not found"}
