from flask import Blueprint, session, redirect, url_for, render_template, request
from utils.auth import check_credentials
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import re
import requests
from random import randint
from database.db import db_connection
import os

# ================= BLUEPRINT =================
auth_bp = Blueprint("auth", __name__)


# ---------------- BREVO MAIL HELPER ----------------
def send_brevo_email(to_email, subject, body_text):
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": os.getenv("BREVO_API_KEY"),
        "content-type": "application/json"
    }
    payload = {
        "sender": {"email": os.getenv("MAIL_USERNAME"), "name": "Leave System"},
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": body_text
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 201


# ---------------- PASSWORD STRENGTH ----------------
def is_strong_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return "Must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return "Must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Must contain at least one special character"
    return None


# ---------------- LOGIN HANDLER ----------------
def handle_login(role):
    if request.method == 'GET':
        return render_template('login.html', role=role)

    email = request.form['email']
    password = request.form['password']

    user = check_credentials(role, email, password)

    if user:
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        session['role'] = role

        if role == "admin":
            return redirect(url_for('admin.admin_dashboard'))
        return redirect(url_for('employee.employee_dashboard'))

    return render_template(
        'login.html',
        role=role,
        message="Invalid credentials or wrong portal"
    )


# ---------------- LOGOUT ----------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))


# ---------------- LOGIN ROUTES ----------------
@auth_bp.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    return handle_login('admin')


@auth_bp.route('/login/employee', methods=['GET', 'POST'])
def employee_login():
    return handle_login('employee')


# ---------------- CHANGE PASSWORD ----------------
@auth_bp.route("/change_password", methods=["GET", "POST"])
def change_password():

    if 'user_id' not in session:
        return redirect(url_for('main.home'))

    user_id = session.get('user_id')

    msg = session.pop("msg", None)
    update_status = session.pop("msg_type", None)

    if request.method == "POST":
        current = request.form["current_password"]
        new = request.form["new_password"]
        confirm = request.form["confirm_password"]

        with db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT password FROM users WHERE user_id = %s
            """, (user_id,))
            result = cursor.fetchone()

            if not result:
                session["msg"] = "User not found"
                session["msg_type"] = "error"
                return redirect(url_for("auth.change_password"))

            db_password = result["password"]

            if not check_password_hash(db_password, current):
                session["msg"] = "Current Password is Incorrect"
                session["msg_type"] = "error"
                return redirect(url_for("auth.change_password"))

            if new != confirm:
                session["msg"] = "Passwords do not match"
                session["msg_type"] = "error"
                return redirect(url_for("auth.change_password"))

            if check_password_hash(db_password, new):
                session["msg"] = "New password cannot be same as current password"
                session["msg_type"] = "error"
                return redirect(url_for("auth.change_password"))

            password_error = is_strong_password(new)
            if password_error:
                session["msg"] = password_error
                session["msg_type"] = "error"
                return redirect(url_for("auth.change_password"))

            hashed_new = generate_password_hash(new)

            cursor.execute("""
                UPDATE users SET password = %s WHERE user_id = %s
            """, (hashed_new, user_id))

            conn.commit()

        session["msg"] = "Password Updated Successfully!"
        session["msg_type"] = "success"
        return redirect(url_for("auth.change_password"))

    return render_template(
        "change_password.html",
        msg=msg,
        update_status=update_status,
        role=session.get('role'),
        user_name=session.get('user_name')
    )


# ---------------- FORGOT PASSWORD ----------------
@auth_bp.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():

    if request.method == "GET":
        return render_template("forgot_password.html", step="email")

    action = request.form.get("action")

    # ---------------- SEND OTP ----------------
    if action == "send_otp":
        email = request.form["email"]

        with db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

        if not user:
            return render_template("forgot_password.html",
                step="email",
                error="No account found with this email."
            )

        otp = str(randint(100000, 999999))

        session["reset_email"] = email
        session["reset_otp"] = otp
        session["otp_verified"] = False
        session.permanent = True

        send_brevo_email(
            to_email=email,
            subject="Leave System OTP",
            body_text=f"Your OTP is {otp}. Valid for 3 minutes."
        )

        return render_template("forgot_password.html",
            step="verify",
            success="OTP sent successfully!"
        )

    # ---------------- RESEND OTP ----------------
    elif action == "resend_otp":
        email = session.get("reset_email")

        if not email:
            return render_template("forgot_password.html",
                step="email",
                error="Session expired."
            )

        otp = str(randint(100000, 999999))
        session["reset_otp"] = otp

        send_brevo_email(
            to_email=email,
            subject="New OTP",
            body_text=f"Your NEW OTP is {otp}"
        )

        return render_template("forgot_password.html",
            step="verify",
            success="New OTP sent!"
        )

    # ---------------- VERIFY OTP ----------------
    elif action == "verify_otp":
        entered_otp = request.form["otp"]

        if entered_otp != session.get("reset_otp"):
            return render_template("forgot_password.html",
                step="verify",
                error="Invalid OTP."
            )

        session["otp_verified"] = True

        return render_template("forgot_password.html",
            step="change_password",
            success="OTP verified!"
        )

    # ---------------- CHANGE PASSWORD ----------------
    elif action == "change_password":

        if not session.get("otp_verified"):
            return redirect(url_for("auth.forgot_password"))

        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        error = is_strong_password(new_password)
        if error:
            return render_template("forgot_password.html",
                step="change_password",
                error=error
            )

        if new_password != confirm_password:
            return render_template("forgot_password.html",
                step="change_password",
                error="Passwords do not match."
            )

        email = session.get("reset_email")
        hashed = generate_password_hash(new_password)

        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET password = %s WHERE email = %s
            """, (hashed, email))
            conn.commit()

        session.clear()

        return render_template("forgot_password.html",
            step="email",
            success="Password reset successful!"
        )