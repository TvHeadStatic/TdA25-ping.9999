from flask import jsonify
import uuid
import datetime
from ast import literal_eval
from db.db_manager import db_manager
from api.ticktacktoe_functionality import validate_gamestate, has_invalid_char, has_illegal_size, has_bad_actor

def api_put(id, req):
    dbMan = db_manager()
    methodQuery = "UPDATE piskvorky SET updatedAt = %s, name = %s, gameMode = %s, gameState = %s, board = %s WHERE uuid LIKE %s"
    updatedAt = str(datetime.datetime.now())
    if has_invalid_char(req["board"]) or has_illegal_size(req["board"]) or has_bad_actor(req["board"]):
        return jsonify({
            "status": 422
        }), 422
    gameState = validate_gamestate(req["board"])
    dbMan.cursor.execute(methodQuery, [updatedAt, req["name"], req["gameMode"], gameState, str(req["board"]), id])
    dbMan.conn.commit()
    methodQuery = "SELECT * FROM piskvorky WHERE uuid LIKE %s"
    dbMan.cursor.execute(methodQuery, [id])
    result = dbMan.cursor.fetchone()
    if result is None: return jsonify({ "response": 404 }), 404
    result["board"] = literal_eval(result["board"])
    dbMan.free()
    return jsonify(result), 200
