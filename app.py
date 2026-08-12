from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "healthcare.db"


# Database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database and patient table
def create_database():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            disease TEXT,
            doctor TEXT,
            medicines TEXT
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Patient dashboard
@app.route("/dashboard")
def dashboard():

    conn = get_db()

    patients = conn.execute(
        "SELECT * FROM patients ORDER BY id DESC"
    ).fetchall()

    total_patients = conn.execute(
        "SELECT COUNT(*) FROM patients"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        patients=patients,
        total_patients=total_patients
    )


# Add patient
@app.route("/add-patient", methods=["GET", "POST"])
def add_patient():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        disease = request.form["disease"]
        doctor = request.form["doctor"]
        medicines = request.form["medicines"]

        conn = get_db()

        conn.execute("""
            INSERT INTO patients
            (name, age, gender, phone, disease, doctor, medicines)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            age,
            gender,
            phone,
            disease,
            doctor,
            medicines
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_patient.html")


# Search patient
@app.route("/search")
def search():

    query = request.args.get("query", "")

    conn = get_db()

    patients = conn.execute("""
        SELECT * FROM patients
        WHERE name LIKE ? OR phone LIKE ?
    """, (
        "%" + query + "%",
        "%" + query + "%"
    )).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        patients=patients,
        total_patients=len(patients)
    )


# Delete patient
@app.route("/delete/<int:patient_id>")
def delete_patient(patient_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM patients WHERE id = ?",
        (patient_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# Medicines
@app.route("/medicines")
def medicines():

    medicine_list = [
        {
            "name": "Paracetamol",
            "price": 30,
            "description": "For fever and pain"
        },
        {
            "name": "Vitamin C",
            "price": 80,
            "description": "Vitamin supplement"
        },
        {
            "name": "ORS",
            "price": 25,
            "description": "For hydration"
        },
        {
            "name": "Antacid",
            "price": 60,
            "description": "For acidity symptoms"
        },
        {
            "name": "Cough Syrup",
            "price": 120,
            "description": "For cough symptoms"
        }
    ]

    return render_template(
        "medicines.html",
        medicines=medicine_list
    )


# Exit page
@app.route("/exit")
def exit_page():
    return redirect(url_for("home"))


# Start application
if __name__ == "__main__":
    create_database()
    app.run(debug=True)