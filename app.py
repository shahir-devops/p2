from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "/data/users.db"


def get_db_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_db_connection()
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

# ✅ Insert user
@app.route("/home", methods=["POST"])
def home():
    try:
        data = request.json

        if not data or "name" not in data or "phone" not in data or "email" not in data:
            return {"error": "Invalid input"}, 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, phone, email) VALUES (?, ?, ?)",
            (data["name"], data["phone"], data["email"])
        )

        conn.commit()
        conn.close()

        return {"message": "User added successfully"}, 201

    except Exception as e:
        return {"error": str(e)}, 500


# ✅ Get users
@app.route("/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
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

    except Exception as e:
        return {"error": str(e)}, 500


# ✅ Health check (important for Kubernetes)
@app.route("/health")
def health():
    return {"status": "UP"}


# Optional info endpoint
@app.route("/services")
def service():
    return "We store user data in DB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)