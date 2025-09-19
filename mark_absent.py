import os
import pymysql

DB = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
    'db': os.environ.get('DB_NAME'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def get_conn():
    return pymysql.connect(**DB, cursorclass=pymysql.cursors.DictCursor)

schema = """
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200),
  roll_no VARCHAR(50),
  card_uid VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attendance (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  card_uid VARCHAR(100) NOT NULL,
  status ENUM('present','absent','late') NOT NULL DEFAULT 'present',
  timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  attendance_date DATE NOT NULL,
  device_id VARCHAR(100),
  UNIQUE KEY unique_student_date (student_id, attendance_date),
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);
"""

def run():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            for stmt in schema.split(';'):
                s = stmt.strip()
                if s:
                    cur.execute(s + ';')
        conn.commit()
        print("✅ Tables created/verified.")
    finally:
        conn.close()

if __name__ == "__main__":
    run()
