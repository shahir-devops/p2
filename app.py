from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

DB_PATH = "/data/users.db"


def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_db()
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

# 🔹 HTML FORM
form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>User Form</title>
</head>
<body>
    <h2>Add User</h2>
    <form method="post">
        Name: <input type="text" name="name"><br><br>
        Phone: <input type="text" name="phone"><br><br>
        Email: <input type="text" name="email"><br><br>
        <button type="submit">Submit</button>
    </form>
    <br>
    <a href="/users">View Users</a>
</body>
</html>
"""

# 🔹 HOME PAGE (GET + POST)
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email)
        )
        conn.commit()
        conn.close()

        return "<h3>User added successfully</h3><a href='/home'>Go Back</a>"

    return render_template_string(form_html)


# 🔹 USERS PAGE (HTML TABLE)
@app.route("/users")
def users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()

    html = "<h2>User List</h2><table border=1><tr><th>ID</th><th>Name</th><th>Phone</th><th>Email</th></tr>"
    for r in rows:
        html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    html += "</table><br><a href='/home'>Add More</a>"

    return html


# 🔹 HEALTH
@app.route("/health")
def health():
    return {"status": "UP"}


@app.route("/services")
def service():
        html = "<h1>We store user data in DB</h1>"
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)