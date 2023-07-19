from flask import Blueprint, request
from init import db
from datetime import date
from models.surf_break import SurfBreak, surf_break_schema, surf_breaks_schema
from flask_jwt_extended import get_jwt_identity, jwt_required

surf_break_bp = Blueprint('surf_breaks', __name__, url_prefix='/surf_breaks')

@surf_break_bp.route('/')
def get_all_surf_breaks():
    stmt = db.select(SurfBreak).order_by(SurfBreak.name)
    surf_breaks = db.session.scalars(stmt)
    return surf_breaks_schema.dump(surf_breaks)

@surf_break_bp.route('/<int:id>')
def get_one_surf_break(id):
    stmt = db.select(SurfBreak).filter_by(break_id=id)
    surf_break = db.session.scalar(stmt)
    if surf_break:
        return surf_break_schema.dump(surf_break)
    else:
        return {'error': f'Surf break not found with id {id}'}, 404

@surf_break_bp.route('/', methods=['POST'])
@jwt_required()
def create_surf_break():
    body_data = surf_break_schema.load(request.get_json())
    
    surf_break = SurfBreak(
        name=body_data.get('name'),
        location=body_data.get('location'),
        description=body_data.get('description'),
        user_id=get_jwt_identity()
    )
    db.session.add(surf_break)
    db.session.commit()
    
    return surf_break_schema.dump(surf_break), 201

# @surf_break_bp.route('/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_one_surf_break():
    
    
# @surf_break_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
# @jwt_required()
# def update_one_surf_break():
