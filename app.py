from flask import Flask,jsonify
from flask_restful import Resource, Api,reqparse
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def hello():
    return "Animal Hospital Backend"

# Create users table and the users database model inhereted by sqlalchemy
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    # Users constructor
    def __init__self(self, id, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email)  # should not need to limit here email is unique in the db

    @classmethod
    def find_by_login(cls, email, password):
        return cls.query.filter_by(email=email, password=password)  # should not need to limit 1 here email is unique

    @classmethod
    def find_by_name(cls, first_name, last_name):
        return cls.query.filter_by(first_name=first_name, last_name=last_name)

    def save_user(self):
        db.session.add(self)
        db.session.commit()  # SQLalchemy will do update or insert depending on weather the row exists or not

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()  # delete the user from the database


class Accounts(Resource):  # add an accounts class as a inherited from Flask-RESTful Resource

    # CRUD-Create
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, help='first name is required.', required=True)
        parser.add_argument('last_name', type=str, help='last name is required.', required=True)
        parser.add_argument('email', type=str, help='email is required.', required=True)
        parser.add_argument('password', type=str, help='password is required', required=True)
        requested_data = parser.parse_args(strict=True)
        New_User = Users(first_name=requested_data['first_name'],
                         last_name=requested_data['last_name'],
                         email=requested_data['email'],
                         password=requested_data['password'])  # create the new user
        if New_User:
            New_User.save_user()  # store the user in the database
            return jsonify({'msg': 'user has been created'}), 200  # return message and ok status code back to client
        else:
            return jsonify({'msg': 'error in entering new user into the databse'}), 400

    # CRUD-Read
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='email is required', required=True)
        parser.add_argument('password', type=str, help='password is required', required=True)
        request_data = parser.parse_args(strict=True)
        # This returns a User object
        Requested_User = Users.find_by_login(email=request_data['email'],password=request_data['password'])
        if Requested_User:
            # Status is ok and user is authenticated
            return jsonify({'msg': 'user is authenticated', 'value': True}), 200
        else:
            # Bad request and unauthorized entry
            return jsonify({'msg': 'user not found', 'value': False}), 401

    # CRUD-Update
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, help='first name is required.', required=True)
        parser.add_argument('last_name', type=str, help='last name is required.', required=True)
        parser.add_argument('email', type=str, help='email is required.', required=True)
        parser.add_argument('password', type=str, help='password is required', required=True)
        requested_data = parser.parse_args(strict=True)
        New_User = Users(first_name=requested_data['first_name'],
                         last_name=requested_data['last_name'],
                         email=requested_data['email'],
                         password=requested_data['password'])  # create the new user
        if New_User:
            New_User.save_user()  # store the user in the database
            return jsonify({'msg': 'user has been created'}), 200  # return message and ok status code back to client
        else:
            return jsonify({'msg': 'error in entering new user into the database'}), 400

    # CRUD-Delete
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str,help='email is required', required=True)
        request_data = parser.parse_args(strict=True)
        User=Users.find_by_email(request_data['email'])
        if User:
            User.delete()
            return jsonify({'msg':'User has been deleted'}), 200
        else:
            return jsonify({'msg':' error in deleting user'}), 400

# Add accounts class to the api end point /accounts
api.add_resource(Accounts, '/api/accounts')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
