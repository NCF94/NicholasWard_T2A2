from flask import Blueprint, request
from init import db
from datetime import date
from models.surf_break import SurfBreak
from models.comment import Comment, comment_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment(break_id):
    body_data = request.get_json()
    stmt = db.select(SurfBreak).filter_by(id=break_id) 
    surf_break = db.session.scalar(stmt)
    if surf_break:
        comment = Comment(
            user_comment=body_data.get('user_comment'),
            rating=body_data.get('rating'),
            date=date.today(),
            surf_break=surf_break, # pass the model instance to the model field
            user_id=get_jwt_identity() # pass id to the _id field
        )

        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201
    else:
        return {'error': f'Surf Break not found with id {break_id}'}, 404
    
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(break_id, comment_id):
    stmt = db.select(Comment).filter_by(comment_id=comment_id)
    comment = db.session.scalar(stmt)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return {'user_comment': f"Comment '{comment.user_comment}' deleted successfully"}
    else:
        return {'error': f'Comment not found with id {comment_id}'}, 404
    
@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_comment(break_id, comment_id):
    body_data = request.get_json()
    stmt = db.select(Comment).filter_by(comment_id=comment_id)
    comment = db.session.scalar(stmt) # comment from database that needs to be updated
    if comment:
        comment.user_comment = body_data.get('user_comment') or comment.user_comment
        db.session.commit()
        return comment_schema.dump(comment)
    else:
        return {'error': f'Comment not found with id {comment_id}'}, 404