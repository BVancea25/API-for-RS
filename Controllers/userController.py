from flask import request,jsonify
from Config.db import database

def add_user():
    req=request.get_json()
    if 'name' not in req :
        return jsonify({'message':'Missing name'}),400
    if 'id' not in req :
        return jsonify({'message':'Missing id'}),400
    if(database.check_user(req['id'])==-1):
        return jsonify({'message':'User already exists'}),403
    try:
        database.create_node("User",{"name":req['name'], "id":req['id'],"profile":[]})
        return jsonify({'message':'User added'}),201
    except Exception as e:
        print(f"An error occurred while creating the node: {e}")
        return jsonify({'message':'User not added'}),401

