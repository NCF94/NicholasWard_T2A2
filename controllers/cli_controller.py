from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.surf_break import SurfBreak
from models.comment import Comment
# from models.card import Card
# from models.comment import Comment
from datetime import date

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")
    
@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name='Nick',
            email='admin@surfing.com',
            date_of_birth='08/02/1994',
            password=bcrypt.generate_password_hash('admin').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='User1',
            date_of_birth='18/07/1990',
            email='user1@surfing.com',
            password=bcrypt.generate_password_hash('user1').decode('utf-8')
        )
    ]
    
    db.session.add_all(users)
    
    surf_break = [
        SurfBreak(
            name='Pines',
            location='Shoreham',
            description='Surf break on the mornington peninsula',
            user=users[0],
            # comment=comments[1]
        ),
        SurfBreak(
            name='Little Noosa',
            location='Shoreham',
            description='Surf break on the mornington peninsula',
            user=users[0],
            # comment=comments[2]
        ),
        SurfBreak(
            name='Honeysuckle',
            location='Point Leo',
            description='Surf break on the mornington peninsula',
            user=users[1],
            # comment=comments[3]
        ),
        SurfBreak(
            name='Second Reef',
            location='Point Leo',
            description='Surf break on the mornington peninsula',
            user=users[1],
            # comment=comments[4]
        )
    ]
    
    db.session.add_all(surf_break)
    
    comments = [
        Comment(
            user_comment="Comment 1",
            rating="1/5",
            user=users[1],
            surf_break=surf_break[0] 
        ),
        Comment(
            user_comment="Comment 2",
            rating="2/5",
            user=users[1],
            surf_break=surf_break[1] 
        ),
        Comment(
            user_comment="Comment 3",
            rating="3/5",
            user=users[0],
            surf_break=surf_break[2] 
        ),
        Comment(
            user_comment="Comment 4",
            rating="4/5",
            user=users[0],
            surf_break=surf_break[3] 
        )
    ]
    db.session.add_all(comments)
    
    db.session.commit()
    
    print("Tables seeded")