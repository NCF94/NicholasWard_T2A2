from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST']) #route to register user
def auth_register():
    try:
        # { "name": "User User2", "date_of_birth":"23/04/12", "email": "user2@surfing.com", "password": "user2" }
        body_data = request.get_json()

        # Create a new User model instance from the user info
        user = User()
        user.name = body_data.get('name')
        user.date_of_birth = body_data.get('date_of_birth')
        user.email = body_data.get('email')

        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(
                body_data.get('password')).decode('utf-8')
        # Add user to the session
        db.session.add(user)
        # Commit to add the user to the DB
        db.session.commit()
        # Respond to client
        return user_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            #error if email exists
            return {'error': 'Email address already in use'}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            #error if column missed. eg name isnt input
            return {'error': f'The {err.orig.diag.column_name} is required'}, 409


@auth_bp.route('/login', methods=['POST']) #route to login
def auth_login():
    body_data = request.get_json()
    # Find the user by email address
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(
            user.id), expires_delta=timedelta(days=1))
        #return user authorisation token
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        #error if info is wrong
        return {'error': 'Invalid email or password'}, 401
