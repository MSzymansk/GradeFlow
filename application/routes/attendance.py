from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash

from application.database.models import Attendance
from application.extensions import db
from application.routes.auth import login_required
from application.services import attendance_service

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/attendance/xd/testowanie', methods=['GET'])
@login_required
def get_attendance():
    session = db.session
    attendance_list = attendance_service.get_attendance_summary_by_teacher(session)
    list_of_lessons = attendance_service.get_lessons(session)
    return jsonify(list_of_lessons)
    #return render_template("attendance.html", classes=attendance_list, lessons=list_of_lessons)


@attendance_bp.route('/attendance', methods=['GET'])
@login_required
def get_lessons_list():
    session = db.session
    list_of_lessons = attendance_service.get_lessons_list(session)
    return render_template("attendance.html", lessons=list_of_lessons)



@attendance_bp.route('/attendance/<data>/<klasa>', methods=['GET'])
@login_required
def szczegoly_lesson(data, klasa):
    session = db.session
    students_attendece_list = attendance_service.get_class_attendance_list(session,data,klasa)
    return render_template("day_attendance.html", attendance = students_attendece_list)



@attendance_bp.route('/attendance/<data>/update', methods=['PUT'])
@login_required
def update_student_state(data):
    json_data = request.get_json()
    try:
        attendance_id = json_data['id']
        status = json_data['status']
        return attendance_service.upgrade_attendance_in_db(db.session, attendance_id, status)
    except KeyError as e:
        print(f"Missing key: {e}")
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
