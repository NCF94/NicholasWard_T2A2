from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

#define SurfBreak model for database
class SurfBreak(db.Model):
    __tablename__ = "surf_breaks" #surf breaks table
    
    #columns in table
    id = db.Column(db.Integer, primary_key=True)  #Primary Key
    name = db.Column(db.String, nullable=False) #cant be empty
    location = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #foreign key, maps to id column of users table
    break_type_id = db.Column(db.Integer, db.ForeignKey('break_type.type_id')) #foreign key, maps to type_id column of break_type table
    
    #relationships
    user = db.relationship('User', back_populates='surf_break') 
    comments = db.relationship('Comment', back_populates='surf_break', cascade = 'all, delete') 
    break_type = db.relationship('BreakType', back_populates='surf_break',cascade = 'all, delete', uselist=False) 
    
# Define marshmallow schema    
class SurfBreakSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email']) # only retrieves name and email atributes from UserSchema
    comments = fields.List(fields.Nested('CommentSchema'), exclude=['surf_break'])# retrieves all attributes from CommentSchema except surf_break
    break_type = fields.Nested('BreakTypeSchema')
    
    # validates name field, requires atleast 2 characters, only letters numbers and spaces allowed
    name = fields.String(required=True, validate=And(
        Length(min=2, error='Surf Break name must be at least 2 characters long'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, spaces and numbers are allowed')
    ))
    
    class Meta:
        fields = ('id', 'name', 'location', 'description', 'user', 'comments', 'break_type')
        ordered = True#order output as order in 'fields'
        
surf_break_schema = SurfBreakSchema()
surf_breaks_schema = SurfBreakSchema(many=True)