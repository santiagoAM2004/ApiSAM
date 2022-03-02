from email import message
from urllib import response
from flask import Flask, request, jsonify, Response, Blueprint
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/apiNoSQL"
mongo = PyMongo(app)

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/', methods =['POST'])
def createUsers():
    userName = request.json['userName']
    password = request.json['password']
    email = request.json['email']

    if userName and password and email:
        hashedPassword = generate_password_hash(password)   
        id = mongo.db.inventory.insert_one(
            {
                
                'userName': userName,
                'password': hashedPassword,
                'email': email
            }
        )
        response = {
            'id': str(id),
            'userName': userName,
            'password': hashedPassword,
            'email': email
        }
    else:
        return notFound()

    return {'message': 'received'}

@bp.route('/', methods =['GET'])
def getUsers():
    users = mongo.db.inventory.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='aplication/json')

@bp.route('/<id>', methods = ['PUT'])
def updateUser(id):
    userName = request.json['userName']
    password = request.json['password']
    email = request.json['email']

    if userName and password and email:
        hashedPassword = generate_password_hash(password)
        updateUser = mongo.db.inventory.update_one({'_id': ObjectId(id)}, {'$set': {
            'userName':userName,
            'password':hashedPassword,
            'email': email
        }})
        response = {'message': 'the object with the id:' + id + 'was updated'}
        return response


@bp.route('/<id>', methods = ['DELETE'])
def deleteUser(id):
    delete = mongo.db.inventory.delete_one({'_id': ObjectId(id)})
    return {'message': 'the object: ' + id + ' was deleted'}

@bp.route('/<id>', methods = ['GET'])
def getUser(id):
    user = mongo.db.inventory.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='aplication/json')

@app.errorhandler(404)
def notFound(error=None):
    response= jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True) 