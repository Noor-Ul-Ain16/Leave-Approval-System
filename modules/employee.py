from flask import Blueprint,session,redirect, url_for,render_template
from database.db import db_connection
from psycopg2.extras import RealDictCursor
from utils.helpers import get_display_status

employee_bp = Blueprint("employee", __name__)

# ---------------- EMPLOYEE DASHBOARD ----------------
@employee_bp.route('/employee/dashboard')
def employee_dashboard():
    if session.get('role') != 'employee':
        return redirect(url_for('auth.employee_login'))

    user_id = session.get('user_id')

    with db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT status, COUNT(*) AS count
            FROM leaves
            WHERE user_id = %s
            GROUP BY status
        """, (user_id,))

        rows = cursor.fetchall()

        counts = {"pending": 0, "approved": 0, "rejected": 0}

        for row in rows:
            status = row["status"]
            count = row["count"]

            if status:
                counts[status.lower()] = count

        cursor.execute("""
            SELECT
                leave_type AS leave_type,
                start_date AS start_date,
                end_date AS end_date,
                status AS status,
                leave_id AS leave_id
            FROM leaves
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id,))

        latest = cursor.fetchone()

    if latest:
        display_status = get_display_status(
            latest["status"],
            latest["start_date"],
            latest["end_date"]
        )

        latest = (
            latest["leave_type"],
            latest["start_date"],
            latest["end_date"],
            display_status,
            latest["leave_id"]
        )

    return render_template(
        "employee_dashboard.html",
        counts=counts,
        latest=latest,
        role=session.get('role'),
        user_name=session.get('user_name')
    )
