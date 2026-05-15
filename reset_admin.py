from app import app, db, User, bcrypt

with app.app_context():
    db.create_all()

    # Check if admin exists
    admin = User.query.filter_by(email='admin@primelend.com').first()

    if admin:
        print("Admin exists. Resetting password...")
        admin.password_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin.is_admin = True
        db.session.commit()
        print("✅ Admin password reset to: admin123")
    else:
        print("Creating new admin account...")
        from datetime import datetime
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@primelend.com',
            phone='(555) 000-0000',
            date_of_birth=datetime(1990, 1, 1),
            annual_income=0,
            password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin=True,
            is_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created: admin@primelend.com / admin123")

    print("\nAll users in database:")
    for u in User.query.all():
        print(f"  - {u.email} (Admin: {u.is_admin})")
