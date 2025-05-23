from flask_mysqldb import MySQL

mysql = MySQL()

def create_user(cursor, email, password_hash):
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password_hash))

def get_user_by_email(cursor, email):
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone()
