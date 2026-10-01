from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
from database import get_db_connection

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)