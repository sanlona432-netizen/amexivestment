# AmexIvestment — Professional American Loan Platform

A complete full-stack loan website with user registration, loan applications, admin dashboard, and real database.

## Features

- **User Registration** — Full signup with email, phone, DOB, income
- **User Login** — Secure authentication with password hashing
- **Loan Application** — Apply for Personal, Auto, Home Equity, Student Refi loans
- **Live Calculator** — Real-time payment estimation
- **User Dashboard** — Track loans, payments, stats
- **Admin Panel** — Manage users, approve/reject/fund loans, view messages
- **Contact Form** — Customers can send inquiries
- **Responsive Design** — Works on all devices

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

### 3. Initialize Database (first time)
```bash
flask init-db
```

### 4. Open in Browser
```
http://localhost:5000
```

## Default Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@amexivestment.com | admin123 |

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (upgrade to PostgreSQL for production)
- **Auth:** Flask-Login + Bcrypt
- **Frontend:** HTML5, CSS3, JavaScript (no framework needed)
- **Styling:** Custom CSS with CSS variables
- **Icons:** Font Awesome 6

## Production Deployment

### Option 1: PythonAnywhere (Free)
1. Upload files to PythonAnywhere
2. Set up virtual environment
3. Configure WSGI file
4. Done!

### Option 2: Heroku
```bash
heroku create primelend-app
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### Option 3: VPS (DigitalOcean, Linode)
1. Install Python, Nginx, Gunicorn
2. Clone repo
3. Set up systemd service
4. Configure Nginx reverse proxy

## File Structure

```
primelend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── amexinvestment.db           # SQLite database (auto-created)
├── templates/
│   ├── index.html         # Homepage
│   ├── register.html      # Sign up
│   ├── login.html         # Sign in
│   ├── dashboard.html     # User dashboard
│   ├── apply.html         # Loan application
│   ├── profile.html       # User profile
│   ├── admin.html         # Admin panel
│   ├── 404.html           # Not found page
│   └── 500.html           # Server error page
└── static/
    ├── css/
    ├── js/
    └── images/
```

## License

MIT License — Free for commercial use.
