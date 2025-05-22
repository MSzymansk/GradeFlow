from application.database.models import Student, Grade, _Class
from flask import jsonify
from sqlalchemy import *


def get_all_students(session):
    students = session.query(Student).join(_Class).all()
    return [
        {
            "id": student.id,
            "pesel": student.pesel,
            "name": student.name,
            "surname": student.surname,
            "class_id": student.class_id,
            "class_name": student._class.name
        }
        for student in students
    ]


def get_all_students_class(session, class_id: int):
    students = session.query(Student).filter(Student.class_id == class_id).all()
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


def get_student(session, student_id: int):
    student = session.query(Student).filter(Student.id == student_id).first()
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


def add_student_to_db(session, new_student: Student):
    stmt = insert(Student).values(pesel=new_student.pesel, name=new_student.name, surname=new_student.surname,
                                  class_id=new_student.class_id).returning(Student.id)
    result = session.execute(stmt)
    new_id = result.scalar_one()
    session.commit()
    return jsonify({"message": "Student added successfully", "student_id": new_id}), 201


def delete_student_from_db(session, student_id: int):
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    stmt = delete(Student).where(Student.id == student_id)
    session.execute(stmt)
    session.commit()
    return jsonify({"message": f"Student with ID {student_id} deleted"}), 200


def update_student_in_db(session, student_id: int, new_student: Student):
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    stmt = update(Student).where(Student.id == student_id).values(
        pesel=new_student.pesel,
        name=new_student.name,
        surname=new_student.surname,
    )
    session.execute(stmt)
    session.commit()
    return jsonify({"message": f"Student with ID {student_id} updated"}), 200
