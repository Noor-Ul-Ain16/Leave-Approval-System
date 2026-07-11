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
- Receive email notifications when leave requests are approved or rejected.

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
- Transactional email notifications powered by the **Brevo Email API**.

---

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Jinja2 Templates
- **Database:** PostgreSQL / MySQL
- **Authentication:** Flask Sessions
- **Email Service:** Brevo Email API
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

**Windows:**

```bash
venv\Scripts\activate
```

**Mac / Linux:**

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

BREVO_API_KEY=your_brevo_api_key
SENDER_EMAIL=your_verified_sender@example.com
SENDER_NAME=Leave Approval System
```

> **Security Warning:** Never commit your `.env` file to version control. It contains sensitive credentials such as your database URL, secret key, and Brevo API key. Ensure `.env` is included in your `.gitignore`.

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

- **Environment Isolation:** Sensitive data (secret keys, credentials, and API keys) are strictly isolated into environment variables.
- **Credential Safety:** Passwords are securely hashed before storage (never stored in plain text).
- **Session Integrity:** Secured session-based authentication prevents unauthorized context switching.
- **Route Protection:** Explicit role-based access restrictions protect sensitive administrative endpoints.

---

## Future Improvements

- REST API expansion for potential mobile or frontend framework integration.
- Containerization utilizing Docker for seamless deployment.
- Dashboard analytics and leave reporting.

---

## Developer

Developed as a technical portfolio project to demonstrate proficiency in Python/Flask backend architecture, secure authentication patterns, relational database design, and integration with third-party APIs.

---

## License

This project is open-source and intended purely for educational and personal portfolio evaluations.
