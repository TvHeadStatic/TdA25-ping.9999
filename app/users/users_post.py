from flask import Flask, jsonify, session
import uuid
import hashlib
import random
import datetime

from db.db_manager import db_manager

def users_post(req):
    if req["username"] == "" or req["email"] == "" or req["password"] == "":
        return jsonify({ "status": 401, "reason": "1 or more fields are empty" }), 401
    if "@" not in str(req["email"]) and "." not in str(req["email"]) and len(str(req["email"])) < 5:
        print(len(str(req["email"])))
        return jsonify({ "status": 401, "reason": "this 'e-mail address' is... not an e-mail email" }), 401
    if " " in str(req["password"]) and len(str(req["password"])) < 8:
        return jsonify({ "status": 401, "reason": "password should be atleast 8 characters long and contain no whitespace" }), 401
    
    dbMan = db_manager()
    methodQuery = "SELECT * FROM users WHERE email LIKE %s"
    dbMan.cursor.execute(methodQuery, [req["email"]])
    result = dbMan.cursor.fetchone()
    if result != None:
        return jsonify({ "status": 401, "reason": "a user with this e-mail email already exists" }), 401

    methodQuery = "INSERT INTO users(uuid, createdAt, email, username, password, salt, elo, wins, draws, losses) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    salt = hex(random.randrange(0, 2**24))
    newPassword = hashlib.sha256(f"{req['password']}{salt}".encode()).hexdigest()
    dbMan.cursor.execute(methodQuery, [str(uuid.uuid4()), str(datetime.datetime.now()), req["email"], req["username"], newPassword, salt, 0.0, 0, 0, 0])
    dbMan.conn.commit()
    dbMan.free()

    newsessiontoken = str(uuid.uuid4())

    session["user"] = {
        "email": req["email"],
        "username": req["username"],
        "token": newsessiontoken
    }
    return jsonify({
        "email": req["email"],
        "username": req["username"],
        "token": newsessiontoken
    }), 201