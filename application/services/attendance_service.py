from collections import defaultdict
from flask import session, jsonify


from application.database.models import Attendance, _Class, student, Student, teacher
from sqlalchemy.orm import selectinload


def get_attendance_summary_by_teacher(db_session):
    attendances = db_session.query(Attendance).all()

    result = [{
        "id":attendance.id,
        "date":attendance.date.strftime("%Y-%m-%d"),
        "time":attendance.time.strftime("%H:%M"),
        "class": attendance._class.name,
        "student_name":attendance.student.name,
        "student_surname" : attendance.student.surname,
        "status": attendance.status,
    }
    for attendance in attendances]

    return result


def get_lessons(db_session):
    lessons = db_session.query(Attendance)\
        .join(_Class, Attendance.class_id == _Class.id)\
        .options(selectinload(Attendance.student), selectinload(Attendance._class))\
        .filter(_Class.teacher_id == session["teacher_id"])\
        .all()

    grouped = defaultdict(list)

    for lesson in lessons:
        key = (lesson.date, lesson._class.name)
        grouped[key].append({
            "imie": lesson.student.name,
            "nazwisko": lesson.student.surname,
            "status": lesson.status
        })

    result = []
    for (date, class_name), students in grouped.items():
        result.append({
            "data": date.isoformat(),
            "klasa": class_name,
            "uczniowie": students
        })

    return result

def get_lessons_list(db_session):
    lessons = db_session.query(Attendance)\
        .join(_Class, Attendance.class_id == _Class.id)\
        .filter(_Class.teacher_id == session["teacher_id"]).all()

    result_set = set()

    for lesson in lessons:
        result_set.add((
            lesson.date.isoformat(),
            lesson.time.strftime("%H:%M"),
            lesson._class.name,
            lesson._class.id
        ))

    result = [
        {"data": date, "godzina": time, "klasa": class_name, "class_id":class_id}
        for (date, time, class_name,class_id) in sorted(result_set)
    ]

    return result


from flask import session

def get_class_attendance_list(db_session, data, _class_select):
    attendance_list = db_session.query(Attendance)\
        .join(_Class)\
        .filter(Attendance.date == data)\
        .filter(_Class.name == _class_select)\
        .filter(_Class.teacher_id == session["teacher_id"])\
        .all()
    time = attendance_list[0].time.strftime("%H:%M") if attendance_list else None
    return {
        "data": data,
        "godzina": time,
        "class": _class_select,
        "students": [
            {
                "attendance_id":attendance.id,
                "studentId": attendance.student.id,
                "studentName": attendance.student.name,
                "studentSurname" : attendance.student.surname,
                "status": attendance.status
            }
            for attendance in attendance_list
        ]
    }


def upgrade_attendance_in_db(db_session, attendance_id, status):
    attendance = db_session.query(Attendance) \
        .filter(Attendance.id == attendance_id).first()
    if not attendance:
        return jsonify({'error': "attendance not found"}), 404
    attendance.status = status
    db_session.commit()
    return jsonify({'message': "attendance updated"}), 200
