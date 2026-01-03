from flask import Flask, request, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os

# Import the database from models.py
from models import db, User, Attendance, Salary

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackathon_dayflow_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dayflow.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize Extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Refers to the login function below

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- DATABASE SETUP ---
# Run this once to create the empty database file
with app.app_context():
    db.create_all()

# ==========================================
# BACKEND LOGIC ROUTES
# ==========================================

@app.route('/signup_logic', methods=['POST'])
def signup_logic():
    # 1. Get Data from Form
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    company_name = request.form.get('company_name')

    # 2. Logic: Handle Logo Upload
    logo_filename = None
    if 'company_logo' in request.files:
        file = request.files['company_logo']
        if file.filename != '':
            logo_filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))

    # 3. Logic: Generate Custom ID (OI + Initials + Year + Serial)
    year = datetime.now().year
    count = User.query.count() + 1
    serial = str(count).zfill(4)
    initials = name[:2].upper()
    generated_id = f"OI{initials}{year}{serial}"

    # 4. Save to Database
    new_user = User(
        name=name, email=email, password=password, role=role,
        company_name=company_name, company_logo=logo_filename,
        custom_id=generated_id
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/login_logic', methods=['POST'])
def login_logic():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.password == password:
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        return "Login Failed"

@app.route('/calculate_salary', methods=['POST'])
@login_required
def calculate_salary():
    if current_user.role != 'hr':
        return "Access Denied"

    employee_id = request.form.get('employee_id')
    wage = float(request.form.get('monthly_wage'))
    
    # 1. Math Logic (As per your requirements)
    basic = wage * 0.50
    hra = basic * 0.50
    pf = basic * 0.12
    pt = 200.0
    net = wage - pf - pt
    
    # 2. Save or Update in Database
    emp = User.query.get(employee_id)
    salary_rec = Salary.query.filter_by(user_id=emp.id).first()
    
    if not salary_rec:
        salary_rec = Salary(user_id=emp.id)
    
    salary_rec.monthly_wage = wage
    salary_rec.basic_salary = basic
    salary_rec.hra = hra
    salary_rec.pf = pf
    salary_rec.net_salary = net
    
    db.session.add(salary_rec)
    db.session.commit()
    
    return redirect(url_for('dashboard'))

# --- PLACEHOLDERS FOR FRONTEND ---
# (These just tell Flask which HTML file to open. 
# You need to put your teammate's files in a 'templates' folder later.)

@app.route('/')
def home():
    return render_template('login.html') # Teammate's file

@app.route('/login')
def login():
    return render_template('login.html') # Teammate's file

@app.route('/signup')
def signup():
    return render_template('signup.html') # Teammate's file

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user) # Teammate's file

if __name__ == '__main__':
    app.run(debug=True)