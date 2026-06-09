from flask import jsonify, request
from app.extensions import db
from app.models.enrollment_model import Enrollment
from app.models.student_model import Student
from app.models.course_model import Course
from datetime import datetime


def _validate_enrollment_payload(data, enrollment_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    student_id = data.get("student_id")
    if student_id is None or str(student_id).strip() == "":
        errors.append("Invalid student selected.")
    else:
        try:
            student = Student.query.get(int(student_id))
            if not student:
                errors.append("Invalid student selected.")
        except (TypeError, ValueError):
            errors.append("Invalid student selected.")

    course_id = data.get("course_id")
    if course_id is None or str(course_id).strip() == "":
        errors.append("Invalid course selected.")
    else:
        try:
            course = Course.query.get(int(course_id))
            if not course:
                errors.append("Invalid course selected.")
        except (TypeError, ValueError):
            errors.append("Invalid course selected.")

    enrollment_date = data.get("enrollment_date")
    if enrollment_date is None or str(enrollment_date).strip() == "":
        errors.append("Enrollment date is required.")
    else:
        try:
            datetime.strptime(str(enrollment_date).strip(), "%Y-%m-%d")
        except ValueError:
            errors.append("Enrollment date is required.")

    status = data.get("status")
    allowed_statuses = ["Active", "Completed", "Dropped"]
    if status is None or str(status).strip() == "":
        errors.append("Enter enrollment status.")
    elif str(status).strip() not in allowed_statuses:
        errors.append("Invalid enrollment status.")

    return errors


def create_enrollment():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_enrollment_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        enrollment = Enrollment(
            student_id=int(data.get("student_id")),
            course_id=int(data.get("course_id")),
            enrollment_date=datetime.strptime(data.get("enrollment_date").strip(), "%Y-%m-%d"),
            status=data.get("status").strip(),
        )
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({"message": "Enrollment created successfully.", "enrollment": enrollment.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify({"enrollments": [e.to_dict() for e in enrollments]}), 200


def get_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404
    return jsonify({"enrollment": enrollment.to_dict()}), 200


def update_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_enrollment_payload(data, enrollment_id=enrollment_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        enrollment.student_id      = int(data.get("student_id"))
        enrollment.course_id       = int(data.get("course_id"))
        enrollment.enrollment_date = datetime.strptime(data.get("enrollment_date").strip(), "%Y-%m-%d")
        enrollment.status          = data.get("status").strip()
        db.session.commit()
        return jsonify({"message": "Enrollment updated successfully.", "enrollment": enrollment.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404
    try:
        db.session.delete(enrollment)
        db.session.commit()
        return jsonify({"message": "Enrollment deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500