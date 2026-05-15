from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from datetime import datetime
import os
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'amexinvestment-secret-key-2026-secure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///amexinvestment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email config - Zoho Mail (FREE professional email)
# Sign up at: https://www.zoho.com/mail/
app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'support@amexivestment.com'  # Your Zoho email
app.config['MAIL_PASSWORD'] = 'YOUR_ZOHO_APP_PASSWORD'  # Generate in Zoho settings

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
mail = Mail(app)


import requests

def verify_recaptcha(token):
    """Verify Google reCAPTCHA v2/v3 response"""
    secret_key = 'YOUR_RECAPTCHA_SECRET_KEY'  # Replace with your key
    if not secret_key or secret_key == 'YOUR_RECAPTCHA_SECRET_KEY':
        return True  # Skip if not configured

    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': secret_key, 'response': token}
    )
    result = response.json()
    return result.get('success', False)

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    annual_income = db.Column(db.Float, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    ssn_last4 = db.Column(db.String(4))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    employment_status = db.Column(db.String(50))
    employer_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    loans = db.relationship('Loan', backref='applicant', lazy=True)
    documents = db.relationship('Document', backref='owner', lazy=True)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    loan_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    term_months = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    monthly_payment = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')  # pending, approved, funded, paid_off, rejected
    credit_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    funded_at = db.Column(db.DateTime)

    payments = db.relationship('Payment', backref='loan', lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    paid_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')  # pending, paid, late

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)  # id, paystub, bank_statement, w2
    filename = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Verify reCAPTCHA
        recaptcha_token = request.form.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_token):
            flash('Please complete the security check.', 'error')
            return redirect(url_for('register'))

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d')
        income = float(request.form.get('income').replace(',', '').replace('$', ''))
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please sign in.', 'error')
            return redirect(url_for('login'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=dob,
            annual_income=income,
            password_hash=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        # Send welcome email
        try:
            msg = Message('Welcome to AmexIvestment!', 
                         sender='support@amexivestment.com',
                         recipients=[email])
            msg.body = f"""Hi {first_name},

Welcome to AmexIvestment! Your account has been created successfully.

You can now:
- Check your personalized loan rates
- Apply for loans up to $100,000
- Track your applications in real-time

Get started: {url_for('login', _external=True)}

Best regards,
The AmexIvestment Team"""
            mail.send(msg)
        except:
            pass

        flash('Account created successfully! Please sign in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    loans = Loan.query.filter_by(user_id=current_user.id).order_by(Loan.created_at.desc()).all()

    total_borrowed = sum(loan.amount for loan in loans if loan.status in ['approved', 'funded'])
    active_loans = [loan for loan in loans if loan.status == 'funded']
    monthly_payment = sum(loan.monthly_payment for loan in active_loans)

    return render_template('dashboard.html', 
                         loans=loans,
                         total_borrowed=total_borrowed,
                         monthly_payment=monthly_payment,
                         active_loans_count=len(active_loans))

@app.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    if request.method == 'POST':
        loan_type = request.form.get('loan_type')
        amount = float(request.form.get('amount'))
        term = int(request.form.get('term'))
        purpose = request.form.get('purpose')

        # Calculate rate based on credit score (simplified)
        credit_score = random.randint(620, 780)
        if credit_score >= 750:
            rate = 4.99
        elif credit_score >= 670:
            rate = 6.99
        elif credit_score >= 580:
            rate = 9.99
        else:
            rate = 14.99

        monthly_rate = rate / 100 / 12
        monthly_payment = (amount * monthly_rate) / (1 - (1 + monthly_rate) ** -term)

        loan = Loan(
            user_id=current_user.id,
            loan_type=loan_type,
            amount=amount,
            term_months=term,
            interest_rate=rate,
            monthly_payment=round(monthly_payment, 2),
            purpose=purpose,
            credit_score=credit_score,
            status='pending'
        )

        db.session.add(loan)
        db.session.commit()

        flash(f'Application submitted! Estimated rate: {rate}% APR', 'success')
        return redirect(url_for('dashboard'))

    return render_template('apply.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        current_user.city = request.form.get('city')
        current_user.state = request.form.get('state')
        current_user.zip_code = request.form.get('zip_code')
        current_user.employment_status = request.form.get('employment_status')
        current_user.employer_name = request.form.get('employer_name')
        current_user.ssn_last4 = request.form.get('ssn_last4')

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    subject = request.form.get('subject')
    message = request.form.get('message')

    msg = ContactMessage(name=name, email=email, phone=phone, subject=subject, message=message)
    db.session.add(msg)
    db.session.commit()

    flash('Message sent! We will contact you within 24 hours.', 'success')
    return redirect(url_for('index'))

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('dashboard'))

    users = User.query.order_by(User.created_at.desc()).all()
    loans = Loan.query.order_by(Loan.created_at.desc()).all()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()

    stats = {
        'total_users': User.query.count(),
        'total_loans': Loan.query.count(),
        'pending_loans': Loan.query.filter_by(status='pending').count(),
        'total_funded': sum(loan.amount for loan in Loan.query.filter_by(status='funded').all()),
        'unread_messages': ContactMessage.query.filter_by(is_read=False).count()
    }

    return render_template('admin.html', users=users, loans=loans, messages=messages, stats=stats)

@app.route('/admin/loan/<int:loan_id>/<action>')
@login_required
def admin_loan_action(loan_id, action):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403

    loan = Loan.query.get_or_404(loan_id)

    if action == 'approve':
        loan.status = 'approved'
        loan.approved_at = datetime.utcnow()
    elif action == 'fund':
        loan.status = 'funded'
        loan.funded_at = datetime.utcnow()

        # Create payment schedule
        for i in range(loan.term_months):
            payment = Payment(
                loan_id=loan.id,
                amount=loan.monthly_payment,
                due_date=datetime.utcnow().replace(day=1) + __import__('dateutil.relativedelta').relativedelta.relativedelta(months=i+1)
            )
            db.session.add(payment)
    elif action == 'reject':
        loan.status = 'rejected'

    db.session.commit()
    flash(f'Loan #{loan_id} {action}d successfully.', 'success')
    return redirect(url_for('admin'))

# ==================== API ENDPOINTS ====================

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json()
    amount = float(data.get('amount', 25000))
    term = int(data.get('term', 36))
    credit_tier = data.get('credit', 'good')

    rates = {'excellent': 0.0499, 'good': 0.0699, 'fair': 0.0999, 'building': 0.1499}
    rate = rates.get(credit_tier, 0.0699)

    monthly_rate = rate / 12
    payment = (amount * monthly_rate) / (1 - (1 + monthly_rate) ** -term)
    total_interest = payment * term - amount

    return jsonify({
        'monthly_payment': round(payment, 2),
        'apr': round(rate * 100, 2),
        'total_interest': round(total_interest, 2),
        'total_cost': round(amount + total_interest, 2)
    })

@app.route('/api/loan/<int:loan_id>')
@login_required
def api_loan_detail(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if loan.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403

    return jsonify({
        'id': loan.id,
        'type': loan.loan_type,
        'amount': loan.amount,
        'term': loan.term_months,
        'rate': loan.interest_rate,
        'monthly': loan.monthly_payment,
        'status': loan.status,
        'purpose': loan.purpose,
        'created': loan.created_at.strftime('%Y-%m-%d')
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ==================== INITIAL SETUP ====================

@app.cli.command('init-db')
def init_db():
    db.create_all()

    # Create admin user
    if not User.query.filter_by(email='admin@amexivestment.com').first():
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@amexivestment.com',
            phone='(555) 000-0000',
            date_of_birth=datetime(1990, 1, 1),
            annual_income=0,
            password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created: admin@amexivestment.com / admin123')

    print('Database initialized!')

def init_admin():
    """Create admin user if not exists"""
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@amexivestment.com').first():
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@amexivestment.com',
                phone='(555) 000-0000',
                date_of_birth=datetime(1990, 1, 1),
                annual_income=0,
                password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                is_admin=True,
                is_verified=True
            )
            db.session.add(admin)
            db.session.commit()
            print('✅ Admin account created: admin@amexivestment.com / admin123')
        else:
            print('✅ Admin account already exists')

if __name__ == '__main__':
    init_admin()
    print('🚀 Starting AmexIvestment...')
    print('📍 Open: http://localhost:5000')
    print('🔑 Admin: admin@amexivestment.com / admin123')
    print('')
    app.run(debug=True, host='0.0.0.0', port=5000)
