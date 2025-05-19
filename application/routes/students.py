from flask import Blueprint, jsonify, request, redirect, url_for
from application.services import grades_service
from application.services import student_service

from application.extensions import db
from flask import render_template

students_bp = Blueprint("students", __name__,url_prefix="/students")

@students_bp.route("/", methods=["GET"])
def get_all():
    session = db.session
    students = student_service.get_all_students(session)
    return render_template("students.html",students=students)

@students_bp.route("/<int:id>/grades", methods=["GET"])
def get_class_grades(id):
    session = db.session
    class_grades = grades_service.get_class_grade(session,id)
    return jsonify(class_grades)