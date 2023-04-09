from datetime import datetime, timedelta

from flask import current_app
from flask_login import login_required, current_user

from model.models import sqlite_db
from seat.seat_url import seat


@seat.route("/query_layer", methods=['GET'])
@login_required
def query_layer():
    from model.models import Layer
    try:
        layers = Layer.query.all()
        sqlite_db.session.commit()
        layer_result = {}
        for layer in layers:
            layer_result[layer.id] = layer.layer_name
        result = {"error": None, "layer": layer_result}
    except Exception as e:
        result = {"error": e.__str__(), "layers": None}
    return result


@seat.route("/query_part_by_layer/<layer_id>", methods=['GET'])
@login_required
def query_part_by_layer(layer_id):
    from model.models import Part
    try:
        parts = Part.query.filter_by(layer_id=layer_id).all()
        sqlite_db.session.commit()
        part_result = {}
        for part in parts:
            part_result[part.id] = part.part_name
        result = {"error": None, "parts": part_result}
    except Exception as e:
        result = {"error": e.__str__(), "parts": None}
    return result


@seat.route("/query_desk_by_part/<part_id>", methods=['GET'])
@login_required
def query_desk_by_part(part_id):
    try:
        from model.models import Desk
        desks = Desk.query.filter_by(part_id=part_id).all()
        sqlite_db.session.commit()
        desk_result = {}
        for desk in desks:
            desk_result[desk.id] = desk.desk_name
        result = {"error": None, "desks": desk_result}

    except Exception as e:
        result = {"error": e.__str__(), "desks": None}
    return result


@seat.route("/query_stool_by_desk/<desk_id>", methods=['GET'])
@login_required
def query_stool_by_desk(desk_id):
    try:
        from model.models import Stool
        stools = Stool.query.filter_by(desk_id=desk_id).all()
        sqlite_db.session.commit()
        stool_result = {}
        for stool in stools:
            stool_result[stool.id] = stool.stool_name
        result = {"error": None, "stools": stool_result}

    except Exception as e:
        result = {"error": e.__str__(), "stools": None}
    return result


@seat.route("/query_position_by_stool/<stool_id>", methods=['GET'])
@login_required
def query_position_by_stool(stool_id):
    # 手动查询
    try:
        from model.models import Stool, Desk, Part, Layer
        stool = Stool.query.get(stool_id)
        if not stool:
            result = {"error": None, "position": None}
        else:
            desk_id = stool.desk_id
            desk = Desk.query.get(desk_id)
            part_id = desk.part_id
            part = Part.query.get(part_id)
            layer_id = part.layer_id
            layer = Layer.query.get(layer_id)
            result = {"error": None, "position": [layer.layer_name, part.part_name, desk.desk_name, stool.stool_name]}
    except Exception as e:
        result = {"error": e.__str__(), "position": None}
    return result


@seat.route("/query_appoint_by_user", methods=['GET'])
@login_required
def query_appoint_by_user():
    try:
        from model.models import Appoint
        appoint = Appoint.query.filter_by(user_id=current_user.get_id()).first()
        if not appoint:
            result = {"error": None, "appoint": None}
        else:
            result = {"error": None, "appoint": [appoint.stool_id, int(appoint.create_time.timestamp())]}
    except Exception as e:
        result = {"error": e.__str__(), "appoint": None}
    return result


@seat.route("/query_appoint_by_stool/<stool_id>", methods=['GET'])
@login_required
def query_appoint_by_stool(stool_id):
    try:
        from model.models import Appoint
        appoint = Appoint.query.filter_by(stool_id=stool_id).first()
        if not appoint:
            result = {"error": None, "appointed": False}
        else:
            # 如果存在数据，先检查占座有没有过期
            if datetime.now() > appoint.create_time + timedelta(
                    seconds=current_app.config['APPOINT_MAX_KEEPING_TIME']):
                # 如果已经过期,将该数据删除
                sqlite_db.session.delete(appoint)
                sqlite_db.session.commit()
                result = {"error": None, "appointed": False}
            else:
                result = {"error": None, "appointed": True}
    except Exception as e:
        result = {"error": e.__str__(), "appointed": None}
    return result
