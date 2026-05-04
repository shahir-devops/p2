from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "/data/users.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/home", methods=["POST"])
def home():
    data = request.json

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, phone, email) VALUES (?, ?, ?)",
        (data["name"], data["phone"], data["email"])
    )

    conn.commit()
    conn.close()

    return {"message": "User added sucessfully"}

@app.route("/users", methods=["GET"])
def get_users():
    conn =sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "email": row[3]
        })
        return jsonify(users)

@app.route("/services")
def service():
    return "we used to save the data from the users"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)