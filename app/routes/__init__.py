from app.routes.course_routes import course_bp
from app.routes.student_routes import student_bp
from app.routes.enrollment_routes import enrollment_bp
from app.routes.lectures_routes import lecture_bp



def register_blueprints(app):
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(enrollment_bp)
    app.register_blueprint(lecture_bp)

