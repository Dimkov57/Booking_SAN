import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host     = os.getenv("DB_HOST",     "localhost"),
        port     = os.getenv("DB_PORT",     "5432"),
        dbname   = os.getenv("DB_NAME",     "booking_san"),
        user     = os.getenv("DB_USER",     "postgres"),
        password = os.getenv("DB_PASSWORD", ""),
    )

def get_all_users():
    conn = get_connection()
    cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT u.student_id, u.first_name, u.last_name,
               u.first_name || ' ' || u.last_name AS name,
               u.email, f.name AS faculty, u.password,
               TO_CHAR(u.joined, 'YYYY-MM-DD') AS joined
        FROM users u JOIN faculties f ON f.faculty_id = u.faculty_id
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return {row["student_id"]: dict(row) for row in rows}

def create_user(student_id, first_name, last_name, email, faculty, password_hash, joined):
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO users (student_id, first_name, last_name, email, faculty_id, password, joined)
            VALUES (%s, %s, %s, %s, (SELECT faculty_id FROM faculties WHERE name = %s), %s, %s)
        """, (student_id, first_name, last_name, email, faculty, password_hash, joined))
        conn.commit(); cur.close(); conn.close()
        return True
    except psycopg2.IntegrityError:
        conn.rollback(); conn.close()
        return False

def update_user(student_id, first_name, last_name, email, faculty):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""
        UPDATE users SET first_name=%s, last_name=%s, email=%s,
               faculty_id=(SELECT faculty_id FROM faculties WHERE name=%s)
        WHERE student_id=%s
    """, (first_name, last_name, email, faculty, student_id))
    conn.commit(); cur.close(); conn.close()

def update_password(student_id, new_password_hash):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE users SET password=%s WHERE student_id=%s", (new_password_hash, student_id))
    conn.commit(); cur.close(); conn.close()

def get_all_bookings():
    conn = get_connection()
    cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT b.booking_id AS id,
               u.first_name || ' ' || u.last_name AS name,
               b.student_id, u.email, f.name AS faculty, b.purpose,
               b.room_id AS room,
               TO_CHAR(b.booking_date, 'YYYY-MM-DD') AS date,
               ts.label AS slot,
               TO_CHAR(b.booked_at, 'YYYY-MM-DD HH24:MI') AS booked_at
        FROM bookings b
        JOIN users u ON u.student_id = b.student_id
        JOIN faculties f ON f.faculty_id = u.faculty_id
        JOIN time_slots ts ON ts.slot_id = b.slot_id
        WHERE b.cancelled_at IS NULL
        ORDER BY b.booking_date, ts.start_time
    """)
    rows = cur.fetchall(); cur.close(); conn.close()
    return [dict(row) for row in rows]

def add_booking(booking):
    try:
        conn = get_connection(); cur = conn.cursor()
        # Перевіряємо чи знайшовся слот
        cur.execute("""
            INSERT INTO bookings (booking_id, student_id, room_id, slot_id, booking_date, purpose, booked_at)
            SELECT %s, %s, %s, slot_id, %s::date, %s, %s::timestamptz
            FROM time_slots WHERE replace(label, '–', '-') = replace(%s, '–', '-')
        """, (booking["id"], booking["student_id"], booking["room"],
              booking["date"], booking.get("purpose", "Not specified"),
              booking.get("booked_at"), booking["slot"]))
        
        if cur.rowcount == 0:
            conn.rollback(); cur.close(); conn.close()
            return False  # слот не знайдено в БД
            
        conn.commit(); cur.close(); conn.close()
        return True
    except psycopg2.IntegrityError:
        conn.rollback(); conn.close()
        return False

def cancel_booking(booking_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE bookings SET cancelled_at = NOW() WHERE booking_id = %s", (booking_id,))
    conn.commit(); cur.close(); conn.close()