from flask import Flask
from dotenv import load_dotenv
from datetime import timedelta
import os

from extensions import mail

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

# ---------------- MAIL CONFIG ----------------

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail.init_app(app)

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