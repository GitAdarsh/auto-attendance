import psycopg2
from datetime import date

DB_HOST = "https://zzktygkmiihnmknsfxfl.supabase.co"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "0bhufAKVj69n2bKd"
DB_PORT = "5432"

def mark_absent():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cur = conn.cursor()

    # 1. All students
    cur.execute("SELECT student_id FROM students")
    all_students = {r[0] for r in cur.fetchall()}

    # 2. Already present today
    cur.execute("SELECT student_id FROM attendance WHERE DATE(timestamp) = %s", (date.today(),))
    present_students = {r[0] for r in cur.fetchall()}

    # 3. Calculate absent
    absent_students = all_students - present_students

    # 4. Insert absent
    for sid in absent_students:
        cur.execute(
            "INSERT INTO attendance (student_id, card_uid, status) VALUES (%s, %s, %s)",
            (sid, None, "absent")
        )

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    mark_absent()
    print("Auto absent marked for today!")

