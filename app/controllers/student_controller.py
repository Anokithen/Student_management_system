from datetime import datetime
from flask import jsonify, request
from app.extensions import db
from app.models.student_model import Student


def _validate_student_payload(data, student_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    first_name = data.get("first_name")
    if first_name is None or str(first_name).strip() == "":
        errors.append("first_name is required.")
    elif not str(first_name).isalpha():
        errors.append("First name must contain only letters.")

    last_name = data.get("last_name")
    if last_name is None or str(last_name).strip() == "":
        errors.append("last_name is required.")
    elif not str(last_name).isalpha():
        errors.append("Last name must contain only letters.")

    email = data.get("email")
    if email is None or str(email).strip() == "":
        errors.append("email is required.")
    elif str(email).strip():
        q = Student.query.filter(Student.email == str(email).strip())
        if student_id:
            q = q.filter(Student.id != student_id)
        if q.first():
            errors.append("Email address already exists.")

    
    return errors  


def create_student():
    dateofbirth = data.get("date_of_birth")
    todaydate = datetime.today()
    
    if dateofbirth is None or str(dateofbirth).strip() == "":
        errors.append("Date of birth is required.")
    else:
        try:
            dob = datetime.strptime(str(dateofbirth).strip(), "%Y-%m-%d")
            if dob >= todaydate:
                errors.append("Date of birth cannot be in the future.")
        except ValueError:
            errors.append("Date of birth must be in YYYY-MM-DD format.")

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400
    errors = _validate_student_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        student = Student(
            first_name=data.get("first_name").strip(),
            last_name=data.get("last_name").strip(),
            email=data.get("email").strip(),
            date_of_birth=datetime.strptime(data.get("date_of_birth").strip(), "%Y-%m-%d"),
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({"message": "Student created successfully.", "student": student.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_students():
    students = Student.query.all()
    return jsonify({"students": [s.to_dict() for s in students]}), 200


def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({"student": student.to_dict()}), 200


def update_student(student_id):
    dateofbirth = data.get("date_of_birth")
    todaydate = datetime.today()
    
    if dateofbirth is None or str(dateofbirth).strip() == "":
        errors.append("Date of birth is required.")
    else:
        try:
            dob = datetime.strptime(str(dateofbirth).strip(), "%Y-%m-%d")
            if dob >= todaydate:
                errors.append("Date of birth cannot be in the future.")
        except ValueError:
            errors.append("Date of birth must be in YYYY-MM-DD format.")

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_student_payload(data, student_id=student_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        student.first_name = data.get("first_name").strip()
        student.last_name = data.get("last_name").strip()  
        student.email = data.get("email").strip()
        student.date_of_birth = datetime.strptime(data.get("date_of_birth").strip(), "%Y-%m-%d") 
        db.session.commit()
        return jsonify({"message": "Student updated successfully.", "student": student.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500