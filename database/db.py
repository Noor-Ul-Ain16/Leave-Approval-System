import psycopg2
from psycopg2 import pool
import os
import sys
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

db_pool = None

if not DATABASE_URL:
    print("CRITICAL ERROR: DATABASE_URL is not set.", file=sys.stderr)
else:
    try:
        db_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=DATABASE_URL,
            sslmode="require"
        )
        print("Database connection pool initialized successfully.")
    except psycopg2.DatabaseError as e:
        print(f"CRITICAL ERROR: Failed to initialize DB pool: {e}", file=sys.stderr)
        db_pool = None


# ----------------------------
# LOW-LEVEL ACCESS (optional)
# ----------------------------
def get_connection():
    if db_pool is None:
        raise psycopg2.DatabaseError("DB pool is not initialized.")

    return db_pool.getconn()


def release_connection(conn):
    if db_pool and conn:
        db_pool.putconn(conn)


# ----------------------------
# SAFE CONTEXT MANAGER (USE THIS)
# ----------------------------
@contextmanager
def db_connection():
    """
    Safe DB connection handler.
    Automatically returns connection to pool even if error occurs.
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        release_connection(conn)