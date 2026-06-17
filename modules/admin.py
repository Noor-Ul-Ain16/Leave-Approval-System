from flask import Blueprint,session,redirect, url_for,render_template
from database.db import db_connection
from utils.helpers import get_display_status
from psycopg2.extras import RealDictCursor

admin_bp = Blueprint("admin", __name__)

# ---------------- ADMIN DASHBOARD ----------------
@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.admin_login'))

    with db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) AS total_count
            FROM leaves
            WHERE LOWER(status) = 'approved'
              AND CURRENT_DATE BETWEEN start_date AND end_date
        """)
        total_count = cursor.fetchone()["total_count"]

        cursor.execute("""
            SELECT status, COUNT(*) AS count
            FROM leaves
            GROUP BY status
        """)
        rows = cursor.fetchall()

        counts = {"pending": 0, "approved": 0, "rejected": 0}

        for row in rows:
            status = row["status"]
            count = row["count"]

            if status:
                key = status.strip().lower()

                if key in counts:
                    counts[key] = count

        cursor.execute("""
            SELECT
                l.leave_id AS leave_id,
                u.name AS name,
                l.leave_type AS leave_type,
                l.start_date AS start_date,
                l.end_date AS end_date,
                l.status AS status,
                l.admin_remarks AS admin_remarks
            FROM leaves l
            JOIN users u ON u.user_id = l.user_id
            ORDER BY
                CASE
                    WHEN LOWER(l.status) = 'pending' THEN 1
                    ELSE 2
                END,
                l.created_at DESC
            LIMIT 3
        """)

        requests = cursor.fetchall()

    for req in requests:
        req["status"] = get_display_status(
            req["status"],
            req["start_date"],
            req["end_date"]
        )

    return render_template(
        "admin_dashboard.html",
        role=session.get('role'),
        user_name=session.get('user_name'),
        total_count=total_count,
        counts=counts,
        requests=requests
    )
