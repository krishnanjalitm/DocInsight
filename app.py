from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/")
def home():
    return "DocInsight is running!"


@app.route("/register", methods=["GET" , "POST"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)


        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, hashed_password)
        )

        connection.commit()
        connection.close()

        print("User registered successfully!")



        # print("Name:", name)
        # print("Email:", email)
        # # print("Password:", password)
        # print("Hashed password:", hashed_password)

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
            return "Login successful!"

        return "Invalid email or password!"

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

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)