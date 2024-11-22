from flask import jsonify
import sqlite3
import uuid
import datetime
from ast import literal_eval
from api.db_manager import db_manager

def api_put(id, req):
    dbMan = db_manager()
    methodQuery = "UPDATE piskvorky SET updatedAt = ?, name = ?, difficulty = ?, gameState = ?, board = ? WHERE uuid LIKE ?"
    updatedAt = str(datetime.datetime.now())
    dbMan.cursor.execute(methodQuery, [updatedAt, req["name"], req["difficulty"], None, str(req["board"]), id])
    dbMan.conn.commit()
    methodQuery = "SELECT * FROM piskvorky WHERE uuid LIKE ?"
    dbMan.cursor.execute(methodQuery, [id])
    result = dbMan.cursor.fetchone()
    if result is None: return jsonify({ "response": 404 }), 404
    result["board"] = literal_eval(result["board"])
    dbMan.free()
    return jsonify(result), 200