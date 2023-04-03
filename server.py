from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
#import pyrebase

# firebaseConfig = {
#   "apiKey": "AIzaSyAvW8qNNaxV6o6wMFo2rKBJP9cEAIKjcwo",
#   "authDomain": "sigma-message.firebaseapp.com",
#   "databaseURL": "https://sigma-message-default-rtdb.firebaseio.com",
#   "projectId": "sigma-message",
#   "databaseUrl": "https://sigma-message-default-rtdb.firebaseio.com/",
#   "storageBucket": "sigma-message.appspot.com",
#   "messagingSenderId": "308857749412",
#   "appId": "1:308857749412:web:fb7ae8c621de8d0fb70b31",
#   "measurementId": "G-X7T145C79G"
# }
#
# firebase = pyrebase.initialize_app(firebaseConfig)
# db = firebase.database()

app = Flask(__name__)
api = Api()

users = {
    1: {"login": "fucker", "id": 15},
    2: {"login": "sucker", "id": 10}
}

parser = reqparse.RequestParser()
parser.add_argument("login", type=str)
parser.add_argument("id", type=int)


class Main(Resource):
    def get(self, user_id):
        if user_id == 0:
            return users
        else:
            return users[user_id]

    def delete(self, user_id):
        del users[user_id]
        return

    def post(self, user_id):
        users[user_id] = parser.parse_args()
        return

    def put(self, user_id):
        users[user_id] = parser.parse_args()
        return


api.add_resource(Main, "/api/users/<int:user_id>")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="127.0.0.1")