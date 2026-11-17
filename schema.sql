-- GreenLeaf Microfinance - database schema (SQLite)
-- Running this file wipes the old tables and creates fresh ones.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS borrowers;

-- One row per borrower (a person who has taken a loan).
CREATE TABLE borrowers (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     TEXT    NOT NULL,
    national_id   TEXT    NOT NULL UNIQUE,
    loan_balance  INTEGER NOT NULL DEFAULT 0
);

-- One row per login account. Each account belongs to exactly one borrower.
CREATE TABLE users (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    username       TEXT    NOT NULL UNIQUE,
    password_hash  TEXT    NOT NULL,
    borrower_id    INTEGER NOT NULL UNIQUE,
    created_at     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (borrower_id) REFERENCES borrowers (id)
);