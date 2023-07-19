from flask import Blueprint, request
from init import db
from datetime import date
from models.surf_break import SurfBreak, surf_break_schema, surf_breaks_schema
from flask_jwt_extended import get_jwt_identity, jwt_required

surf_break_bp = Blueprint('surf_breaks', __name__, url_prefix='/surf_breaks')

@surf_break_bp.route('/')
def get_all_surf_breaks():
    stmt = db.select(SurfBreak)
    surf_breaks = db.session.scalars(stmt)
    return surf_breaks_schema.dump(surf_breaks)
    
