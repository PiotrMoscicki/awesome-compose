#!/usr/bin/env python
import os

from flask import Flask, jsonify, request
from pymongo import MongoClient
import datetime

app = Flask(__name__)

client = MongoClient("mongo:27017")

@app.route('/')
def index():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return "Hello from the MongoDB client!\n"

# endpoint returning available databases
@app.route('/databases')
def databases():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return str(client.list_database_names())

# endpoint for inserting todos into the database using query args to pass the todo
@app.route('/insert', methods=['GET'])
def insert():
    db = client.test
    collection = db.test
    # get key value pairs from query args
    todo = request.args.to_dict()
    # add ingest time to the todo
    todo['ingest_time'] = datetime.datetime.utcnow()
    # make a copy of todo to return
    todo_return = todo.copy()
    # insert the todo into the collection
    collection.insert_one(todo)
    # return args from request
    return jsonify(todo_return)

# endpoint for retrieving todos from the database
@app.route('/get')
def get():
    db = client.test
    collection = db.test
    # find all documents in the collection
    todos = collection.find({},{ "_id": 0 })
    # return the documents
    return jsonify(list(todos))

if __name__ == "__main__":
    # make sure database test is available
    db = client.test
    # make sure collection test is available
    collection = db.test

    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)