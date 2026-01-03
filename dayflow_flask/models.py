from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# 1. The User Table (Handles Login & Roles)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Auth Details
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'hr' or 'employee'
    
    # Company Details (For HR to upload)
    company_name = db.Column(db.String(100))
    company_logo = db.Column(db.String(200)) # Stores the filename of the logo
    
    # Custom Generated ID (e.g., OIJOH20260001)
    custom_id = db.Column(db.String(50), unique=True)
    
    # Gamification (The Unique Feature)
    reliability_score = db.Column(db.Integer, default=100)
    attendance_streak = db.Column(db.Integer, default=0)

    # Relationships
    attendance_records = db.relationship('Attendance', backref='employee', lazy=True)
    salary_info = db.relationship('Salary', backref='employee', uselist=False, lazy=True)

# 2. The Attendance Table
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    
    work_hours = db.Column(db.Float, default=0.0)
    extra_hours = db.Column(db.Float, default=0.0) # Overtime
    status = db.Column(db.String(20), default='Absent')

# 3. The Salary Table
class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Base Input
    monthly_wage = db.Column(db.Float, default=0.0)
    
    # Auto-Calculated Fields
    basic_salary = db.Column(db.Float, default=0.0)
    hra = db.Column(db.Float, default=0.0)
    pf = db.Column(db.Float, default=0.0)
    professional_tax = db.Column(db.Float, default=200.0)
    net_salary = db.Column(db.Float, default=0.0)