from app.extensions import db
from app.utils import utc_now
from app.models.student_model import Student
from app.models.course_model import Course

class Enrollment(db.Model):
    __tablename__ = "enrollments"

    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer,db.ForeignKey('courses.id'), nullable=False)
    enrollment_date =db.Column(db.DateTime,nullable=False)
    status = db.Column(db.String(20),nullable=False)
   

    def to_dict(self):
        return {
            "enrollment_id": self.enrollment_id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "enrollment_date": self.enrollment_date,
            "status": self.status,

        }
