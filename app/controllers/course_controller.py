from flask import jsonify, request

from app.extensions import db
from app.models.course_model import Course
from app.models.lectures_model import Lecture


def _validate_course_payload(data, course_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    coursecode = data.get("course_code")
    if coursecode is None or str(coursecode).strip() == "":
        errors.append("course_code is required.")
    elif str(coursecode).strip():
        q = Course.query.filter(Course.course_code == str(coursecode).strip())
        if course_id:
            q = q.filter(Course.id != course_id)
        if q.first():
            errors.append("Course coursecode already exists.")

    coursename= data.get("course_name")
    if coursename is None:
        errors.append("course_name is required.")
    else:
        try:
            coursename_len = len(coursename)
            if coursename_len <= 2:
                errors.append("coursename minimum char size is 3")
        except (TypeError, ValueError):
            errors.append("coursename minimum char size is 3")

    credits = data.get("credits")
    if credits is None:
        errors.append("credits is required.")
    else:
        try:
            credits_val = int(credits)
            if credits_val >= 6:
                errors.append("credits must be in lower than 6.")
        except (TypeError, ValueError):
            errors.append("credits must be in lower than 6.")
        
    lecture_id = data.get("lecture_id")
    if lecture_id is not None:
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            errors.append(f"Lecturer with id {lecture_id} does not exist."), 404
    
    lecture_id = data.get("lecture_id")
    if lecture_id is None:
        errors.append(f"lecturer id is important")

    return errors


def create_course():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_course_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400
    

    try:
        course = Course(
            course_code=data.get("course_code").strip(),
            course_name=data.get("course_name"),
            credits=int(data.get("credits")),
            lecture_id=data.get("lecture_id"),
        )
        db.session.add(course)
        db.session.commit()
        return jsonify({"message": "Course created successfully.", "course": course.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_courses():
    courses = Course.query.all()
    return jsonify({"courses": [c.to_dict() for c in courses]}), 200


def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found."}), 404
    return jsonify({"course": course.to_dict()}), 200


def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_course_payload(data, course_id=course_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        course.course_code = data.get("course_code").strip()
        course.course_name = str(data.get("course_name")).strip()
        course.credits = int(data.get("credits"))
        course.lecture_id = int(data.get("lecture_id"))
        db.session.commit()
        return jsonify({"message": "Course updated successfully.", "course": course.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found."}), 404
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
