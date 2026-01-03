from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime, date
import os
import json

# Import the database from models.py
from models import db, User, Attendance, Salary

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hackathon_dayflow_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dayflow.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Enable CORS for frontend integration
CORS(app)

# Initialize Extensions
db.init_app(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- DATABASE SETUP ---
with app.app_context():
    db.create_all()

# ==========================================
# API ROUTES FOR FRONTEND INTEGRATION
# ==========================================

@app.route('/api/signup', methods=['POST'])
def api_signup():
    try:
        data = request.get_json()
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Generate custom ID
        year = datetime.now().year
        count = User.query.count() + 1
        serial = str(count).zfill(4)
        name_parts = data['name'].split()
        first = name_parts[0][:2].upper() if name_parts else "XX"
        last = name_parts[1][:2].upper() if len(name_parts) > 1 else "XX"
        generated_id = f"OI{first}{last}{year}{serial}"
        
        # Create new user
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=data['password'],  # In production, hash this!
            role=data['role'].lower(),
            company_name=data.get('company', ''),
            custom_id=generated_id
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'loginId': generated_id,
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email,
                'role': new_user.role,
                'company': new_user.company_name,
                'loginId': generated_id
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/signin', methods=['POST'])
def api_signin():
    try:
        data = request.get_json()
        
        # Find user by login ID or email
        user = User.query.filter(
            (User.custom_id == data['loginId']) | (User.email == data['loginId'])
        ).first()
        
        if user and user.password == data['password'] and user.role == data['role'].lower():
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role,
                    'company': user.company_name,
                    'loginId': user.custom_id,
                    'reliabilityScore': user.reliability_score,
                    'attendanceStreak': user.attendance_streak
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials or role mismatch'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/employees', methods=['GET'])
def api_get_employees():
    try:
        employees = User.query.all()
        employee_list = []
        
        for emp in employees:
            # Get latest attendance
            latest_attendance = Attendance.query.filter_by(
                user_id=emp.id, 
                date=date.today()
            ).first()
            
            status = 'absent'
            if latest_attendance:
                if latest_attendance.check_out:
                    status = 'checked_out'
                elif latest_attendance.check_in:
                    status = 'checked_in'
            
            employee_list.append({
                'id': emp.id,
                'name': emp.name,
                'email': emp.email,
                'role': emp.role,
                'company': emp.company_name,
                'loginId': emp.custom_id,
                'reliabilityScore': emp.reliability_score,
                'attendanceStreak': emp.attendance_streak,
                'status': status
            })
        
        return jsonify({'success': True, 'employees': employee_list})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/attendance', methods=['POST'])
def api_attendance():
    try:
        data = request.get_json()
        user_id = data['userId']
        action = data['action']  # 'check_in', 'check_out', 'leave'
        
        # Get or create today's attendance record
        today = date.today()
        attendance = Attendance.query.filter_by(user_id=user_id, date=today).first()
        
        if not attendance:
            attendance = Attendance(user_id=user_id, date=today)
        
        current_time = datetime.now()
        
        if action == 'check_in':
            attendance.check_in = current_time
            attendance.status = 'Present'
        elif action == 'check_out':
            if attendance.check_in:
                attendance.check_out = current_time
                # Calculate work hours
                work_duration = current_time - attendance.check_in
                attendance.work_hours = work_duration.total_seconds() / 3600
                attendance.status = 'Present'
        elif action == 'leave':
            attendance.status = 'Leave'
        
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'{action.replace("_", " ").title()} recorded successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/attendance/<int:user_id>', methods=['GET'])
def api_get_attendance(user_id):
    try:
        attendance_records = Attendance.query.filter_by(user_id=user_id).order_by(Attendance.date.desc()).all()
        
        records = []
        for record in attendance_records:
            records.append({
                'date': record.date.strftime('%Y-%m-%d'),
                'checkIn': record.check_in.strftime('%H:%M') if record.check_in else '',
                'checkOut': record.check_out.strftime('%H:%M') if record.check_out else '',
                'workHours': round(record.work_hours, 2) if record.work_hours else 0,
                'extraHours': round(record.extra_hours, 2) if record.extra_hours else 0,
                'status': record.status
            })
        
        return jsonify({'success': True, 'attendance': records})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/salary/<int:user_id>', methods=['GET', 'POST'])
def api_salary(user_id):
    try:
        if request.method == 'GET':
            salary = Salary.query.filter_by(user_id=user_id).first()
            if salary:
                return jsonify({
                    'success': True,
                    'salary': {
                        'monthlyWage': salary.monthly_wage,
                        'basicSalary': salary.basic_salary,
                        'hra': salary.hra,
                        'pf': salary.pf,
                        'professionalTax': salary.professional_tax,
                        'netSalary': salary.net_salary
                    }
                })
            else:
                return jsonify({'success': False, 'message': 'No salary information found'})
        
        elif request.method == 'POST':
            data = request.get_json()
            wage = float(data['monthlyWage'])
            
            # Calculate salary components
            basic = wage * 0.50
            hra = basic * 0.50
            pf = basic * 0.12
            pt = 200.0
            net = wage - pf - pt
            
            # Save or update salary
            salary = Salary.query.filter_by(user_id=user_id).first()
            if not salary:
                salary = Salary(user_id=user_id)
            
            salary.monthly_wage = wage
            salary.basic_salary = basic
            salary.hra = hra
            salary.pf = pf
            salary.professional_tax = pt
            salary.net_salary = net
            
            db.session.add(salary)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Salary updated successfully'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==========================================
# SERVE FRONTEND FILES
# ==========================================

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
