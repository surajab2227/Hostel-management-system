# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Database
Update `config.py` with your MySQL credentials, or create a `.env` file:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=mydb
```

### Step 3: Setup Database
```bash
python setup_database.py
```
Or on Windows:
```bash
run_setup.bat
```

This creates:
- Database tables
- Default admin user (username: `admin`, password: `admin123`)

### Step 4: Run Application
```bash
python app.py
```
Or on Windows:
```bash
run_app.bat
```

### Step 5: Access Application
Open browser: `http://localhost:5000`

Login with:
- Username: `admin`
- Password: `admin123`

**⚠️ Change the default password immediately!**

---

## 📋 What's New?

### ✨ Features Added:
1. ✅ **Web Interface** - Modern, responsive UI
2. ✅ **User Authentication** - Secure login system
3. ✅ **Admin Panel** - Role-based access control
4. ✅ **Dashboard** - Analytics and statistics
5. ✅ **Search** - Find students by name, bed, or ID
6. ✅ **Enhanced Data** - Student ID, contact, email tracking
7. ✅ **Payment Tracking** - Paid/Pending status
8. ✅ **Email Notifications** - Optional email alerts
9. ✅ **Better UX** - Professional Bootstrap design

### 🔒 Security Improvements:
- Password hashing
- SQL injection protection
- Session management
- Role-based permissions

---

## 📁 Key Files

- `app.py` - Main Flask application
- `config.py` - Configuration settings
- `setup_database.py` - Database initialization
- `templates/` - HTML pages
- `static/` - CSS and JavaScript

---

## 🎯 Next Steps

1. **Change Admin Password** - Update default credentials
2. **Configure Email** (Optional) - Add SMTP settings in `.env`
3. **Customize** - Adjust `TOTAL_BEDS` in config
4. **Register Users** - Create accounts for your team

---

## 🆘 Need Help?

Check `README.md` for detailed documentation.

