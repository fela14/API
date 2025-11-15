from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from sqlalchemy.exc import IntegrityError

# --- Flask and Database setup ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# --- Database Model ---
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

# --- Request Parser ---
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help='Name cannot be blank')
user_args.add_argument('email', type=str, required=True, help='Email cannot be blank')

# --- Output Fields ---
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

# --- Resource: All Users ---
class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        """Get all users"""
        users = UserModel.query.all()
        return users, 200

    def post(self):
        """Create a new user"""
        args = user_args.parse_args()
        new_user = UserModel(name=args['name'], email=args['email'])
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'User with that name or email already exists'}, 400

        return {'message': 'User created successfully'}, 201


# --- Resource: Single User ---
class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        """Get a single user by ID"""
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user, 200

    def patch(self, id):
        """Update user info"""
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")

        user.name = args['name']
        user.email = args['email']
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'That name or email already exists'}, 400

        return {'message': 'User updated successfully'}, 200

    def delete(self, id):
        """Delete a user"""
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")

        db.session.delete(user)
        db.session.commit()
        return {'message': f'User with id {id} deleted successfully'}, 200


# --- Register Resources ---
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

# --- Home Route ---
@app.route('/')
def home():
    return '<h1>Flask REST API with Error Handling</h1>'

# --- Run ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ensures database and tables are created before run
    app.run(debug=True)
