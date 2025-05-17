from instan.config import DATABASE_URI
from application.database.models import Base, Student, Teacher, _Class, Attendance
from sqlalchemy import *
from sqlalchemy.orm import *
from flask import jsonify


def init_database():
    engine = create_engine(f'sqlite:///{DATABASE_URI}', echo=True)
    Base.metadata.create_all(engine)


# Students
def get_all_students(session):
    students = session.query(Student).all()
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
        "class_id": student.class_id,
    }
    return jsonify(student_data), 200


def add_student(session, pesel: int, name: str, surname: str, class_id: int):
    stmt = insert(Student).values(pesel=pesel, name=name, surname=surname, class_id=class_id).returning(Student.id)
    result = session.execute(stmt)
    session.commit()
    new_id = result.scalar_one()
    return jsonify({"message": "Student added successfully", "student_id": new_id}), 201


def delete_student(session, student_id: int):
    student = session.query(Student).filter(Student.id == student_id).first()
    if not student:
        return jsonify({"error": "Student not found"}), 404

    stmt = delete(Student).where(Student.id == student_id)
    session.execute(stmt)
    session.commit()
    return jsonify({"message": f"Student with ID {student_id} deleted"}), 200

