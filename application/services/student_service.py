import flask

from application.database.models import Student, Grade, _Class, Attendance
from flask import jsonify, session
from sqlalchemy import *


def get_all_students(db_session):
    students = db_session.query(Student).join(_Class)\
    .filter(_Class.teacher_id == session['teacher_id']).all()

    results = []

    for student in students:
        avg = db_session.query(func.avg(Grade.value)).filter(Grade.student_id==student.id).scalar() or 1.0
        absence = db_session.query(func.count(Attendance.id)).filter(Attendance.student_id==student.id, Attendance.status == "nieobecny").scalar()

        results.append({
            "id": student.id,
            "pesel": student.pesel,
            "name": student.name,
            "surname": student.surname,
            "class_id": student.class_id,
            "class_name": student._class.name,
            "avg": avg,
            "absence_count": absence
        })

    return results

def get_all_students_class(db_session, class_id: int):
    students = db_session.query(Student).filter(Student.class_id == class_id).all()
    if not students:
        return jsonify({"error": "No students found for given class id"}), 404

    students_list = [
        {
            "id": student.id,
            "pesel": student.pesel,
            "name": student.name,
            "surname": student.surname,
            "class_id": student.class_id
        }
        for student in students
    ]
    return jsonify(students_list), 200


def get_student(db_session, student_id: int):
    student = db_session.query(Student).filter(Student.id == student_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student_data = {
        "id": student.id,
        "pesel": student.pesel,
        "name": student.name,
        "surname": student.surname,
        "class_id": student.class_id
    }
    return jsonify(student_data), 200


def add_student_to_db(db_session, new_student: Student):
    stmt = insert(Student).values(pesel=new_student.pesel, name=new_student.name, surname=new_student.surname,
                                  class_id=new_student.class_id).returning(Student.id)
    result = db_session.execute(stmt)
    new_id = result.scalar_one()
    db_session.commit()
    return jsonify({"message": "Student added successfully", "student_id": new_id}), 201


def delete_student_from_db(db_session, student_id: int):
    student = db_session.query(Student).filter(Student.id == student_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    stmt = delete(Student).where(Student.id == student_id)
    db_session.execute(stmt)
    db_session.commit()
    return jsonify({"message": f"Student with ID {student_id} deleted"}), 200


def update_student_in_db(db_session, student_id: int, new_student: Student):
    student = db_session.query(Student).filter(Student.id == student_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    stmt = update(Student).where(Student.id == student_id).values(
        pesel=new_student.pesel,
        name=new_student.name,
        surname=new_student.surname,
    )
    db_session.execute(stmt)
    db_session.commit()
    return jsonify({"message": f"Student with ID {student_id} updated"}), 200