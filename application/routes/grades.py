from flask import Blueprint, jsonify, request, redirect, url_for
from application.extensions import db
from flask import render_template
from application.services.class_service import *
from application.services.grades_service import *



grades_bp = Blueprint("grades", __name__, url_prefix="/grades")


@grades_bp.route("/", methods=["GET"])
def get_all():
    session = db.session
    classes = get_all_classes_from_db(session)
    grades = get_all_grades_students_classes(session)
    return render_template("grades.html", grades=grades, classes=classes)