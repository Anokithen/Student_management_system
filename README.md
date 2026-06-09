# Student API — Flask + MySQL CRUD

REST API built with Flask, SQLAlchemy ORM, and MySQL. Manages **Students** and **Courses** with full CRUD operations.

---

## Setup

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file in the project root
cp .env.example .env   # then fill in your credentials

# 4. Create the database in MySQL
mysql -u root -p -e "CREATE DATABASE student_db;"

# 5. Run the app (tables are created automatically on first start)
python run.py
```

## Environment Variables (`.env`)

| Variable      | Description          | Default      |
|---------------|----------------------|--------------|
| `DB_USER`     | MySQL username       | `root`       |
| `DB_PASSWORD` | MySQL password       | `root123`    |
| `DB_HOST`     | MySQL host           | `localhost`  |
| `DB_NAME`     | Database name        | `student_db` |
| `FLASK_DEBUG` | Enable debug mode    | `True`       |

---

## API Testing

Base URL: `http://localhost:5000`

---

### Students

#### POST `/api/students` — Create a student

```json
{
  "full_name": "Raj Jey",
  "email": "jey@gmail.com",
  "age": 30,
  "cgpa": 3.8,
  "is_active": true,
  "joined_date": "2024-01-15"
}
```

**Success response `201`**
```json
{
  "message": "Student created successfully.",
  "student": {
    "id": 1,
    "full_name": "Raj Jey",
    "email": "jey@gmail.com",
    "age": 30,
    "cgpa": 3.8,
    "is_active": true,
    "joined_date": "2024-01-15",
    "created_at": "2024-01-15T10:30:00+00:00"
  }
}
```

**Validation error `400`**
```json
{
  "errors": [
    "email is required.",
    "age must be a positive integer."
  ]
}
```

**Duplicate email `400`**
```json
{
  "error": "Email address already exists."
}
```

---

#### GET `/api/students` — Get all students

No request body needed.

**Success response `200`**
```json
{
  "students": [
    {
      "id": 1,
      "full_name": "Raj Jey",
      "email": "jey@gmail.com",
      "age": 30,
      "cgpa": 3.8,
      "is_active": true,
      "joined_date": "2024-01-15",
      "created_at": "2024-01-15T10:30:00+00:00"
    }
  ]
}
```

---

#### GET `/api/students/1` — Get one student

No request body needed.

**Success response `200`**
```json
{
  "student": {
    "id": 1,
    "full_name": "Raj Jey",
    "email": "jey@gmail.com",
    "age": 30,
    "cgpa": 3.8,
    "is_active": true,
    "joined_date": "2024-01-15",
    "created_at": "2024-01-15T10:30:00+00:00"
  }
}
```

**Not found `404`**
```json
{
  "error": "Student not found."
}
```

---

#### PUT `/api/students/1` — Update a student

```json
{
  "full_name": "Raj Jey",
  "email": "jey@gmail.com",
  "age": 31,
  "cgpa": 3.9,
  "is_active": true,
  "joined_date": "2024-01-15"
}
```

**Success response `200`**
```json
{
  "message": "Student updated successfully.",
  "student": {
    "id": 1,
    "full_name": "Raj Jey",
    "email": "jey@gmail.com",
    "age": 31,
    "cgpa": 3.9,
    "is_active": true,
    "joined_date": "2024-01-15",
    "created_at": "2024-01-15T10:30:00+00:00"
  }
}
```

---

#### DELETE `/api/students/1` — Delete a student

No request body needed.

**Success response `200`**
```json
{
  "message": "Student deleted successfully."
}
```

---

### Courses

#### POST `/api/courses` — Create a course

```json
{
  "course_title": "Python Programming",
  "course_fee": 4999.00,
  "duration_months": 3,
  "description": "Learn Python from basics to advanced with hands-on projects.",
  "is_available": true
}
```

**More sample course payloads**

