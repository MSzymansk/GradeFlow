from application.database.models import Grade, Student, _Class
from flask import session, jsonify
from sqlalchemy import *


def get_class_grade(db_session, class_id: int):
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
    students_query = db_session.query(Student).join(_Class).filter(_Class.teacher_id == session["teacher_id"]).all()
    students = {}
    for student in students_query:
        students[student.id] = {
            "student_id": student.id,
            "student_name": student.name,
            "student_surname": student.surname,
            "class_name": student._class.name,
            "class_id": student._class.id,
            "grades_list": []
        }
        if hasattr(student, 'grades'):
            students[student.id]["grades_list"] = [grade.value for grade in student.grades]

        grades_list = students[student.id]["grades_list"]
        students[student.id]["avg_grade"] = sum(grades_list) / len(grades_list) if grades_list else 0

    return list(students.values())



def get_students_grades(db_session, id: int):
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


def update_grade_in_db(db_session, new_grade: Grade):
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


def delete_grade_from_db(db_session, id: int):
    grade = db_session.query(Grade).filter(Grade.id == id).first()
    if not grade:
        return jsonify({"error": "Grade not found"}), 404
    stmt = delete(Grade).where(Grade.id == id)
    db_session.execute(stmt)
    db_session.commit()
    return jsonify({"message": f"Grade with ID {id} delated"}), 200


def add_grade_to_db(db_session, new_grade: Grade):
    stmt = insert(Grade).values(
        value=new_grade.value,
        type=new_grade.type,
        student_id=new_grade.student_id,
        teacher_id=session["teacher_id"]
    ).returning(Grade.id)

    result = db_session.execute(stmt)
    new_id = result.scalar_one()
    db_session.commit()
    return jsonify({"message": "Grade added successfully", "grade_id": new_id}), 201
