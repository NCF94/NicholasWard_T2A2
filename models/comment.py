from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


#define Comment model for database
class Comment(db.Model):
    __tablename__ = 'comments' #comments table

    #columns in table
    comment_id = db.Column(db.Integer, primary_key=True) #primary key
    user_comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.String)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #foreign key, maps to id column of users table
    break_id = db.Column(db.Integer, db.ForeignKey('surf_breaks.id'), nullable=False) #foreign key, maps to id column of surf_breaks table
    
    #relationships
    user = db.relationship('User', back_populates='comments') 
    surf_break = db.relationship('SurfBreak', back_populates='comments')
    
# Define marshmallow schema    
class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    surf_break = fields.Nested('SurfBreakSchema', exclude=['comments'])

    class Meta:
        fields = ('comment_id', 'user', 'break', 'rating', 'date', 'user', 'user_comment')
        ordered = True#order output as order in 'fields'

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)