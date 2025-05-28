from datetime import date, datetime
from io import BytesIO

from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, send_file

from application.database.models import Attendance
from application.services import student_service
from application.services import class_service
from application.extensions import db
from application.routes.auth import login_required
from application.services import attendance_service
from openpyxl import Workbook

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/attendance', methods=['GET'])
@login_required
def get_lessons_list():
    session = db.session
    list_of_lessons = attendance_service.get_lessons_list(session)
    classes_list = class_service.get_all_classes_from_db(db.session)
    return render_template("attendance.html", lessons=list_of_lessons, classes=classes_list)



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

@attendance_bp.route('/attendance/new',methods=['GET'])
@login_required
def new_lesson():
    classes_list = class_service.get_all_classes_from_db(db.session)
    student_list_attendance = student_service.get_all_students(db.session)
    return render_template("add_attendance_list.html",class_students = student_list_attendance,classes=classes_list, current_date=date.today().isoformat())



@attendance_bp.route('/attendance/add',methods=['POST'])
@login_required
def add_attendance():
    json = request.get_json()
    try:
        for entry in json:
            entry_date = datetime.strptime(entry['date'], "%Y-%m-%d").date()
            entry_time = datetime.strptime(entry['time'], "%H:%M").time()
            new_attendance = Attendance(
                student_id=entry['student_id'],
                class_id=entry['class_id'],
                time=entry_time,
                date=entry_date,
                status=entry['status']
            )
            db.session.add(new_attendance)

        db.session.commit()
        return jsonify({"success": True, "message": "Obecność została zapisana."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 400

@attendance_bp.route('/attendance/raport', methods=['GET'])
@login_required
def generate_raport():
    studen_attendance_list = attendance_service.get_attendance_summary_by_teacher(db.session)
    wb  = Workbook()
    ws = wb.active
    ws.title = "raport obecnosci"
    ws.append(["ID obecnosci","Data","Godzina","Klasa","Imię","Nazwisko","Status"])

    for entry in studen_attendance_list:
        ws.append([
            entry["id"],
            entry["date"],
            entry["time"],
            entry["class"],
            entry["student_name"],
            entry["student_surname"],
            entry["status"]
        ])
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(output,download_name="raport_uczniow.xlsx",as_attachment=True,mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")