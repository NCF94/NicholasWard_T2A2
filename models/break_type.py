from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf


VALID_BREAK_TYPE = ('Reef', 'Point', 'Beach')

class BreakType(db.Model):
    __tablename__ = 'break_type'
    
    id = db.Column(db.Integer, primary_key=True)
    break_type = db.Column(db.String(50))
    
    break_id = db.Column(db.Integer, db.ForeignKey('surf_breaks.id'), nullable=False)

    
    surf_break = db.relationship('SurfBreak', back_populates='break_type', cascade='all, delete')
    
class BreakTypeSchema(ma.Schema):
    surf_break = fields.Nested('SurfBreakSchema', exclude=['comments'])
    
    break_type = fields.String(validate=OneOf(VALID_BREAK_TYPE))
    
    class Meta:
        fields = ('id', 'break_type')
        ordered = True
    
break_type_schema = BreakTypeSchema
break_types_schema = BreakTypeSchema(many=True)
