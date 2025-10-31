# Hostel Management System - Web Application

A modern, feature-rich web application for managing hostel accommodations, built with Flask, MySQL, and Bootstrap.

## 🌟 Features

### Core Functionality
- **User Authentication**: Secure login and registration system
- **Role-Based Access Control**: Admin and regular user roles with different permissions
- **Bed Management**: View, add, and remove bed allotments
- **Smart Bed Assignment**: Automatically assigns the next available bed
- **Student Information**: Track student ID, contact, email, and check-in dates

### Advanced Features
- **Search & Filter**: Search students by name, bed number, or student ID
- **Analytics Dashboard**: Real-time statistics (occupancy rate, payment status, etc.)
- **Payment Tracking**: Track payment status (Paid/Pending) for each allotment
- **Email Notifications**: Automatic email alerts for bed allocations and removals (optional)
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Professional UI**: Modern Bootstrap-based interface with intuitive navigation

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask 3.0
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3
- **Authentication**: Flask-Login
- **Email**: Flask-Mail (optional)
- **Security**: Password hashing with Werkzeug

## 📋 Prerequisites

- Python 3.7 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone or Navigate to Project Directory
```bash
cd hostel-accommodation-system
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Database Settings

Create a `.env` file in the project root (or update `config.py` directly):

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password_here
MYSQL_DATABASE=mydb
MYSQL_PORT=3306

SECRET_KEY=your-secret-key-here-change-this

# Optional: Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@hostel.com

# Hostel Configuration
TOTAL_BEDS=20
HOSTEL_FEE=5000
```

**Note**: For Gmail, you'll need to generate an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

### 4. Initialize Database

Run the database setup script:

```bash
python setup_database.py
```

This will:
- Create the database if it doesn't exist
- Create necessary tables (users, hostel)
- Migrate existing data from old schema (if any)
- Create a default admin user (username: `admin`, password: `admin123`)

**⚠️ Important**: Change the default admin password immediately after first login!

### 5. Run the Application

```bash
python app.py
```

Or using Flask command:
```bash
flask run
```

The application will be available at: `http://localhost:5000`

## 📖 Usage Guide

### First Time Setup

1. **Login**: Use the default admin credentials:
   - Username: `admin`
   - Password: `admin123`

2. **Register New Users**: 
   - Navigate to Register page
   - The first user registered automatically becomes admin
   - Subsequent users are regular users

3. **Change Admin Password** (Recommended):
   - After first login, update your password through database or code

### Managing Beds

#### Adding a Bed Allotment (Admin Only)
1. Go to **Bed Management** → Click **Allot New Bed**
2. Enter student information (Name is required, others optional)
3. System automatically assigns the next available bed number
4. Email notification is sent if email is provided and configured

#### Viewing Bed Allotments
- Navigate to **Bed Management** to see all current allotments
- View dashboard for quick statistics and recent allotments

#### Removing a Bed Allotment (Admin Only)
- Click the delete button (trash icon) next to any bed in Bed Management
- Confirmation dialog will appear before deletion

#### Updating Payment Status (Admin Only)
- Click the payment button (credit card icon) to toggle between Paid/Pending

### Searching Students

1. Navigate to **Search** page
2. Select search type (Name, Bed Number, Student ID, or All Fields)
3. Enter search query and click Search

### Dashboard Analytics

The dashboard displays:
- **Total Beds**: Total capacity
- **Available Beds**: Currently available
- **Occupied Beds**: Currently occupied
- **Occupancy Rate**: Percentage of beds occupied
- **Payment Statistics**: Count of Paid vs Pending payments
- **Recent Allotments**: Latest 10 bed allocations

## 🔒 Security Features

- Password hashing using Werkzeug (no plaintext passwords)
- SQL injection protection (parameterized queries)
- Session management with Flask-Login
- Role-based access control
- Secure authentication system

## 📁 Project Structure

```
hostel-accommodation-system/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── setup_database.py      # Database initialization script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── database_setup.sql      # SQL schema (alternative setup)
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Dashboard
│   ├── beds.html          # Bed management
│   ├── add_bed.html       # Add bed form
│   └── search.html        # Search page
└── static/               # Static files
    ├── css/
    │   └── style.css      # Custom styles
    └── js/                # JavaScript files (if any)
```

## 🐛 Troubleshooting

### Database Connection Error
- Verify MySQL server is running
- Check credentials in `.env` or `config.py`
- Ensure database exists (run `setup_database.py`)

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.7+

### Email Not Working
- Email functionality is optional
- Configure MAIL settings in `.env` for notifications
- App will work without email configuration

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`
- Or stop other applications using port 5000

## 🔄 Migration from C++ Console App

The web application is designed to work with your existing MySQL database. The `setup_database.py` script will:
- Preserve existing data in the `hostel` table
- Add new columns for enhanced features (StudentID, Contact, Email, etc.)
- Create new `users` table for authentication

## 🚀 Deployment

### Local Network Access
```bash
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Production Deployment
For production deployment:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure a reverse proxy (Nginx)
4. Use environment variables for sensitive data
5. Enable HTTPS/SSL
6. Use a stronger SECRET_KEY

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 License

This project is open source and available for educational and personal use.

## 👤 Author

Developed as an enhanced version of the original C++ console application.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

---

**Note**: This is a complete transformation of the original C++ console application into a modern web application suitable for resumes, portfolios, and real-world deployment.
