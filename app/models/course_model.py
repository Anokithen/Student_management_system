from app.extensions import db
from app.utils import utc_now
from app.models.lectures_model import Lecture


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(20), nullable=False, unique=True)
    course_name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    lecture_id = db.Column(db.Integer,db.ForeignKey('lectures.id'), nullable=False)
   

    def to_dict(self):
        return {
            "id": self.id,
            "course_code": self.course_code,
            "course_name": self.course_name,
            "credits": self.credits,
            "lecture_id": self.lecture_id,

        }
