from flask import Blueprint, jsonify

from application.extensions import db
from application.routes.auth import login_required
from application.services import attendance_service

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance', methods=['GET'])
@login_required
def attendance():
    session = db.session
    attendance_list = attendance_service.get_attendance_summary_by_teacher(session)
    return jsonify(attendance_list)



