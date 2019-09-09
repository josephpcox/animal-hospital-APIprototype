from flask import Flask,jsonify
from flask_restful import Resource, Api,reqparse
from flask_sqlalchemy import SQLAlchemy
from tests import test_accounts
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


# Create users table to hold the users of the software
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    # Users constructor
    def __init__self(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def get_json(self):
        return {'id': self.id, 'first name': self.first_name, 'last name': self.last_name, 'email': self.email,
                'password': self.password}

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
        return

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()  # delete the user from the database
        return


#  Every owner could have more then one animal, and evey animal could have more than one owner associated with it
class Owners(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    animal_id = db.Column(db.Integer, db.Forgienkey('animals.id'))
    animals = db.relationship('Animals', lazey='dynamic') # This will generate objects from the database dynamically

    def __init__(self,first_name,last_name,email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def get_json(self):
        return {'first name': self.first_name, 'last name': self.last_name, 'email': self.email, 'phone': self.phone}

    def get_animals_json(self):
        return {'last name': self.last_name, 'first name': self.first_name, 'email': self.email, 'phone': self.phone,
                'animals': [animal.json() for animals in self.animals]}

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email)

    @classmethod
    def find_by_name(cls, firs_name, last_name):
        return cls.query.filter_by(firs_name=firs_name, last_name=last_name)

    def save_owner(self):
        db.session.add(self)
        db.session.commit()  # store the owner in the database
        return

    def delete_owner(self):
        db.session.delete(self)
        db.session.commit()  # delete the owner from the database
        return


class Animals(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal_name = db.Column(db.String(50), nullable=False)
    nights_stayed = db.Columen(db.Integer, nullable=False)
    free_nights = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.Forigenkey ('owners.id'))
    owners = db.relationship('Owners', lazy='dynamic')

    def __init__(self, animal_name):
        self.animal_name = animal_name
        self.nights_stayed = 0
        self.free_nights = 0

    @classmethod
    def find_by_name(cls,first_name):
        return cls.query.filter_by(first_name = first_name)

    def get_json(self):
        return {'animal name': self.animal_name, 'nights stayed': self.nights_stayed, 'free nights': self.free_nights}

    def get_owners_json(self):
        return {'animal name': self.animal_name, 'owners:': [owner.get_json() for owner in self.owners]}

    def save_animal(self):
        db.session.add(self)
        db.session.commit()
        return

    def delete_animal(self):
        db.session.delete(self)
        db.session.commit()
        return

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
            msg = jsonify({'msg': 'user has been created'})  # return message and ok status code back to client
            status = 200
        else:
            msg = jsonify({'msg': 'error in entering new user into the databse'})
            status = 400
        return status

    # CRUD-Read
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='email is required', required=True)
        parser.add_argument('password', type=str, help='password is required', required=True)
        request_data = parser.parse_args(strict=True)
        # This returns a User object
        requested_user = Users.find_by_login(email=request_data['email'],password=request_data['password'])
        if requested_user:
            # Status is ok and user is authenticated
            msg = jsonify({'msg': 'user is authenticated', 'value': True})
            status = 200
        else:
            # Bad request and unauthorized entry
            msg=jsonify({'msg': 'user not found', 'value': False})
            status = 401
        return status

    # CRUD-Update
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, help='first name is required.', required=True)
        parser.add_argument('last_name', type=str, help='last name is required.', required=True)
        parser.add_argument('email', type=str, help='email is required.', required=True)
        parser.add_argument('password', type=str, help='password is required', required=True)
        requested_data = parser.parse_args(strict=True)
        update_user = Users.find_by_email(requested_data['email']).first()
        update_user.first_name = requested_data['first_name']
        update_user.last_name = requested_data['last_name']
        update_user.password = requested_data['password']

        if update_user:
            update_user.save_user()  # store the user in the database
            msg = jsonify({'msg': 'user has been created'})  # return message and ok status code back to client
            status = 200
        else:
            msg = jsonify({'msg': 'error in entering new user into the database'})
            status = 400

        return status

    # CRUD-Delete
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='email is required', required=True)
        request_data = parser.parse_args(strict=True)
        User = Users.find_by_email(request_data['email']).first()
        if User:
            User.delete_user()
            msg = 'User has been deleted'
            status = 200
        else:
            msg = 'error in deleting user'
            status = 400

        return status


# Add accounts class to the api end point /accounts
api.add_resource(Accounts, '/api/accounts')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))

    # run the unit tests on start using static methods from test classes
    test_accounts.test_post()
    test_accounts.test_put()
    test_accounts.test_delete()


