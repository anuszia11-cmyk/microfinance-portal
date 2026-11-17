# 🌿 GreenLeaf Microfinance – Mock Lending Portal

**Task 2 of the *Secure Microfinance Lending Portal – Hardening, Testing, Detection & Deployment* project**
Client: GreenLeaf Microfinance Cooperative (fictional) · Intern: Anas Zia · Ezitech Cyber Security Internship

A small **Flask + SQLite** web portal where borrowers can register, log in, see a list of borrowers, and open a borrower's detail page at `/borrower/<id>`. Passwords are stored as **bcrypt hashes**, and the database comes with **10 sample borrowers**.

> ⚠️ **This version is intentionally vulnerable.**
> The `/borrower/<id>` page checks that you are logged in, but **not** whether the record belongs to you. Any logged-in user can view another borrower's national ID and loan balance just by changing the number in the URL. This is an **IDOR (Insecure Direct Object Reference)** bug, left in on purpose as required by the project brief. It will be demonstrated and fixed in **Task 3**.

All names and national IDs in this project are fictional demo data.

---

## Table of contents

1. [Features](#features)
2. [Tech stack](#tech-stack)
3. [Project structure](#project-structure)
4. [How to run it](#how-to-run-it)
5. [Demo accounts](#demo-accounts)
6. [Pages and routes](#pages-and-routes)
7. [Database design](#database-design)
8. [How it works](#how-it-works)
9. [Running the tests](#running-the-tests)
10. [Security notes](#security-notes)
11. [Screenshots](#screenshots)
12. [Task 2 checklist](#task-2-checklist)
13. [What I did and why](#what-i-did-and-why)
14. [Next steps](#next-steps)

---

## Features

| Feature | Details |
|---|---|
| **Registration** | Username, full name, national ID (CNIC format `12345-1234567-1`), password and confirm password. Creates a new borrower with a PKR 0 balance and a linked login. |
| **Login / logout** | Session-based login. Passwords are checked with bcrypt. Logout clears the session. |
| **Password storage** | Only bcrypt hashes (`$2b$12$...`) are stored – never the real password. |
| **Borrower dashboard** | Lists all borrowers with ID, name and loan balance, plus total count and total outstanding. Your own row is marked **You**. |
| **Borrower detail page** | `/borrower/<id>` shows borrower ID, full name, national ID, loan balance and loan status. |
| **Sample data** | `init_db.py` loads 10 borrowers, each with a demo login. |
| **Automated tests** | 10 pytest tests covering login, registration, password hashing and pages. |

## Tech stack

| Tool | Used for |
|---|---|
| Python 3.11+ | Programming language |
| Flask | Web framework (routes, sessions, templates) |
| SQLite | Database stored in a single file (`greenleaf.db`) |
| bcrypt | Password hashing |
| Jinja2 | HTML templates (comes with Flask) |
| HTML / CSS | Page layout and styling |
| pytest | Automated tests |
| Git / GitHub | Version control |

## Project structure

```
greenleaf-lending-portal/
├── app.py              # Flask app: routes, login logic, sessions, database helpers
├── passwords.py        # hash_password() and check_password() using bcrypt
├── init_db.py          # Creates the database and loads 10 sample borrowers
├── schema.sql          # Table definitions (borrowers, users)
├── requirements.txt    # Python packages to install
├── pytest.ini          # pytest settings
├── .gitignore          # Keeps venv, database and secrets out of Git
├── templates/          # Jinja2 HTML templates
│   ├── base.html       #   shared layout: header, flash messages, footer
│   ├── login.html      #   login form
│   ├── register.html   #   registration form
│   ├── dashboard.html  #   list of all borrowers
│   ├── borrower.html   #   one borrower's details
│   └── error.html      #   error page (404)
├── static/
│   └── style.css       # Styling
├── tests/
│   └── test_app.py     # Automated tests
└── docs/
    └── screenshots/    # Proof screenshots used in this README
```

## How to run it

### Windows (PowerShell / VS Code terminal)

```powershell
# 1. Get the code
git clone https://github.com/<your-username>/greenleaf-lending-portal.git
cd greenleaf-lending-portal

# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install the packages
pip install -r requirements.txt

# 4. Create the database with sample data
python init_db.py

# 5. Start the app
flask run
```

> If activation fails with *"running scripts is disabled"*, run
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again.

### Linux / macOS

```bash
git clone https://github.com/<your-username>/greenleaf-lending-portal.git
cd greenleaf-lending-portal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
flask run
```

Then open **<http://127.0.0.1:5000>** in your browser. Stop the app with **Ctrl + C**.

**Notes**

- Step 4 is optional: if `greenleaf.db` is missing, the app creates and fills it automatically on the first request.
- Running `python init_db.py` again **deletes all data** and starts fresh.
- To keep users logged in after restarting the app, set a fixed secret key before `flask run`:
  - Windows: `$env:SECRET_KEY="put-a-long-random-string-here"`
  - Linux/macOS: `export SECRET_KEY="put-a-long-random-string-here"`

## Demo accounts

Every sample borrower has a login. All demo accounts use the password **`GreenLeaf@123`**.

| Username | Borrower ID | Name | Loan balance |
|---|---|---|---|
| `borrower1` | 1 | Ayesha Khan | PKR 45,000 |
| `borrower2` | 2 | Bilal Ahmed | PKR 120,000 |
| `borrower3` | 3 | Fatima Noor | PKR 75,500 |
| `borrower4` | 4 | Usman Tariq | PKR 30,000 |
| `borrower5` | 5 | Sana Iqbal | PKR 0 |
| `borrower6` | 6 | Hamza Raza | PKR 98,000 |
| `borrower7` | 7 | Zainab Ali | PKR 60,250 |
| `borrower8` | 8 | Imran Shah | PKR 150,000 |
| `borrower9` | 9 | Maryam Javed | PKR 22,000 |
| `borrower10` | 10 | Ahmed Hassan | PKR 85,000 |

You can also create your own account on the **Register** page.

## Pages and routes

| Method | URL | Login needed | What it does |
|---|---|---|---|
| GET | `/` | – | Goes to the dashboard if logged in, otherwise to the login page |
| GET, POST | `/register` | – | Shows the registration form / creates a new account |
| GET, POST | `/login` | – | Shows the login form / logs the user in |
| GET | `/logout` | – | Logs out (clears the session) |
| GET | `/dashboard` | ✅ | Lists all borrowers |
| GET | `/borrower/<id>` | ✅ | Shows one borrower's details (**no ownership check yet – see Task 3**) |

## Database design

**`borrowers`** – one row per borrower

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key, auto-increment |
| `full_name` | TEXT | Required |
| `national_id` | TEXT | Required, unique (CNIC format) |
| `loan_balance` | INTEGER | Outstanding amount in whole PKR (integers avoid rounding errors with money) |

**`users`** – one row per login account

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key, auto-increment |
| `username` | TEXT | Required, unique |
| `password_hash` | TEXT | bcrypt hash – never the plain password |
| `borrower_id` | INTEGER | Links the login to its borrower (`borrowers.id`), unique |
| `created_at` | TEXT | Set automatically |

Each login account belongs to exactly one borrower. Login data and financial data are kept in separate tables.

## How it works

**Registration**
1. The form data is validated on the server: username format, CNIC format, password length (8 characters to 72 bytes) and matching passwords.
2. The password is hashed with bcrypt.
3. A new borrower (balance PKR 0) and a linked user are saved in **one transaction**, so both are saved or neither is.
4. A duplicate username or national ID is rejected with a friendly message.

**Login**
1. The user is looked up by username with a parameterized query.
2. bcrypt checks the typed password against the stored hash.
3. On success, the session is cleared and then filled with `user_id`, `username` and `borrower_id`.
4. On failure, the same message is shown whether the username or the password was wrong.

**Sessions**
Flask stores the session in a cookie **signed** with `SECRET_KEY`. Users can't change the cookie without breaking the signature. Pages that need a login use a `@login_required` decorator that sends visitors to the login page.

**Templates**
All pages extend `base.html`. Jinja2 automatically escapes every value it prints, which protects against cross-site scripting (XSS).

## Running the tests

With the virtual environment active:

```bash
pytest -v
```

| Test | Checks that… |
|---|---|
| `test_sample_data_has_10_borrowers` | the database contains 10 sample borrowers |
| `test_login_page_loads` | the login page opens |
| `test_dashboard_requires_login` | visitors who aren't logged in are sent to the login page |
| `test_demo_user_can_log_in_and_see_all_borrowers` | a demo user can log in and see all borrowers |
| `test_wrong_password_is_rejected` | a wrong password is refused |
| `test_unknown_user_gets_same_error` | an unknown username gets the same error message |
| `test_register_stores_bcrypt_hash_not_plain_password` | registration stores a bcrypt hash, not the password |
| `test_duplicate_username_is_rejected` | the same username can't be registered twice |
| `test_borrower_detail_shows_correct_data` | the detail page shows the correct name, CNIC and balance |
| `test_missing_borrower_returns_404` | a borrower ID that doesn't exist returns 404 |

## Security notes

### Protections in this version

| Protection | Why it matters |
|---|---|
| **bcrypt password hashing** (random salt, cost factor 12) | If the database is stolen, attackers get slow-to-crack hashes, not passwords. The same password never gives the same hash. |
| **Parameterized SQL queries** (`?` placeholders) everywhere | User input can't change the SQL command, which prevents SQL injection. |
| **Same login error message** + dummy bcrypt check for unknown users | Attackers can't find out which usernames exist, either from the message or from the response time. |
| **Session cleared on login and logout** | Prevents old session data being reused (session fixation). |
| **HttpOnly and SameSite=Lax session cookie** | JavaScript can't read the cookie (helps against XSS), and most cross-site requests don't send it (helps against CSRF). |
| **Secret key from an environment variable** | No secrets are stored in the code or on GitHub. |
| **Server-side input validation** | Browser checks can be bypassed with tools like curl or Postman, so the server checks everything again. |
| **Jinja2 auto-escaping** | User-supplied text is shown as text, not run as code. |
| **`.gitignore` excludes the database and `.env`** | Password hashes, personal data and secrets never reach GitHub. |

### Known gaps (planned for later tasks)

| Gap | Fixed in |
|---|---|
| `/borrower/<id>` has no ownership check (IDOR) | **Task 3** |
| Loan search endpoint and SQL injection testing | **Task 4** |
| Logging of failed logins and an alert dashboard | **Task 5** |
| HTTPS and the secure cookie flag on the live site | **Task 6** |
| CSRF tokens on forms and login rate limiting | Future improvement |

## Screenshots

### Login page
![Login page](docs/screenshots/01-login.png)

### Registration page
![Registration page](docs/screenshots/02-register.png)

### Dashboard (logged in as `borrower1`)
![Dashboard](docs/screenshots/03-dashboard.png)

### Borrower detail page (`/borrower/1`)
![Borrower detail](docs/screenshots/04-borrower-detail.png)

### Passwords stored as bcrypt hashes
![Hashed passwords in the database](docs/screenshots/05-hashed-passwords.png)

### All tests passing
![pytest results](docs/screenshots/06-tests-passing.png)

## Task 2 checklist

| Mentor check | Status | Where to find it |
|---|---|---|
| Repository contains `app.py`, templates, `requirements.txt` and runs with `flask run` | ✅ | Project root, `templates/`, [How to run it](#how-to-run-it) |
| Registration and login work, passwords are stored hashed | ✅ | `/register`, `/login`, `passwords.py`, screenshot 05 |
| Borrower list and detail pages show correct sample data | ✅ | `/dashboard`, `/borrower/<id>`, `init_db.py`, screenshots 03–04 |
| Initial version does **not** enforce record ownership | ✅ (on purpose) | `borrower_detail()` in `app.py` – fixed in Task 3 |

## What I did and why

I built a small Flask + SQLite lending portal for GreenLeaf Microfinance with user registration, login, a borrower dashboard and a `/borrower/<id>` detail page, and I loaded 10 sample borrowers using a seed script. Passwords are hashed with bcrypt so that a database leak would not expose real passwords, and every SQL query uses parameters to prevent SQL injection. Each login account is linked to one borrower record, which Task 3 will use to check ownership. As the brief requires, the detail page does not check record ownership yet, so any logged-in user can view another borrower's data by changing the ID in the URL. I will demonstrate and fix this IDOR vulnerability in Task 3.

## Next steps

- **Task 3** – Prove the IDOR bug with curl/Postman, write `IDOR_report.md`, add a 403 check and a pytest for it.
- **Task 4** – Add a `/search?name=` endpoint, demonstrate SQL injection, then fix it with parameterized queries.
- **Task 5** – JSON logging, a detection script running as a systemd service, and an alerts dashboard.
- **Task 6** – Deploy to PythonAnywhere, record a demo video and write the client handover note.

---

*Demo project for training purposes. All borrower data is fictional.*# microfinance-portal
