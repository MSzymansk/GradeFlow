from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash

from application.extensions import db
from application.routes.auth import login_required
from application.services import attendance_service

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/attendance/xd', methods=['GET'])
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
    return jsonify("hello")