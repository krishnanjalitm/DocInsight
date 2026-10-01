from database import get_db_connection

connection = get_db_connection()

users = connection.execute("SELECT * FROM users").fetchall()

for user in users:
    print(dict(user))

connection.close()