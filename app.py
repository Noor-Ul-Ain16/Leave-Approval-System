from flask import Flask
from dotenv import load_dotenv
from datetime import timedelta
import os

from modules.main import main_bp
from modules.auth import auth_bp
from modules.employee import employee_bp
from modules.admin import admin_bp
from modules.leaves import leave_bp

from utils.error_handlers import register_error_handlers

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# LINES FOR HUGGING FACE COMPATIBILITY ---
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'None'

# ---------------- SESSION CONFIG ----------------

app.permanent_session_lifetime = timedelta(hours=2)

# ---------------- ERROR HANDLERS ----------------

register_error_handlers(app)

# ---------------- BLUEPRINTS ----------------

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(leave_bp)

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)