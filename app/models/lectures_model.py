from app.extensions import db
from app.utils import utc_now


class Lecture(db.Model):
    __tablename__ = "lectures"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    department= db.Column(db.String(100), nullable=False)
    

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "department":self.department,
            "email": self.email,
        }
