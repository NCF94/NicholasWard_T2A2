from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    user_comment = db.Column(db.Text)
    rating = db.Column(db.Interger)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    break_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)

    user = db.relationship('User', back_populates='comments') # {id: 1, name: "User 1"}
    surf_breaks = db.relationship('SurfBreak', back_populates='comments', cascade='all, delete')


class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    surf_break = fields.Nested('SurfBreakSchema', exclude=['comments'])

    class Meta:
        fields = ('comment_id', 'user', 'break', 'rating', 'user_comment')
        ordered = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)