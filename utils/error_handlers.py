# utils/error_handlers.py
import psycopg2
from flask import render_template, session

def register_error_handlers(app):

    
    @app.errorhandler(psycopg2.DatabaseError)
    def handle_database_error(error):
        """
        Catches all PostgreSQL connectivity drops, transaction block deadlocks, 
        or execution structural syntax faults cleanly.
        """
        # Flushes raw error logs out to your terminal container console for easy debugging
        print(f"\n[SERVER CRITICAL ERROR] Database Exception Triggered:\n{error}\n", flush=True)
    
        return render_template(
            "error.html",
            title="Database Connection Error",
            message="We are experiencing temporary difficulties communicating with our secure database infrastructure. Your current transaction data was safely aborted. Please reload or try again in a few moments.",
            role=session.get('role'),
            user_name=session.get('user_name')
        ), 500

    @app.errorhandler(404)
    def handle_not_found_error(error):
        """Gracefully captures invalid URLs or dropped endpoint parameters."""
        return render_template(
            "error.html",
            title="Page Not Found",
            message="The page link or resource identifier you are trying to reach doesn't exist, has changed directories, or is temporarily offline.",
            role=session.get('role'),
            user_name=session.get('user_name')
        ), 404
 
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handles request verbs mismatches (e.g., performing raw browser GETs on POST workflows)."""
        return render_template(
            "error.html",
            title="Action Not Allowed",
            message="The application controller rejected the request verification parameters. Please navigate the dashboard panels using the official user interface forms.",
            role=session.get('role'),
            user_name=session.get('user_name')
        ), 405

    @app.errorhandler(Exception)
    def handle_all_unhandled_exceptions(error):
        """
        The Ultimate Safety Mesh. Intercepts any programming syntax drops or unexpected 
        system state crashes across the app environment.
        """
        print(f"\n[SERVER CRITICAL ERROR] Internal Execution Engine Failure:\n{error}\n", flush=True)
    
        # 🚨 THE FIX: Clear the broken session state so the user isn't trapped in a loop!
        session.clear() 
    
        return render_template(
            "error.html",
            title="Application Exception",
            message="An unexpected logic calculation or process synchronization anomaly occurred on our internal servers. Your active session has been safely cleared to prevent loops. Please log in again.",
            role=None,       # Set to None since we cleared the session
            user_name=None   # Set to None since we cleared the session
        ), 500
