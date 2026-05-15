from app import app, db, User, bcrypt
from datetime import datetime

print("=" * 50)
print("PRIMELEND ADMIN ACCOUNT FIX")
print("=" * 50)
print()

with app.app_context():
    # Create all tables
    db.create_all()
    print("[1/3] Database tables created/verified")

    # Check for existing admin
    admin = User.query.filter_by(email='admin@amexinvestment.com').first()

    if admin:
        print("[2/3] Admin account found — resetting password...")
        admin.password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin.is_admin = True
        db.session.commit()
        print("[3/3] Admin password reset to: admin123")
    else:
        print("[2/3] Creating new admin account...")
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@amexinvestment.com',
            phone='(555) 000-0000',
            date_of_birth=datetime(1990, 1, 1),
            annual_income=0,
            password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True,
            is_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        print("[3/3] Admin account created!")

    print()
    print("=" * 50)
    print("DONE!")
    print("=" * 50)
    print()
    print("Login credentials:")
    print("  Email:    admin@amexinvestment.com")
    print("  Password: admin123")
    print()
    print("All users in database:")
    for u in User.query.all():
        role = "ADMIN" if u.is_admin else "User"
        print(f"  - {u.email} ({role})")
    print()
    print("Now run: py app.py")
    print("Then go to: http://localhost:5000")
    print()

input("Press Enter to exit...")
