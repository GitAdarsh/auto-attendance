import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Supabase DB credentials
DB_HOST = https://zzktygkmiihnmknsfxfl.supabase.co  # Supabase se copy karo
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "0bhufAKVj69n2bKd"  # Supabase project banate time dala tha
DB_PORT = "5432"

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

@app.route('/api/tap', methods=['POST'])
def tap_card():
    data = request.json
    card_uid = data.get("card_uid")
    student_id = data.get("student_id")
    status = "present"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO attendance (student_id, card_uid, status) VALUES (%s, %s, %s)",
        (student_id, card_uid, status)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok", "message": "Attendance marked"})

if __name__ == '__main__':
    app.run(debug=True)

