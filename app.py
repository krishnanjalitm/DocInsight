from pdf_processor import extract_text_from_pdf
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from flask import flash
from werkzeug.utils import secure_filename
import os
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = "dev-secret-key"
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "DocInsight is running!"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()

        try:
            connection.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, hashed_password)
            )

            connection.commit()

        except sqlite3.IntegrityError:
            connection.close()
            flash("Email already registered. Please use another email.", "error")
            return redirect(url_for("register"))

        connection.close()

        flash("Registration successful! You can now login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["user_id"]
            session["name"] = user["name"]
            session["role"] = user["role"]
            
            return redirect(url_for("dashboard")) 

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session["name"],
        role=session["role"]
    )


@app.route("/upload", methods=["POST"])
def upload():

    if "user_id" not in session:
        return redirect(url_for("login"))

    file = request.files.get("document")

    if not file or file.filename == "":
        flash("Please select a PDF file.", "error")
        return redirect(url_for("dashboard"))

    if not file.filename.lower().endswith(".pdf"):
        flash("Only PDF files are allowed.", "error")
        return redirect(url_for("dashboard"))

    original_filename = secure_filename(file.filename)

    unique_filename = f"{session['user_id']}_{uuid.uuid4().hex}_{original_filename}"

    file.save(
        os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
    )

    file_path = os.path.join(
    app.config["UPLOAD_FOLDER"],
    unique_filename
    )

    extracted_text = extract_text_from_pdf(file_path)

    print("PDF text extracted successfully!")
    print(extracted_text[:1000])

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO documents (user_id, filename, extracted_text)
        VALUES (?, ?, ?)
        """,
        (session["user_id"], unique_filename, extracted_text)
    )

    connection.commit()
    connection.close()

    flash("PDF uploaded successfully!", "success")

    return redirect(url_for("dashboard"))


@app.route("/admin")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        return "Access denied! Admins only."

    return render_template(
        "admin_dashboard.html",
        name=session["name"],
        role=session["role"]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)