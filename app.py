from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Function to get a fresh database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="swathi2008",  # Replace with your MySQL password
        database="student_management"
    )

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "")
    dob = request.form.get("dob", "")
    phone = request.form.get("phone", "")
    email = request.form.get("email", "")
    department = request.form.get("department", "")
    year = request.form.get("year", "")

    # Validation checks
    if not name.replace(" ", "").isalpha():
        return "Invalid name"

    if not phone.isdigit() or len(phone) != 10:
        return "Invalid phone number"

    if "@" not in email or "." not in email:
        return "Invalid email"

    if department not in ["CSE", "ECE", "EEE", "Mechanical", "Civil"]:
        return "Invalid department"

    if year not in ["1", "2", "3", "4"]:
        return "Invalid year"

    # Database insertion inside a managed connection
    db = get_db_connection()
    cursor = db.cursor()

    query = """
        INSERT INTO students
        (name, dob, phone, email, department, year)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (name, dob, phone, email, department, year)

    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()

    return "Student registered successfully!"


@app.route("/students")
def students():
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("students.html", students=data)


if __name__ == "__main__":
    app.run(debug=True, port=8080)