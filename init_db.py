"""
Create the SQLite database and load sample data.

Usage:
    python init_db.py

WARNING: this deletes any existing data in greenleaf.db and starts fresh.
All names and national IDs below are fictional demo data.
"""

import os
import sqlite3

from passwords import hash_password

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.environ.get("DATABASE", os.path.join(BASE_DIR, "greenleaf.db"))
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")

# Every demo account (borrower1 ... borrower10) uses this password.
DEMO_PASSWORD = "GreenLeaf@123"

# (full name, national ID, outstanding loan balance in PKR)
SAMPLE_BORROWERS = [
    ("Ayesha Khan",   "91101-2345671-2",  45000),
    ("Bilal Ahmed",   "91202-3456782-1", 120000),
    ("Fatima Noor",   "91303-4567893-4",  75500),
    ("Usman Tariq",   "91404-5678904-3",  30000),
    ("Sana Iqbal",    "91505-6789015-6",      0),
    ("Hamza Raza",    "91606-7890126-5",  98000),
    ("Zainab Ali",    "91707-8901237-8",  60250),
    ("Imran Shah",    "91808-9012348-7", 150000),
    ("Maryam Javed",  "91909-0123459-0",  22000),
    ("Ahmed Hassan",  "92010-1234560-9",  85000),
]


def create_database(db_path: str = DEFAULT_DB) -> None:
    """Build the tables from schema.sql and insert the 10 sample borrowers.

    Each borrower also gets a demo login: borrower1 -> borrower 1, etc.
    """
    conn = sqlite3.connect(db_path)
    try:
        with open(SCHEMA_FILE, encoding="utf-8") as schema:
            conn.executescript(schema.read())

        with conn:  # one transaction: all rows are saved, or none are
            for number, (name, national_id, balance) in enumerate(SAMPLE_BORROWERS, start=1):
                cursor = conn.execute(
                    "INSERT INTO borrowers (full_name, national_id, loan_balance) "
                    "VALUES (?, ?, ?)",
                    (name, national_id, balance),
                )
                conn.execute(
                    "INSERT INTO users (username, password_hash, borrower_id) "
                    "VALUES (?, ?, ?)",
                    (f"borrower{number}", hash_password(DEMO_PASSWORD), cursor.lastrowid),
                )
    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
    print(f"Database created at {DEFAULT_DB}")
    print(f"Loaded {len(SAMPLE_BORROWERS)} sample borrowers.")
    print(f"Demo logins: borrower1 ... borrower{len(SAMPLE_BORROWERS)}  /  password: {DEMO_PASSWORD}")