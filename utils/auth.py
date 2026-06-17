from database.db import db_connection
from werkzeug.security import check_password_hash


def check_credentials(role, email, password):

    with db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, name, email, password, role
            FROM users
            WHERE email = %s AND role = %s
        """, (email, role))

        user = cursor.fetchone()

    if not user:
        return None

    db_password = user[3]

    if check_password_hash(db_password, password):
        return user

    return None