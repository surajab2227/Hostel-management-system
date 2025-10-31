# 🚀 PythonAnywhere Deployment Guide

## ✅ Why PythonAnywhere?
- **100% FREE tier** with always-on hosting
- **MySQL database included** (no external service needed!)
- **Perfect for Flask apps**
- **No sleep/spin-down** (unlike Render/Replit)
- **Perfect for portfolio/interview projects**

---

## Step 1: Create PythonAnywhere Account

1. Go to: **https://www.pythonanywhere.com**
2. Click **"Sign up"** → **"Beginner account"** (FREE)
3. Verify your email
4. You'll get a free account: `yourusername.pythonanywhere.com`

---

## Step 2: Upload Your Code

### Option A: Clone from GitHub (Easiest)
1. In PythonAnywhere dashboard, open **"Files"** tab
2. Open **"Bash console"** (command line)
3. Run:
```bash
cd ~
git clone https://github.com/surajab2227/Hostel-management-system.git
cd Hostel-management-system
```

### Option B: Upload Files Manually
1. Go to **"Files"** tab
2. Click **"Upload a file"**
3. Upload your project files one by one

---

## Step 3: Install Dependencies

1. Open **"Bash console"**
2. Navigate to your project:
```bash
cd ~/Hostel-management-system
```
3. Install dependencies:
```bash
pip3.10 install --user -r requirements.txt
```

**Note:** PythonAnywhere uses Python 3.10 by default. Adjust if needed.

---

## Step 4: Set Up MySQL Database

1. Go to **"Databases"** tab
2. Click **"Initialize MySQL"** (first time only)
3. You'll get:
   - **Database name:** `yourusername$mydb` (or create custom)
   - **Username:** `yourusername`
   - **Password:** (create one or use auto-generated)
   - **Host:** `yourusername.mysql.pythonanywhere-services.com`

4. **Note these credentials!** You'll need them.

---

## Step 5: Update Database Configuration

1. In **"Files"** tab, edit `config.py`
2. Update MySQL settings:
```python
MYSQL_HOST = 'yourusername.mysql.pythonanywhere-services.com'
MYSQL_USER = 'yourusername'
MYSQL_PASSWORD = 'your-password-here'
MYSQL_DATABASE = 'yourusername$mydb'
MYSQL_PORT = 3306
```

**Or better:** Use environment variables in Web app settings!

---

## Step 6: Initialize Database

1. Open **"Bash console"**
2. Navigate to your project:
```bash
cd ~/Hostel-management-system
```
3. Run database setup:
```bash
python3.10 setup_database.py
```
4. This creates all tables and admin user!

---

## Step 7: Configure Web App

1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Flask"**
4. Select **Python 3.10**
5. Set **Path:** `/home/yourusername/Hostel-management-system/app.py`
6. Click **"Next"** → **"Finish"**

---

## Step 8: Configure WSGI File

1. In **"Web"** tab, click on the WSGI file link
2. Replace the content with:
```python
import sys

# Add your project directory to the path
path = '/home/yourusername/Hostel-management-system'
if path not in sys.path:
    sys.path.insert(0, path)

# Import your Flask app
from app import app as application

if __name__ == "__main__":
    application.run()
```

**Important:** Replace `yourusername` with your actual username!

3. **Save the file**

---

## Step 9: Set Environment Variables

1. In **"Web"** tab, click **"Environment variables"** section
2. Add these variables:

```
MYSQL_HOST=yourusername.mysql.pythonanywhere-services.com
MYSQL_USER=yourusername
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=yourusername$mydb
MYSQL_PORT=3306
SECRET_KEY=your-random-secret-key-here-make-it-long
TOTAL_BEDS=20
HOSTEL_FEE=5000
```

**Important:** Replace all `yourusername` with your actual username!

3. Click **"Add"** for each variable

---

## Step 10: Reload Your Web App

1. In **"Web"** tab, click **"Reload"** button (green button)
2. Wait a few seconds
3. Your app should be live!

---

## Step 11: Access Your Live Website

Your app will be available at:
**`https://yourusername.pythonanywhere.com`**

---

## Troubleshooting

### Issue: "Cannot import app"
- Make sure WSGI file path is correct
- Check that `app.py` exists in your project directory
- Verify Python version matches (3.10)

### Issue: "Database connection error"
- Double-check MySQL credentials
- Make sure database is initialized
- Verify environment variables are set correctly

### Issue: "Module not found"
- Install missing packages: `pip3.10 install --user package-name`
- Check `requirements.txt` has all dependencies

### Issue: "500 Internal Server Error"
- Check **"Error log"** in Web tab
- Check **"Server log"** for detailed errors
- Verify all environment variables are set

---

## Free Tier Limitations:

- ✅ **Always-on** (no sleep!)
- ✅ **MySQL included**
- ⚠️ **1 web app** only
- ⚠️ **512MB disk space**
- ⚠️ **Limited CPU time** (enough for portfolio projects)
- ⚠️ **Custom domain** requires paid plan

**But it's FREE and ALWAYS ON!** Perfect for portfolio/interview!

---

## Quick Checklist:

- [ ] Account created on PythonAnywhere
- [ ] Code uploaded (GitHub clone or manual)
- [ ] Dependencies installed (`pip3.10 install -r requirements.txt`)
- [ ] MySQL database initialized
- [ ] Database credentials updated in config
- [ ] Database tables created (`python3.10 setup_database.py`)
- [ ] Web app created and configured
- [ ] WSGI file updated correctly
- [ ] Environment variables set
- [ ] Web app reloaded
- [ ] App is live! 🎉

---

## Tips:

1. **Always reload** after making changes
2. **Check error logs** if something doesn't work
3. **Test locally** first if possible
4. **Keep credentials secure** (use environment variables)

---

## That's it! 🎉

Your hostel management system is now live on PythonAnywhere!

**URL:** `https://yourusername.pythonanywhere.com`

**Admin Login:**
- Username: `admin`
- Password: `admin123` (change this!)

---

## Next Steps:

1. **Change admin password** (for security)
2. **Test all features** on live site
3. **Share your URL** in portfolio/resume!

**Perfect for interviews - it's always on and completely free!** ✅

