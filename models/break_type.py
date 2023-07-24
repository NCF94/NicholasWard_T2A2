from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf


VALID_BREAK_TYPE = ('reef', 'point', 'beach')

class BreakType(db.Model):
    __tablename__ = 'break_type'
    
    type_id = db.Column(db.Integer, primary_key=True)
    break_type = db.Column(db.String)
    
    # break_id = db.Column(db.Integer, db.ForeignKey('surf_breaks.id'), nullable=False)

    
    surf_break = db.relationship('SurfBreak', back_populates='break_type', uselist=False)
    
class BreakTypeSchema(ma.Schema):
    surf_break = fields.Nested('SurfBreakSchema', exclude=['comments'])

 
    break_type = fields.String(validate=OneOf(VALID_BREAK_TYPE))
    
    class Meta:
        fields = ('type_id','break_type')
        ordered = True
    
break_type_schema = BreakTypeSchema()
break_types_schema = BreakTypeSchema(many=True)
