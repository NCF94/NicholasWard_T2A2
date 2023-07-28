from flask import Blueprint, request
from init import db
from models.break_type import BreakType, break_type_schema
from models.surf_break import SurfBreak
from flask_jwt_extended import get_jwt_identity, jwt_required


break_type_bp = Blueprint('break_type', __name__)

@break_type_bp.route('/', methods=['POST'])
@jwt_required()
def create_break_type(break_id):
    body_data = break_type_schema.load(request.get_json())
    stmt = db.select(SurfBreak).filter_by(id=break_id) 
    surf_break = db.session.scalar(stmt)
    if surf_break:
        break_type = BreakType(
            break_type=body_data.get('break_type'),
            surf_break=surf_break # pass the model instance to the model field
        )

        db.session.add(break_type)
        db.session.commit()
        return break_type_schema.dump(break_type), 201
    else:
        return {'error': f'Surf Break not found with id {break_id}'}, 404
    
@break_type_bp.route('/<int:type_id>', methods=['DELETE'])
@jwt_required()
def delete_break_type(break_id, type_id):
    stmt = db.select(BreakType).filter_by(type_id=type_id)
    break_type = db.session.scalar(stmt)
    if break_type:
        db.session.delete(break_type)
        db.session.commit()
        return {'message': f'Break type {break_type.break_type} deleted successfully'}
    else:
        return {'error': f'Break type not found with id {type_id}'}, 404
    
@break_type_bp.route('/<int:type_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_break_type(break_id, type_id):
    body_data = request.get_json()
    stmt = db.select(BreakType).filter_by(id=type_id)
    break_type = db.session.scalar(stmt) # break from database that needs to be updated
    if break_type:
        break_type.break_type = body_data.get('break_type') or break_type.break_type
        db.session.commit()
        return break_type_schema.dump(break_type)
    else:
        return {'error': f'Break type not found with id {type_id}'}, 404