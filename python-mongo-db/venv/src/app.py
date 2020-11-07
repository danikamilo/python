from flask import Flask, request, jsonify, Response
from  flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/pythonmongodb'
mongo = PyMongo(app) 

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    hashed_password = generate_password_hash(password)
    if username and email and password:
        id = mongo.db.users.insert(
            {"username":username,"password":hashed_password,"email":email}
        )
        response = {
            'id' : str(id),
            'username' : username,
            'password' : password,
            'email' : email
        }
        return response
    else:
        response = {'message': 'received'}
        return response

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id' : ObjectId(id)})
    response = jsonify({'message' : 'User ' + id + ' was delete succesfully'})
    return response

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id' : ObjectId(id)}, {'$set': {
            'username' : username,
            'password' : hashed_password,
            'email' : email
        }})
        response = jsonify({'message' : 'User ' +id+ ' was updated sucessfully'})
        return response

@app.errorhandler(404)
def not_found(error=None):
    message = jsonify({
        "message" : "Recurso no encontrado" + request.url,
        "status"  : 404 
    }) 
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)