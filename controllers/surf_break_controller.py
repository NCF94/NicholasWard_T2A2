from flask import Blueprint, request
from init import db
from datetime import date
from models.surf_break import SurfBreak, surf_break_schema, surf_breaks_schema
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.comment_controller import comments_bp
from controllers.break_type_controller import break_type_bp
from models.user import User
import functools

surf_break_bp = Blueprint('surf_breaks', __name__, url_prefix='/surf_breaks')
surf_break_bp.register_blueprint(comments_bp, url_prefix='/<int:break_id>/comments')
surf_break_bp.register_blueprint(break_type_bp, url_prefix='/<int:break_id>/break_type')

def authorise_as_admin(fn): #decorator for deleting surf breaks
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):  #function to check if user is admin before surf break can be deleted.
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_admin:
            return fn(*args, **kwargs)
        else:
            #error message in not admin
            return {'error': 'Not authorised to perform delete'}
    
    return wrapper

# GET method to view all surf breaks
@surf_break_bp.route('/') #route to GET surf breaks
def get_all_surf_breaks():
    stmt = db.select(SurfBreak).order_by(SurfBreak.name)
    surf_breaks = db.session.scalars(stmt)
    # returns all surf breaks
    return surf_breaks_schema.dump(surf_breaks)

# GET method to view individual surf breaks using their ID
@surf_break_bp.route('/<int:id>') #route to GET individual surk breaks
def get_one_surf_break(id):
    stmt = db.select(SurfBreak).filter_by(id=id)
    surf_break = db.session.scalar(stmt)
    if surf_break:
        #if there is a match for the ID used, return that surf break
        return surf_break_schema.dump(surf_break)
    else:
        # if there is no surf break with that id, return error message
        return {'error': f'Surf break not found with id {id}'}, 404


# POST method to create a surf break
@surf_break_bp.route('/', methods=['POST'])  #route to POST surf breaks
@jwt_required()
def create_surf_break():
    body_data = surf_break_schema.load(request.get_json())

    surf_break = SurfBreak(
        name=body_data.get('name'), #input by user
        location=body_data.get('location'),#input by user
        description=body_data.get('description'),#input by user
        user_id=get_jwt_identity() #get user id
    )
    #add to session
    db.session.add(surf_break)
    #commit to db
    db.session.commit()

    return surf_break_schema.dump(surf_break), 201

# Delete method using surf break id
@surf_break_bp.route('/<int:id>', methods=['DELETE'])  #route to DELETE surf breaks
@jwt_required()
@authorise_as_admin# decorator - if user is not admin, surf break will not be deleted and return error message
def delete_one_surf_break(id):
    stmt = db.select(SurfBreak).filter_by(id=id)
    surf_break = db.session.scalar(stmt)
    if surf_break:
        #delete from session
        db.session.delete(surf_break)
        #commit to db
        db.session.commit()
        #return success message if surf break found and deleted
        return {'message': f'Surf Break {surf_break.name} deleted successfully'}
    else:
        #return error message, surf break not found
        return {'error': f'Surf Break not found with id {id}'}, 404

#PUT, PATCH method to update surf breaks
@surf_break_bp.route('/<int:id>', methods=['PUT', 'PATCH']) #route to PUT,PATCH surf breaks
@jwt_required()
def update_one_surf_break(id):
    body_data = surf_break_schema.load(request.get_json(), partial=True)
    stmt = db.select(SurfBreak).filter_by(id=id)
    surf_break = db.session.scalar(stmt)
    if surf_break:
        #retieve updated and existing surf break name, location and description
        surf_break.name = body_data.get('name') or surf_break.name
                                #updated                existing
        surf_break.location = body_data.get('location') or surf_break.location
        surf_break.description = body_data.get(
            'description') or surf_break.description
        #commit changes
        db.session.commit()
        #return updated schema
        return surf_break_schema.dump(surf_break)
    else:
        #error message
        return {'error': f'Surf Break not found with id {id}'}, 404
    
    

