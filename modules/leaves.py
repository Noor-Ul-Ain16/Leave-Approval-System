from flask import Blueprint, session, redirect, url_for, render_template, request
from database.db import db_connection, get_connection
from utils.helpers import get_display_status
from psycopg2.extras import RealDictCursor
from datetime import date, datetime
import math

leave_bp = Blueprint("leave", __name__)


# =========================================================
# MY REQUESTS (EMPLOYEE) + PAGINATION
# =========================================================
@leave_bp.route('/my_requests')
def my_requests():
    if session.get('role') != 'employee':
        return redirect(url_for('auth.employee_login'))

    user_id = session.get('user_id')

    search = request.args.get('search', '').strip().lower()
    filter_by = request.args.get('filter_by', 'leave_type')

    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    with db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # =========================
        # COUNT QUERY
        # =========================
        count_query = """
            SELECT COUNT(*)
            FROM leaves
            WHERE user_id = %s
        """
        count_params = [user_id]

        if search:

            if filter_by == "leave_type":
                count_query += " AND LOWER(leave_type) LIKE %s"
                count_params.append(f"%{search}%")

            elif filter_by == "status":

                if search == "on-leave":
                    count_query += """
                        AND status = 'approved'
                        AND CURRENT_DATE BETWEEN start_date AND end_date
                    """

                elif search == "completed":
                    count_query += """
                        AND status = 'approved'
                        AND end_date < CURRENT_DATE
                    """

                else:
                    count_query += " AND LOWER(status) LIKE %s"
                    count_params.append(search)

        cursor.execute(count_query, tuple(count_params))
        total_records = cursor.fetchone()["count"]

        # =========================
        # DATA QUERY
        # =========================
        data_query = """
            SELECT
                leave_id,
                leave_type,
                start_date,
                end_date,
                status,
                created_at
            FROM leaves
            WHERE user_id = %s
        """
        data_params = [user_id]

        if search:

            if filter_by == "leave_type":
                data_query += " AND LOWER(leave_type) LIKE %s"
                data_params.append(f"%{search}%")

            elif filter_by == "status":

                if search == "on-leave":
                    data_query += """
                        AND status = 'approved'
                        AND CURRENT_DATE BETWEEN start_date AND end_date
                    """

                elif search == "completed":
                    data_query += """
                        AND status = 'approved'
                        AND end_date < CURRENT_DATE
                    """

                else:
                    data_query += " AND LOWER(status) LIKE %s"
                    data_params.append(search)

        data_query += """
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        data_params.extend([per_page, offset])

        cursor.execute(data_query, tuple(data_params))
        requests = cursor.fetchall()

    # =========================
    # DISPLAY STATUS FIX
    # =========================
    for req in requests:
        req["status"] = get_display_status(
            req["status"],
            req["start_date"],
            req["end_date"]
        )

    total_pages = math.ceil(total_records / per_page)

    return render_template(
        "display_requests.html",
        requests=requests,
        role=session.get('role'),
        user_name=session.get('user_name'),
        name="My Leave Requests",
        mode="view_employee_requests",
        page=page,
        total_pages=total_pages,
        search=search,
        filter_by=filter_by
    )
# =========================================================
# ALL REQUESTS (ADMIN) + PAGINATION
# =========================================================
@leave_bp.route('/all_requests')
def all_requests():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.admin_login'))

    search = request.args.get('search', '').strip().lower()
    filter_by = request.args.get('filter_by', 'name')

    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    with db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # =========================
        # COUNT QUERY
        # =========================
        count_query = """
            SELECT COUNT(*)
            FROM leaves l
            JOIN users u ON l.user_id = u.user_id
            WHERE 1=1
        """
        count_params = []

        # =========================
        # DATA BASE QUERY
        # =========================
        data_query = """
            SELECT
                l.leave_id,
                u.name,
                l.leave_type,
                l.start_date,
                l.end_date,
                l.status,
                l.created_at
            FROM leaves l
            JOIN users u ON l.user_id = u.user_id
            WHERE 1=1
        """
        data_params = []

        # =========================
        # FILTER LOGIC
        # =========================
        if search:

            # ---------------- NAME ----------------
            if filter_by == "name":
                count_query += " AND LOWER(u.name) LIKE %s"
                data_query += " AND LOWER(u.name) LIKE %s"
                count_params.append(f"%{search}%")
                data_params.append(f"%{search}%")

            # ---------------- LEAVE TYPE ----------------
            elif filter_by == "leave_type":
                count_query += " AND LOWER(l.leave_type) LIKE %s"
                data_query += " AND LOWER(l.leave_type) LIKE %s"
                count_params.append(f"%{search}%")
                data_params.append(f"%{search}%")

            # ---------------- STATUS + COMPUTED STATES ----------------
            elif filter_by == "status":

                if search == "on-leave":
                    condition = """
                        AND l.status = 'approved'
                        AND CURRENT_DATE BETWEEN l.start_date AND l.end_date
                    """
                    count_query += condition
                    data_query += condition

                elif search == "completed":
                    condition = """
                        AND l.status = 'approved'
                        AND l.end_date < CURRENT_DATE
                    """
                    count_query += condition
                    data_query += condition

                else:
                    count_query += " AND LOWER(l.status) LIKE %s"
                    data_query += " AND LOWER(l.status) LIKE %s"
                    count_params.append(search)
                    data_params.append(search)

        # =========================
        # EXECUTE COUNT
        # =========================
        cursor.execute(count_query, tuple(count_params))
        total_records = cursor.fetchone()["count"]

        # =========================
        # PAGINATION DATA
        # =========================
        data_query += " ORDER BY l.created_at DESC LIMIT %s OFFSET %s"
        data_params.extend([per_page, offset])

        cursor.execute(data_query, tuple(data_params))
        requests = cursor.fetchall()

    # =========================
    # DISPLAY STATUS FIX
    # =========================
    for req in requests:
        req["status"] = get_display_status(
            req["status"],
            req["start_date"],
            req["end_date"]
        )

    total_pages = math.ceil(total_records / per_page)

    return render_template(
        "display_requests.html",
        requests=requests,
        role=session.get('role'),
        user_name=session.get('user_name'),
        name="All Leave Requests",
        page=page,
        total_pages=total_pages,
        search=search,
        filter_by=filter_by
    )

# =========================================================
# REQUEST DETAILS
# =========================================================
@leave_bp.route('/leave/<int:leave_id>')
def request_details(leave_id):
    if 'user_id' not in session:
        return redirect(url_for('main.home'))

    user_id = session.get('user_id')
    role = session.get('role')

    with db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if role == 'employee':
            cursor.execute("""
                SELECT l.*, u.name, u.email
                FROM leaves l
                JOIN users u ON l.user_id = u.user_id
                WHERE l.leave_id = %s AND l.user_id = %s
            """, (leave_id, user_id))
        else:
            cursor.execute("""
                SELECT l.*, u.name, u.email
                FROM leaves l
                JOIN users u ON l.user_id = u.user_id
                WHERE l.leave_id = %s
            """, (leave_id,))

        request_data = cursor.fetchone()

    return render_template(
        'request_details.html',
        request=request_data,
        role=role,
        user_name=session.get('user_name')
    )


# =========================================================
# REQUEST LEAVE
# =========================================================
@leave_bp.route('/request_leave', methods=['GET', 'POST'])
def request_leave():
    if session.get('role') != 'employee':
        return redirect(url_for('auth.employee_login'))

    if request.method == 'POST':
        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']

        user_id = session.get('user_id')

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        today = date.today()

        if start_date_obj < today:
            return render_template(
                'request_leave.html',
                role=session.get('role'),
                user_name=session.get('user_name'),
                message="You cannot apply for past dates."
            )

        if start_date_obj > end_date_obj:
            return render_template(
                'request_leave.html',
                role=session.get('role'),
                user_name=session.get('user_name'),
                message="Invalid date range."
            )

        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT COUNT(*) AS count
            FROM leaves
            WHERE user_id = %s
              AND LOWER(status) = 'pending'
        """, (user_id,))

        if cursor.fetchone()["count"] > 0:
            cursor.close()
            conn.close()

            return render_template(
                'request_leave.html',
                role=session.get('role'),
                user_name=session.get('user_name'),
                message="You already have a pending request."
            )

        cursor.execute("""
            INSERT INTO leaves
            (user_id, leave_type, start_date, end_date, reason, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            leave_type,
            start_date,
            end_date,
            reason,
            'pending'
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('leave.my_requests'))

    return render_template(
        "request_leave.html",
        role=session.get('role'),
        user_name=session.get('user_name')
    )


# =========================================================
# APPROVE REQUESTS (ADMIN) + PAGINATION
# =========================================================
@leave_bp.route('/approve_requests')
def approve_requests():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.admin_login'))

    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    with db_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # COUNT
        cursor.execute("""
            SELECT COUNT(*) AS count
            FROM leaves
            WHERE LOWER(status) = 'pending'
        """)
        total_records = cursor.fetchone()["count"]

        # DATA
        cursor.execute("""
            SELECT
                l.leave_id,
                u.name,
                l.leave_type,
                l.start_date,
                l.end_date,
                l.status,
                l.created_at
            FROM leaves l
            JOIN users u ON l.user_id = u.user_id
            WHERE LOWER(l.status) = 'pending'
            ORDER BY l.created_at DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))

        requests = cursor.fetchall()

    total_pages = math.ceil(total_records / per_page)

    return render_template(
        "display_requests.html",
        requests=requests,
        role=session.get('role'),
        user_name=session.get('user_name'),
        name="Approve Requests",
        mode="approve_requests",
        page=page,
        total_pages=total_pages
    )


# =========================================================
# HANDLE APPROVE / REJECT
# =========================================================
@leave_bp.route("/leave/<int:leave_id>/action", methods=["POST"])
def handle_leave_action(leave_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth.admin_login'))

    action = request.form["action"]
    remarks = request.form.get("remarks", "")
    admin_id = session.get("user_id")

    if action not in ["approve", "reject"]:
        return redirect(url_for("leave.request_details", leave_id=leave_id))

    status = "approved" if action == "approve" else "rejected"

    with db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE leaves
            SET status = %s,
                admin_remarks = %s,
                admin_id = %s,
                action_date = CURRENT_TIMESTAMP
            WHERE leave_id = %s
        """, (status, remarks, admin_id, leave_id))

        conn.commit()

    return redirect(url_for("leave.request_details", leave_id=leave_id))