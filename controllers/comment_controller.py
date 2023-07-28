from flask import Blueprint, request
from init import db
from datetime import date
from models.surf_break import SurfBreak
from models.comment import Comment, comment_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

comments_bp = Blueprint('comments', __name__)
 #POST method of addiing comments
@comments_bp.route('/', methods=['POST']) #route to POST comments
@jwt_required()
def create_comment(break_id):
    body_data = request.get_json()
    stmt = db.select(SurfBreak).filter_by(id=break_id) #select surf break using its ID
    surf_break = db.session.scalar(stmt) 
    if surf_break:
        comment = Comment( 
            user_comment=body_data.get('user_comment'), #user input
            rating=body_data.get('rating'), #user input
            date=date.today(), #date
            surf_break=surf_break, # pass the model instance to the model field
            user_id=get_jwt_identity() # pass id to the _id field
        )

        db.session.add(comment) #add comment to SurfBreak
        db.session.commit() #commit to db
        return comment_schema.dump(comment), 201
    else:
        #error message if Surf Break doesnt exist
        return {'error': f'Surf Break not found with id {break_id}'}, 404
    
 # DELETE method for deleting comments   
@comments_bp.route('/<int:comment_id>', methods=['DELETE']) #route to DELETE comments
@jwt_required()
def delete_comment(break_id, comment_id):
    stmt = db.select(Comment).filter_by(comment_id=comment_id) #select comment using its comment id
    comment = db.session.scalar(stmt)
    if comment:
        db.session.delete(comment) #delete comment if id is found
        db.session.commit() #commit to db
        # return what comment was deleted
        return {'user_comment': f"Comment '{comment.user_comment}' deleted successfully"}
    else:
        # error  message if comment id doesnt exist
        return {'error': f'Comment not found with id {comment_id}'}, 404
    
#PUT, PATCH method for updating comments    
@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH']) #route to PUT, PATCH comments
@jwt_required()
def update_comment(break_id, comment_id):
    body_data = request.get_json() #retrieve data
    stmt = db.select(Comment).filter_by(comment_id=comment_id) #select comment using comment_id
    comment = db.session.scalar(stmt) # comment from database that needs to be updated
    if comment:
        comment.user_comment = body_data.get('user_comment') or comment.user_comment #comment update input by user
        db.session.commit() #commit to db
        return comment_schema.dump(comment) # return updated comment
    else:
        return {'error': f'Comment not found with id {comment_id}'}, 404 #error message if comment_id not found