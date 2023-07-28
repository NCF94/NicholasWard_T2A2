from init import db, ma
from marshmallow import fields, validates, validate
from marshmallow.exceptions import ValidationError
from marshmallow.validate import OneOf


VALID_BREAK_TYPE = ('reef', 'point', 'beach') #accepted break types

class BreakType(db.Model):
    __tablename__ = 'break_type' #breaktype table
    
    #columns in table
    type_id = db.Column(db.Integer, primary_key=True) # PRimary Key
    break_type = db.Column(db.String)

    # relationships
    surf_break = db.relationship('SurfBreak', back_populates='break_type', uselist=False) 
    
class BreakTypeSchema(ma.Schema):
    surf_break = fields.Nested('SurfBreakSchema', exclude=['comments'])

        # validates the break type entered is one of reef, point or beach
    break_type = fields.String(required=True, validate = OneOf(VALID_BREAK_TYPE, error='break type must be one of reef, point or beach'))
    
    class Meta:
        fields = ('type_id','break_type')
        ordered = True
    
break_type_schema = BreakTypeSchema()
break_types_schema = BreakTypeSchema(many=True)
