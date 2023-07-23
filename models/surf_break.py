from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf


class SurfBreak(db.Model):
    __tablename__ = "surf_breaks"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # type_id = db.Column(db.Integer, db.ForeignKey('break_type.id'), nullable=False)
    
    user = db.relationship('User', back_populates='surf_break')
    comments = db.relationship('Comment', back_populates='surf_break', cascade='all, delete')
    break_type = db.relationship('BreakType', back_populates='surf_break', uselist=False)
    
class SurfBreakSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('CommentSchema'), exclude=['surf_break'])
    break_type = fields.List(fields.Nested('BreakTypeSchema'), exclude=['surf_break'])
    
    name = fields.String(required=True, validate=And(
        Length(min=2, error='Surf Break name must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, spaces and numbers are allowed')
    ))
    
    class Meta:
        fields = ('id', 'name', 'location', 'description', 'user', 'comments')
        ordered = True
        
surf_break_schema = SurfBreakSchema()
surf_breaks_schema = SurfBreakSchema(many=True)