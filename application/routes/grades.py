from flask import Blueprint, jsonify, request, redirect, url_for
from application.extensions import db
from flask import render_template
from application.services.class_service import *
from application.services.grades_service import *
from application.routes.auth import login_required

grades_bp = Blueprint("grades", __name__, url_prefix="/grades")


@grades_bp.route("/", methods=["GET"])
@login_required
def get_all():
    session = db.session
    classes = get_all_classes_from_db(session)
    grades = get_all_grades_students_classes(session)
    return render_template("grades.html", grades=grades, classes=classes)


@grades_bp.route("/details/<id>")
@login_required
def get_grades_details(id):
    grades = get_students_grades(db.session, id)
    return render_template("grades_details.html", grades=grades)


@grades_bp.route("/update", methods=['PUT'])
def update_grade():
    json = request.get_json()
    try:
        new_grade = Grade(
            id=json["id"],
            type=json["type"],
            value=json["value"]
        )
        return update_grade_in_db(db.session, new_grade)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@grades_bp.route('/delete', methods=['POST'])
def delete_grade():
    json = request.get_json()
    try:
        return delete_grade_from_db(db.session, json["id"])
    except Exception as e:
        return jsonify({"error": str(e)}), 400
