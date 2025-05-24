from application.database.models import Grade, Student, _Class
from flask import session, jsonify
from sqlalchemy import *


def get_class_grade(db_session, class_id):
    res = []
    students = db_session.query(Student).filter(Student.class_id == class_id).all()
    for student in students:
        grades = Grade.query.filter_by(student_id=student.id).all()
        avg = round(sum(g.value for g in grades) / len(grades), 2) if grades else None
        res.append({
            "id": student.id,
            "student_name": student.name,
            "student_surname": student.surname,
            "grades": [g.value for g in grades],
            "avg": avg,
        })
    return res


def get_all_grades_students_classes(db_session):
    grades = db_session.query(Grade).join(Student).join(_Class).filter(_Class.teacher_id == session["teacher_id"]).all()

    students = {}

    for grade in grades:
        student = grade.student
        student_id = student.id

        if student_id not in students:
            students[student_id] = {
                "student_id": student.id,
                "student_name": student.name,
                "student_surname": student.surname,
                "class_name": student._class.name,
                "class_id": student._class.id,
                "grades_list": []
            }

        students[student_id]["grades_list"].append(grade.value)

    for student_data in students.values():
        grades_list = student_data["grades_list"]
        student_data["avg_grade"] = sum(grades_list) / len(grades_list) if grades_list else 0

    return list(students.values())


def get_students_grades(db_session, id):
    student_grades = db_session.query(Grade).join(Student).filter(Student.id == id).all()

    result = []
    for e in student_grades:
        result.append({
            "name": e.student.name,
            "surname": e.student.surname,
            "grade_id": e.id,
            "grade_value": e.value,
            "grade_type": e.type
        })
    return result


def update_grade_in_db(db_session, new_grade):
    grade = db_session.query(Grade).filter(Grade.id == new_grade.id).first()
    if not grade:
        return jsonify({"error": "Grade not found"}), 404
    stmt = update(Grade).where(Grade.id == new_grade.id).values(
        type=new_grade.type,
        value=new_grade.value
    )
    db_session.execute(stmt)
    db_session.commit()
    return jsonify({"message": f"Grade with ID {new_grade.id} updated"}), 200


def delete_grade_from_db(db_session, id):
    grade = db_session.query(Grade).filter(Grade.id == id).first()
    if not grade:
        return jsonify({"error": "Grade not found"}), 404
    stmt = delete(Grade).where(Grade.id == id)
    db_session.execute(stmt)
    db_session.commit()
    return jsonify({"message": f"Grade with ID {id} delated"}), 200
