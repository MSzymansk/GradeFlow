from flask import Blueprint, jsonify, request, redirect, url_for

from application.routes.auth import login_required
from application.services import grades_service
from application.services import student_service

from application.extensions import db
from flask import render_template

from application.services.student_service import *

students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/", methods=["GET"])
@login_required
def get_all():
    session = db.session
    students = student_service.get_all_students(session)
    return render_template("students.html", students=students)


@students_bp.route("/<int:id>/grades", methods=["GET"])
@login_required
def get_class_grades(id):
    session = db.session
    class_grades = grades_service.get_class_grade(session, id)
    return jsonify(class_grades)


@students_bp.route("/add", methods=["POST"])
@login_required
def add_student():
    json = request.get_json()
    try:
        new_student = Student(
            name=json['name'],
            surname=json['surname'],
            pesel=json['pesel'],
            class_id=int(json['class_id'])
        )
        return add_student_to_db(db.session, new_student)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@students_bp.route('/delete', methods=["POST"])
@login_required
def delete_student():
    json = request.get_json()
    try:
        return delete_student_from_db(db.session, json['id'])
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@students_bp.route('/update', methods=["PUT"])
@login_required
def update_student():
    json = request.get_json()
    try:
        new_student = Student(
            name=json['name'],
            surname=json['surname'],
            pesel=json['pesel'],
            class_id=int(json['class_id'])
        )
        return update_student_in_db(db.session, json['id'], new_student)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
