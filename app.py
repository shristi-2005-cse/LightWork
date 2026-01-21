from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS services")
    cursor.execute("DROP TABLE IF EXISTS requests")

    cursor.execute("""
    CREATE TABLE services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider_name TEXT,
        store_name TEXT,
        service_name TEXT,
        price REAL,
        address TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        service_name TEXT,
        expected_price REAL,
        phone TEXT,
        status TEXT
    )
    """)

    db.commit()
    db.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    db = get_db()
    cursor = db.cursor()

    # ADD SERVICE
    if request.method == "POST" and request.form.get("form_type") == "add_service":
        cursor.execute("""
            INSERT INTO services
            (provider_name, store_name, service_name, price, address, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            request.form["provider_name"],
            request.form["store_name"],
            request.form["service_name"],
            request.form["price"],
            request.form["address"],
            request.form["phone"]
        ))
        db.commit()
        return redirect("/")

    # REQUEST SERVICE (THIS IS THE IMPORTANT PART)
    if request.method == "POST" and request.form.get("form_type") == "request_service":
        cursor.execute("""
            INSERT INTO requests
            (customer_name, service_name, expected_price, phone, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.form["customer_name"],
            request.form["service_name"],
            request.form["expected_price"],
            request.form["phone"],
            "Pending"
        ))
        db.commit()
        return redirect("/")

    # FETCH DATA
    cursor.execute("""
        SELECT provider_name, store_name, service_name, price, address, phone
        FROM services
        ORDER BY id DESC
    """)
    services = cursor.fetchall()

    cursor.execute("""
        SELECT customer_name, service_name, expected_price, phone, status
        FROM requests
        ORDER BY id DESC
    """)
    requests_data = cursor.fetchall()

    db.close()
    return render_template(
        "index.html",
        services=services,
        requests=requests_data
    )

if __name__ == "__main__":
    app.run(debug=True)
