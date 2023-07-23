from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.surf_break_controller import surf_break_bp
from controllers.break_type_controller import break_type_bp
from controllers.comment_controller import comments_bp
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)
    
    app.json.sort_keys = False # Orders fields if specified in schema
    
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL") # Gets from .env file
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY") # Gets from .env file
    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400
    
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(surf_break_bp)
    app.register_blueprint(break_type_bp)
    app.register_blueprint(comments_bp)
    
    
    return app
    