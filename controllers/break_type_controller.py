from flask import Blueprint, request
from init import db
from models.break_type import BreakType, break_type_schema
from models.surf_break import SurfBreak
from flask_jwt_extended import get_jwt_identity, jwt_required


break_type_bp = Blueprint('break_type', __name__)

# POST method for assigning break type to a surf break
@break_type_bp.route('/', methods=['POST']) #route to POST break types
@jwt_required()
def create_break_type(break_id):
    body_data = break_type_schema.load(request.get_json())
    stmt = db.select(SurfBreak).filter_by(id=break_id) 
    surf_break = db.session.scalar(stmt)
    if surf_break:
        break_type = BreakType(
            # break type input
            break_type=body_data.get('break_type'),
            # pass the model instance to the model field
            surf_break=surf_break 
        )
        #add break type to session
        db.session.add(break_type)
        #commit to db
        db.session.commit()
        #return surf break with updated break type to SurfBreak
        return break_type_schema.dump(break_type), 201
    else:
        #error message if surf break doesnt exist
        return {'error': f'Surf Break not found with id {break_id}'}, 404
    
 #DELETE method for deleteing break type using type_id  
@break_type_bp.route('/<int:type_id>', methods=['DELETE']) #route to DELETE break types
@jwt_required()
def delete_break_type(break_id, type_id):
    stmt = db.select(BreakType).filter_by(type_id=type_id)
    break_type = db.session.scalar(stmt) #break type from db that needs to be deleted
    if break_type:
        db.session.delete(break_type) # delete break type 
        db.session.commit() # commit to db
        # return message saying what break type was deleted
        return {'message': f'Break type {break_type.break_type} deleted successfully'}
    else:
        #error message if break type doesnt exist
        return {'error': f'Break type not found with id {type_id}'}, 404
    
#PUT, PATCH methods for break type    
@break_type_bp.route('/<int:type_id>', methods=['PUT', 'PATCH']) #route to PUT,PATCH break types
@jwt_required()
def update_break_type(break_id, type_id):
    body_data = request.get_json()
    stmt = db.select(BreakType).filter_by(type_id=type_id)
    break_type = db.session.scalar(stmt) # break from database that needs to be updated
    if break_type:
        #updated break type
        break_type.break_type = body_data.get('break_type') or break_type.break_type
        #commit changed to db
        db.session.commit()
        #return changes
        return break_type_schema.dump(break_type)
    else:
        #error message
        return {'error': f'Break type not found with id {type_id}'}, 404