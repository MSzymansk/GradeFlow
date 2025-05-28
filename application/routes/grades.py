from io import BytesIO

from openpyxl import Workbook
from flask import Blueprint, jsonify, request, redirect, url_for, send_file
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
@login_required
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
@login_required
def delete_grade():
    json = request.get_json()
    try:
        return delete_grade_from_db(db.session, json["id"])
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@grades_bp.route('/add', methods=['POST'])
@login_required
def add_grade():
    json = request.get_json()
    try:
        new_grade = Grade(
            value=json["value"],
            type=json["type"],
            student_id=json["student_id"]
        )
        return add_grade_to_db(db.session, new_grade)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@grades_bp.route('/raport', methods=['GET'])
@login_required
def generate_raport():
    students_list = get_all_grades_students_classes(db.session)

    wb = Workbook()
    ws = wb.active
    ws.title = "Raport uczniów"
    ws.append(["ID ucznia", "Imię", "Nazwisko", "Klasa", "ID klasy", "Oceny", "Średnia ocen"])

    for student in students_list:
        grades_list = student["grades_list"]
        string_grades = []

        for grade in grades_list:
            string_grades.append(str(grade))

        grades_str = ", ".join(string_grades)
        ws.append([
            student["student_id"],
            student["student_name"],
            student["student_surname"],
            student["class_name"],
            student["class_id"],
            grades_str,
            round(student["avg_grade"], 2)
        ])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(output,
                     download_name="raport_uczniow.xlsx",
                     as_attachment=True,
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@grades_bp.route('/get_grades_for_chart',  methods=['GET'])
def api_all_grades_students_classes():
    data = get_all_grades_students_classes(db.session)
    return jsonify(data)