```json
{
  "course_title": "Full Stack Web Development",
  "course_fee": 12999.00,
  "duration_months": 6,
  "description": "HTML, CSS, JavaScript, React, Node.js and MySQL.",
  "is_available": true
}
```

```json
{
  "course_title": "Data Structures and Algorithms",
  "course_fee": 3499.00,
  "duration_months": 2,
  "description": "Problem solving with arrays, trees, graphs and dynamic programming.",
  "is_available": true
}
```

```json
{
  "course_title": "Flask REST API Development",
  "course_fee": 5999.00,
  "duration_months": 2,
  "description": "Build production-ready REST APIs using Flask and SQLAlchemy.",
  "is_available": true
}
```

```json
{
  "course_title": "Machine Learning with Python",
  "course_fee": 9999.00,
  "duration_months": 4,
  "description": "scikit-learn, pandas, numpy and real-world ML projects.",
  "is_available": true
}
```

**Success response `201`**
```json
{
  "message": "Course created successfully.",
  "course": {
    "id": 1,
    "course_title": "Python Programming",
    "course_fee": 4999.0,
    "duration_months": 3,
    "description": "Learn Python from basics to advanced with hands-on projects.",
    "is_available": true,
    "created_at": "2024-01-15T10:30:00+00:00"
  }
}
```

**Validation error `400`**
```json
{
  "errors": [
    "course_title is required.",
    "course_fee must be a positive number."
  ]
}
```

**Duplicate title `400`**
```json
{
  "error": "Course title already exists."
}
```

---

#### GET `/api/courses` — Get all courses

No request body needed.

**Success response `200`**
```json
{
  "courses": [
    {
      "id": 1,
      "course_title": "Python Programming",
      "course_fee": 4999.0,
      "duration_months": 3,
      "description": "Learn Python from basics to advanced with hands-on projects.",
      "is_available": true,
      "created_at": "2024-01-15T10:30:00+00:00"
    }
  ]
}
```

---

#### GET `/api/courses/1` — Get one course

No request body needed.

**Success response `200`**
```json
{
  "course": {
    "id": 1,
    "course_title": "Python Programming",
    "course_fee": 4999.0,
    "duration_months": 3,
    "description": "Learn Python from basics to advanced with hands-on projects.",
    "is_available": true,
    "created_at": "2024-01-15T10:30:00+00:00"
  }
}
```

**Not found `404`**
```json
{
  "error": "Course not found."
}
```

---

#### PUT `/api/courses/1` — Update a course

```json
{
  "course_title": "Python Programming",
  "course_fee": 5499.00,
  "duration_months": 4,
  "description": "Updated course with advanced topics and new projects.",
  "is_available": true
}
```

**Success response `200`**
```json
{
  "message": "Course updated successfully.",
  "course": {
    "id": 1,
    "course_title": "Python Programming",
    "course_fee": 5499.0,
    "duration_months": 4,
    "description": "Updated course with advanced topics and new projects.",
    "is_available": true,
    "created_at": "2024-01-15T10:30:00+00:00"
  }
}
```

---

#### DELETE `/api/courses/1` — Delete a course

No request body needed.

**Success response `200`**
```json
{
  "message": "Course deleted successfully."
}
```

---

## Project Structure

```
student-api/
├── .env                        # local DB credentials (not committed)
├── .env.example                # template for .env
├── .gitignore
├── README.md
├── requirements.txt
├── run.py                      # entry point — starts the server
└── app/
    ├── __init__.py             # create_app() factory + error handlers
    ├── config.py               # loads DB config from .env
    ├── extensions.py           # SQLAlchemy db instance
    ├── utils.py                # shared helpers (utc_now, etc.)
    ├── models/
    │   ├── student_model.py
    │   └── course_model.py
    ├── controllers/
    │   ├── student_controller.py
    │   └── course_controller.py
    └── routes/
        ├── student_routes.py
        └── course_routes.py
```
