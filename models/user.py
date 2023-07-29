from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


#Define User model for database
class User(db.Model):
    __tablename__ = 'users' #users table

    #columns in table
    id = db.Column(db.Integer, primary_key=True) #primary key
    name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    #relationships
    surf_break = db.relationship('SurfBreak', back_populates='user') 
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete') 
    
# Define marshmallow schema    
class UserSchema(ma.Schema):
    surf_breaks = fields.List(fields.Nested('SurfBreakSchema', exclude=['user']))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))

    name = fields.String(required=True, validate=And(
        Length(min=2, error='Name must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, spaces and numbers are allowed')
    ))
    class Meta:
        fields = ('id', 'name', 'date_of_birth', 'email', 'password', 'is_admin')
        ordered = True#order output as order in 'fields'
    
user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])