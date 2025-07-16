from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime
import subprocess

app = Flask(__name__)

# ✅ MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="xxx",
        password="xxxx",
        database="xxxxx"
    )

# ✅ Dashboard route
@app.route("/", methods=["GET"])
def dashboard():
    sentiment_filter = request.args.get("sentiment")
    sender_filter = request.args.get("sender")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = "SELECT * FROM emails WHERE 1=1"
    params = []

    if sentiment_filter:
        query += " AND sentiment = %s"
        params.append(sentiment_filter)

    if sender_filter:
        query += " AND sender LIKE %s"
        params.append(f"%{sender_filter}%")

    if start_date:
        query += " AND DATE(received_at) >= %s"
        params.append(start_date)

    if end_date:
        query += " AND DATE(received_at) <= %s"
        params.append(end_date)

    query += " ORDER BY received_at DESC"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params)
        emails = cursor.fetchall()

        sentiment_counts = {
            "positive": sum(1 for e in emails if e["sentiment"] == "positive"),
            "negative": sum(1 for e in emails if e["sentiment"] == "negative"),
            "neutral": sum(1 for e in emails if e["sentiment"] == "neutral"),
        }

        return render_template("dashboard.html",
            emails=emails,
            sentiment_counts=sentiment_counts,
            selected_sentiment=sentiment_filter,
            selected_sender=sender_filter,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        print("❌ Error loading dashboard:", e)
        return "Internal Server Error", 500
    finally:
        cursor.close()
        conn.close()

# ✅ Delete an email
@app.route('/delete/<int:email_id>', methods=['POST'])
def delete_email(email_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM emails WHERE id = %s", (email_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

# ✅ Manual refresh (runs process.py)
@app.route("/refresh", methods=["POST"])
def refresh_emails():
    try:
        subprocess.run(["python3", "process.py"], check=True)
    except Exception as e:
        print("❌ Error running process.py:", e)
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True, port=5090)
