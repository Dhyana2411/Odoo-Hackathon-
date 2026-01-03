# HRMS Frontend - Human Resource Management System

A complete web-based Human Resource Management System with role-based access control.

## 🌐 Website Structure & Navigation

### Entry Points
- **index.html** - Main landing page with welcome message and navigation to sign in/up
- **sign in.html** - User authentication page
- **sign up.html** - User registration page

### Dashboard Pages
- **After Sign in.html** - Main employee dashboard (works for both HR and Employee roles)
- **My Profile for Admin.html** - User profile management page
- **attendances list of Admin.html** - Admin view for managing all employee attendance
- **attendances list of employee.html** - Employee view for personal attendance tracking
- **Timeoff.html** - Time-off request management (leave management)

## 🔐 Authentication System

### User Roles
- **Employee** - Basic user with limited access
- **HR / Admin** - Administrative user with full access

### Features
- Automatic login ID generation (format: OI[FirstName][LastName][Year][Serial])
- Role-based navigation and access control
- Persistent login state using localStorage
- Secure logout functionality

## 🧭 Navigation Flow

```
index.html (Landing Page)
    ↓
sign in.html ←→ sign up.html
    ↓
After Sign in.html (Dashboard)
    ├── My Profile for Admin.html
    ├── attendances list of Admin.html (HR only)
    ├── attendances list of employee.html (Employee view)
    └── Timeoff.html
```

## 📁 File Structure

```
my frontend/
├── index.html                          # Landing page
├── sign in.html                        # Login page
├── sign up.html                        # Registration page
├── After Sign in.html                  # Main dashboard
├── My Profile for Admin.html           # Profile management
├── attendances list of Admin.html     # Admin attendance view
├── attendances list of employee.html  # Employee attendance view
├── Timeoff.html                        # Leave management
├── style.css                           # Main stylesheet
├── auth.js                             # Authentication logic
├── navigation.js                       # Navigation & common functions
└── README.md                           # This file
```

## 🚀 Getting Started

1. **Start Here**: Open `index.html` in your web browser
2. **Create Account**: Click "Sign Up" to create a new user account
3. **Choose Role**: Select either "Employee" or "HR / Admin" during registration
4. **Login**: Use the generated login ID and your password to sign in
5. **Navigate**: Use the top navigation bar to access different sections

## ✨ Key Features

### Authentication
- User registration with role selection
- Automatic login ID generation
- Secure login with role validation
- Persistent session management

### Dashboard
- Role-based navigation
- Employee status tracking (Check In/Out/Leave)
- Real-time status indicators
- User profile management

### Attendance Management
- Admin can view all employee attendance
- Employees can track personal attendance
- Time tracking with work hours calculation
- Search and filter functionality

### Leave Management
- Time-off request submission
- Approval/rejection workflow
- Leave type categorization (Paid/Sick)
- Leave balance tracking

## 🎨 Design Features

- **Dark Theme**: Modern dark UI design
- **Responsive**: Bootstrap-based responsive layout
- **Interactive**: Dynamic status indicators and real-time updates
- **User-Friendly**: Intuitive navigation and clear visual hierarchy

## 🔧 Technical Details

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Framework**: Bootstrap 5.3.2
- **Storage**: localStorage for data persistence
- **Authentication**: Client-side role-based access control
- **Navigation**: Single-page application feel with multi-page structure

## 📱 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🎯 Usage Tips

1. **First Time**: Start with `index.html` for the best experience
2. **Demo Data**: Create test accounts with different roles to explore features
3. **Navigation**: Use the top navigation bar to move between sections
4. **Logout**: Always use the logout button to properly end your session
5. **Role Testing**: Create both Employee and HR accounts to see different views

## 🔄 Data Flow

All user data is stored in browser localStorage:
- `users` - Array of registered users
- `currentUser` - Currently logged-in user information

This allows the system to work offline and maintain state between sessions.

---

**Note**: This is a frontend-only implementation. For production use, integrate with a proper backend API and database system.