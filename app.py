from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


# Function to create a database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="swathi2008",
        database="student_management"
    )


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER STUDENT ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    # Show registration page
    if request.method == "GET":
        return render_template("register.html")

    # Get data from HTML form
    name = request.form.get("name", "").strip()
    age = request.form.get("age", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "")
    year = request.form.get("year", "")

    # ---------- VALIDATION ----------

    if not name or not name.replace(" ", "").isalpha():
        return "Invalid name. Please enter a valid name."

    if not age.isdigit() or int(age) < 1 or int(age) > 100:
        return "Invalid age."

    if not phone.isdigit() or len(phone) != 10:
        return "Invalid phone number. Enter 10 digits."

    if "@" not in email or "." not in email:
        return "Invalid email address."

    if department not in ["CSE", "ECE", "EEE", "Mechanical", "Civil"]:
        return "Invalid department."

    if year not in ["1", "2", "3", "4"]:
        return "Invalid year."


    # ---------- DATABASE ----------

    db = get_db_connection()
    cursor = db.cursor()

    # Check duplicate email or phone
    cursor.execute(
        "SELECT * FROM students WHERE email = %s OR phone = %s",
        (email, phone)
    )

    existing_student = cursor.fetchone()

    if existing_student:
        cursor.close()
        db.close()
        return "Email or phone number is already registered."


    # Insert student
    else:
        query = """
            INSERT INTO students
            (name, age, phone, email, department, year)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            name,
            int(age),
            phone,
            email,
            department,
            year
        )

        cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()

    return "Student registered successfully!"


# ---------------- VIEW STUDENTS ----------------

@app.route("/students")
def students():

    search = request.args.get("search", "").strip()

    db = get_db_connection()
    cursor = db.cursor()

    if search:
        query = """
            SELECT * FROM students
            WHERE name LIKE %s
            OR email LIKE %s
            OR phone LIKE %s
            OR department LIKE %s
        """

        value = "%" + search + "%"

        cursor.execute(
            query,
            (value, value, value, value)
        )

    else:
        cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "students.html",
        students=data,
        search=search
    )


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True, port=8080)