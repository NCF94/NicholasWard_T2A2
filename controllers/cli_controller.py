from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.surf_break import SurfBreak
from models.comment import Comment
from models.break_type import BreakType
from datetime import date

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create') #create tables specified in models folder
def create_db():
    db.create_all()
    print("Tables Created") #confirmation message function worked

@db_commands.cli.command('drop') #delete or 'drop' database and its associated tables
def drop_db():
    db.drop_all()
    print("Tables dropped") #confirmation message function worked
    
@db_commands.cli.command('seed') #seeds the created database with data for all models in the database
def seed_db():
    users = [
        User( #ADMIN
            name='Nick',
            email='admin@surfing.com',
            date_of_birth='08/02/1994',
            password=bcrypt.generate_password_hash('admin').decode('utf-8'),
            is_admin=True
        ),
        User( #NON ADMIN USER
            name='User1',
            date_of_birth='18/07/1990',
            email='user1@surfing.com',
            password=bcrypt.generate_password_hash('user1').decode('utf-8')
        )
    ]
    
    db.session.add_all(users)
    
    break_type = [ #Create break types
        BreakType(
            type_id = 0,
            break_type="beach",
        ),
        
        BreakType(
            type_id = 1,
            break_type="reef",
        ),
        
        BreakType(
            type_id = 2,
            break_type="point",
        ),
    ]
    db.session.add_all(break_type)
    
    surf_break = [ #CREATE surf_breaks
        SurfBreak(
            name='Pines',
            location='Shoreham',
            description='Surf break on the mornington peninsula',
            user=users[0],
            break_type=break_type[0]  
        ),
        SurfBreak(
            name='Little Noosa',
            location='Shoreham',
            description='Surf break on the mornington peninsula',
            user=users[0],
            break_type=break_type[1]  
        ),
        SurfBreak(
            name='Honeysuckle',
            location='Point Leo',
            description='Surf break on the mornington peninsula',
            user=users[1],
            break_type=break_type[2]  
        ),
    ]
    
    db.session.add_all(surf_break)
    
    comments = [ #create comments
        Comment(
            user_comment="Comment 1",
            rating="1/5",
            date=date.today(),
            user=users[1],
            surf_break=surf_break[0] 
        ),
        Comment(
            user_comment="Comment 2",
            rating="2/5",
            date=date.today(),
            user=users[1],
            surf_break=surf_break[1] 
        ),
        Comment(
            user_comment="Comment 3",
            rating="3/5",
            date=date.today(),
            user=users[0],
            surf_break=surf_break[2] 
        ),
    ]
    
    db.session.add_all(comments)
    
    
    
    
    db.session.commit() # commit or seed all to database
    
    print("Tables seeded") #confirmatrion message function worked