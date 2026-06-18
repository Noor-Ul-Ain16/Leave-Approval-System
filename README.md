---
title: Leave Approval System
emoji: 📝
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: app.py
pinned: false
---

# Leave Approval System
My Flask and Supabase application deployed on Hugging Face Spaces.

# Leave Approval System

A full-stack web-based Leave Approval System built with Flask. The application streamlines the process of leave requests within an organization by enabling employees to submit requests and administrators to review, approve, or reject them efficiently.

---

## Overview

This system is designed to simplify leave management workflows by providing:

- **Role-based access control** (Admin & Employee)
- **Centralized leave request handling**
- **Secure authentication system**
- **Structured and scalable backend architecture**

---

## Key Features

### Employee Features
- Secure registration and login.
- Submit leave requests with specific details (dates, reason, type).
- View real-time status of submitted requests (Pending/Approved/Rejected).
- Track comprehensive personal leave history.

### Admin Features
- Secure admin authentication.
- Centralized dashboard to view all employee leave requests.
- One-click approve or reject functionality.
- Detailed drill-down into employee request histories.

### System & Architecture Features
- Session-based authentication and route protection.
- Role-based authorization middleware.
- Modular architectural design using **Flask Blueprints**.
- Environment-based configuration (`.env` support).
- Database agnostic connection layer (compatible with PostgreSQL/MySQL).

---

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Jinja2 Templates
- **Database:** PostgreSQL / MySQL
- **Authentication:** Flask Sessions
- **Database Connector:** Psycopg2 / MySQL Connector
- **Environment Management:** python-dotenv

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/leave-approval-system.git
cd leave-approval-system
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

* **Windows:**
  ```bash
  venv\Scripts\activate
  ```
* **Mac / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project:

```env
SECRET_KEY=your_secure_random_secret_key
DATABASE_URL=your_database_connection_url

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_app_specific_password
```

>  **Security Warning:** Never commit the `.env` file to version control. Ensure it is included in your `.gitignore`.

### 5. Run the Application

```bash
python app.py
```

Once running, access the local development server at:
```text
http://127.0.0.1:5000/
```

---

## Security Practices

- **Environment Isolation:** Sensitive data (secret keys, credentials) are strictly isolated into environment variables.
- **Credential Safety:** Passwords are securely hashed before storage (never stored in plain text).
- **Session Integrity:** Secured session-based authentication prevents unauthorized context switching.
- **Route Protection:** Explicit role-based access restrictions protect sensitive administrative endpoints.

---

## Future Improvements

- Automated email notification triggers upon request approval or rejection.
- REST API expansion for potential mobile or frontend framework integration.
- Containerization utilizing Docker for seamless deployment.

---

## Developer

Developed as a technical portfolio project to demonstrate proficiency in Python/Flask backend architecture, secure authentication patterns, and structured relational database design.

---

## License

This project is open-source and intended purely for educational and personal portfolio evaluations.
