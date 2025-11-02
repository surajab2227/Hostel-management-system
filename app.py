from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from config import Config
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.config.from_object(Config)
# --- Clever Cloud MySQL configuration (Render environment variables) ---
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_ADDON_HOST', app.config.get('MYSQL_HOST'))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_ADDON_USER', app.config.get('MYSQL_USER'))
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_ADDON_PASSWORD', app.config.get('MYSQL_PASSWORD'))
app.config['MYSQL_DATABASE'] = os.environ.get('MYSQL_ADDON_DB', app.config.get('MYSQL_DATABASE'))
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_ADDON_PORT', app.config.get('MYSQL_PORT', 3306)))
# ------------------------------------------------------------------------


# Initialize Flask extensions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

mail = Mail()
mail.init_app(app)

# Database connection helper
def get_db_connection():
    """Create and return MySQL database connection (Render + Clever Cloud compatible)"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', app.config.get('MYSQL_HOST')),
            user=os.getenv('MYSQL_USER', app.config.get('MYSQL_USER')),
            password=os.getenv('MYSQL_PASSWORD', app.config.get('MYSQL_PASSWORD')),
            database=os.getenv('MYSQL_DATABASE', app.config.get('MYSQL_DATABASE')),
            port=int(os.getenv('MYSQL_PORT', app.config.get('MYSQL_PORT', 3306)))
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# User model (simplified for Flask-Login)
class User:
    def __init__(self, id, username, email, role='user'):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def is_admin(self):
        return self.role == 'admin'

@login_manager.user_loader
def load_user(user_id):
    """Load user from database"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user_data:
            return User(user_data['id'], user_data['username'], 
                       user_data['email'], user_data['role'])
    except Error as e:
        print(f"Error loading user: {e}")
    
    return None

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    """Home page - redirect to login or dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection error. Please try again later.', 'danger')
            return render_template('login.html')
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data and check_password_hash(user_data['password'], password):
                user = User(user_data['id'], user_data['username'], 
                           user_data['email'], user_data['role'])
                login_user(user)
                flash(f'Welcome back, {user.username}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
        except Error as e:
            flash('Error during login. Please try again.', 'danger')
            print(f"Login error: {e}")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection error.', 'danger')
            return render_template('register.html')
        
        try:
            cursor = conn.cursor()
            # Check if username or email exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", 
                         (username, email))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                flash('Username or email already exists.', 'danger')
                return render_template('register.html')
            
            # Create new user (default role is 'user', first user becomes admin)
            cursor.execute("SELECT COUNT(*) as count FROM users")
            count = cursor.fetchone()[0]
            role = 'admin' if count == 0 else 'user'
            
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, email, password, role, created_at) VALUES (%s, %s, %s, %s, %s)",
                (username, email, hashed_password, role, datetime.now())
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Error as e:
            flash('Registration failed. Please try again.', 'danger')
            print(f"Registration error: {e}")
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - different views for admin and students"""
    if current_user.is_admin():
        return admin_dashboard()
    else:
        return student_dashboard()

def admin_dashboard():
    """Admin dashboard with statistics"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return render_template('dashboard.html', stats={}, is_admin=True)
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get total beds
        total_beds = app.config['TOTAL_BEDS']
        
        # Get reserved beds count
        cursor.execute("SELECT COUNT(*) as count FROM hostel")
        reserved_beds = cursor.fetchone()['count']
        available_beds = total_beds - reserved_beds
        
        # Get recent allotments
        cursor.execute("""
            SELECT BedNo, Name, StudentID, Contact, Email, 
                   CheckInDate, PaymentStatus 
            FROM hostel 
            ORDER BY CheckInDate DESC 
            LIMIT 10
        """)
        recent_allotments = cursor.fetchall()
        
        # Get pending applications count
        cursor.execute("SELECT COUNT(*) as count FROM bed_applications WHERE status = 'Pending'")
        pending_applications = cursor.fetchone()['count']
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) as count FROM hostel WHERE PaymentStatus = 'Paid'")
        paid_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM hostel WHERE PaymentStatus = 'Pending'")
        pending_count = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        stats = {
            'total_beds': total_beds,
            'reserved_beds': reserved_beds,
            'available_beds': available_beds,
            'occupancy_rate': round((reserved_beds / total_beds * 100) if total_beds > 0 else 0, 1),
            'paid_count': paid_count,
            'pending_count': pending_count,
            'pending_applications': pending_applications
        }
        
        return render_template('dashboard.html', stats=stats, 
                             recent_allotments=recent_allotments, is_admin=True)
    except Error as e:
        flash('Error loading dashboard data.', 'danger')
        print(f"Dashboard error: {e}")
        return render_template('dashboard.html', stats={}, recent_allotments=[], is_admin=True)

def student_dashboard():
    """Student dashboard showing their bed status and applications"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return render_template('student_dashboard.html', bed_info=None, applications=[])
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get student's bed allocation if any
        cursor.execute("""
            SELECT BedNo, Name, StudentID, Contact, Email, 
                   CheckInDate, PaymentStatus 
            FROM hostel 
            WHERE user_id = %s
        """, (current_user.id,))
        bed_info = cursor.fetchone()
        
        # Get student's applications
        cursor.execute("""
            SELECT id, student_name, student_id, status, applied_date, reviewed_date, bed_no, notes
            FROM bed_applications 
            WHERE user_id = %s 
            ORDER BY applied_date DESC
        """, (current_user.id,))
        applications = cursor.fetchall()
        
        # Get user info
        cursor.execute("SELECT username, email FROM users WHERE id = %s", (current_user.id,))
        user_info = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('student_dashboard.html', 
                             bed_info=bed_info, 
                             applications=applications,
                             user_info=user_info)
    except Error as e:
        flash('Error loading dashboard data.', 'danger')
        print(f"Dashboard error: {e}")
        return render_template('student_dashboard.html', bed_info=None, applications=[])

@app.route('/beds')
@login_required
def beds():
    """View all bed allotments"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return render_template('beds.html', allotments=[])
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT BedNo, Name, StudentID, Contact, Email, 
                   CheckInDate, PaymentStatus 
            FROM hostel 
            ORDER BY BedNo ASC
        """)
        allotments = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('beds.html', allotments=allotments, 
                             total_beds=app.config['TOTAL_BEDS'])
    except Error as e:
        flash('Error loading bed data.', 'danger')
        print(f"Beds error: {e}")
        return render_template('beds.html', allotments=[])

@app.route('/beds/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_bed():
    """Add new bed allotment"""
    if request.method == 'POST':
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        contact = request.form.get('contact')
        email = request.form.get('email')
        
        if not name:
            flash('Student name is required.', 'danger')
            return render_template('add_bed.html')
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection error.', 'danger')
            return render_template('add_bed.html')
        
        try:
            cursor = conn.cursor()
            
            # Check if all beds are occupied
            cursor.execute("SELECT COUNT(*) as count FROM hostel")
            reserved = cursor.fetchone()[0]
            
            if reserved >= app.config['TOTAL_BEDS']:
                cursor.close()
                conn.close()
                flash('Sorry! No beds available.', 'warning')
                return render_template('add_bed.html')
            
            # Find next available bed
            cursor.execute("SELECT BedNo FROM hostel ORDER BY BedNo")
            occupied = [row[0] for row in cursor.fetchall()]
            bed_no = None
            for i in range(1, app.config['TOTAL_BEDS'] + 1):
                if i not in occupied:
                    bed_no = i
                    break
            
            # Insert new allotment
            cursor.execute("""
                INSERT INTO hostel (BedNo, Name, StudentID, Contact, Email, 
                                   CheckInDate, PaymentStatus) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (bed_no, name, student_id or None, contact or None, 
                  email or None, datetime.now(), 'Pending'))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Send email notification if configured
            if email and app.config['MAIL_USERNAME']:
                try:
                    send_notification_email(email, name, bed_no, 'allocation')
                except Exception as e:
                    print(f"Email error: {e}")
            
            flash(f'Bed {bed_no} allocated to {name} successfully!', 'success')
            return redirect(url_for('beds'))
        except Error as e:
            flash('Error adding bed allotment.', 'danger')
            print(f"Add bed error: {e}")
    
    return render_template('add_bed.html')

@app.route('/beds/remove/<int:bed_no>', methods=['POST'])
@login_required
@admin_required
def remove_bed(bed_no):
    """Remove bed allotment"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return redirect(url_for('beds'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Get student info before deletion for email
        cursor.execute("SELECT Name, Email FROM hostel WHERE BedNo = %s", (bed_no,))
        student = cursor.fetchone()
        
        cursor.execute("DELETE FROM hostel WHERE BedNo = %s", (bed_no,))
        
        if cursor.rowcount > 0:
            conn.commit()
            
            # Send email notification if configured
            if student and student['Email'] and app.config['MAIL_USERNAME']:
                try:
                    send_notification_email(student['Email'], student['Name'], 
                                          bed_no, 'removal')
                except Exception as e:
                    print(f"Email error: {e}")
            
            flash(f'Bed {bed_no} allotment removed successfully!', 'success')
        else:
            flash('No allotment found for this bed.', 'warning')
        
        cursor.close()
        conn.close()
    except Error as e:
        flash('Error removing bed allotment.', 'danger')
        print(f"Remove bed error: {e}")
    
    return redirect(url_for('beds'))

@app.route('/search')
@login_required
def search():
    """Search for students"""
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'name')
    
    if not query:
        return render_template('search.html', results=[], query='', search_type=search_type)
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return render_template('search.html', results=[], query=query, search_type=search_type)
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        if search_type == 'name':
            cursor.execute("""
                SELECT BedNo, Name, StudentID, Contact, Email, 
                       CheckInDate, PaymentStatus 
                FROM hostel 
                WHERE Name LIKE %s 
                ORDER BY Name
            """, (f'%{query}%',))
        elif search_type == 'bed':
            cursor.execute("""
                SELECT BedNo, Name, StudentID, Contact, Email, 
                       CheckInDate, PaymentStatus 
                FROM hostel 
                WHERE BedNo = %s
            """, (query,))
        elif search_type == 'student_id':
            cursor.execute("""
                SELECT BedNo, Name, StudentID, Contact, Email, 
                       CheckInDate, PaymentStatus 
                FROM hostel 
                WHERE StudentID LIKE %s 
                ORDER BY Name
            """, (f'%{query}%',))
        else:
            cursor.execute("""
                SELECT BedNo, Name, StudentID, Contact, Email, 
                       CheckInDate, PaymentStatus 
                FROM hostel 
                WHERE Name LIKE %s OR StudentID LIKE %s OR BedNo = %s
                ORDER BY BedNo
            """, (f'%{query}%', f'%{query}%', query))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('search.html', results=results, query=query, search_type=search_type)
    except Error as e:
        flash('Error performing search.', 'danger')
        print(f"Search error: {e}")
        return render_template('search.html', results=[], query=query, search_type=search_type)

@app.route('/beds/update_payment/<int:bed_no>', methods=['POST'])
@login_required
@admin_required
def update_payment(bed_no):
    """Update payment status"""
    status = request.form.get('status')
    
    if status not in ['Paid', 'Pending']:
        flash('Invalid payment status.', 'danger')
        return redirect(url_for('beds'))
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return redirect(url_for('beds'))
    
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE hostel SET PaymentStatus = %s WHERE BedNo = %s", 
                      (status, bed_no))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Payment status updated successfully!', 'success')
    except Error as e:
        flash('Error updating payment status.', 'danger')
        print(f"Update payment error: {e}")
    
    return redirect(url_for('beds'))

# Student Routes
@app.route('/apply', methods=['GET', 'POST'])
@login_required
def apply_for_bed():
    """Students can apply for a bed"""
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_id = request.form.get('student_id')
        contact = request.form.get('contact')
        email = request.form.get('email')
        
        if not student_name:
            flash('Student name is required.', 'danger')
            return render_template('apply_bed.html')
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection error.', 'danger')
            return render_template('apply_bed.html')
        
        try:
            cursor = conn.cursor()
            
            # Check if user already has a bed
            cursor.execute("SELECT BedNo FROM hostel WHERE user_id = %s", (current_user.id,))
            existing_bed = cursor.fetchone()
            if existing_bed:
                cursor.close()
                conn.close()
                flash('You already have a bed allocated!', 'info')
                return redirect(url_for('dashboard'))
            
            # Check if user has pending application
            cursor.execute("SELECT id FROM bed_applications WHERE user_id = %s AND status = 'Pending'", 
                          (current_user.id,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                flash('You already have a pending application!', 'warning')
                return redirect(url_for('dashboard'))
            
            # Create application
            cursor.execute("""
                INSERT INTO bed_applications 
                (user_id, student_name, student_id, contact, email, status) 
                VALUES (%s, %s, %s, %s, %s, 'Pending')
            """, (current_user.id, student_name, student_id or None, 
                  contact or None, email or current_user.email))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Application submitted successfully! Admin will review it soon.', 'success')
            return redirect(url_for('dashboard'))
        except Error as e:
            flash('Error submitting application.', 'danger')
            print(f"Apply bed error: {e}")
    
    return render_template('apply_bed.html')

@app.route('/my-applications')
@login_required
def my_applications():
    """View student's own applications"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return render_template('my_applications.html', applications=[])
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, student_name, student_id, status, applied_date, reviewed_date, bed_no, notes
            FROM bed_applications 
            WHERE user_id = %s 
            ORDER BY applied_date DESC
        """, (current_user.id,))
        applications = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('my_applications.html', applications=applications)
    except Error as e:
        flash('Error loading applications.', 'danger')
        print(f"Applications error: {e}")
        return render_template('my_applications.html', applications=[])

@app.route('/my-profile')
@login_required
def my_profile():
    """View and edit student profile"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get user info
        cursor.execute("SELECT * FROM users WHERE id = %s", (current_user.id,))
        user_info = cursor.fetchone()
        
        # Get bed allocation
        cursor.execute("""
            SELECT BedNo, Name, StudentID, Contact, Email, 
                   CheckInDate, PaymentStatus 
            FROM hostel 
            WHERE user_id = %s
        """, (current_user.id,))
        bed_info = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('my_profile.html', user_info=user_info, bed_info=bed_info)
    except Error as e:
        flash('Error loading profile.', 'danger')
        print(f"Profile error: {e}")
        return redirect(url_for('dashboard'))

# Admin Routes for Applications
@app.route('/admin/applications')
@login_required
@admin_required
def view_applications():
    """Admin view all bed applications"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return render_template('admin_applications.html', applications=[])
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ba.id, ba.user_id, u.username, u.email, ba.student_name, ba.student_id, 
                   ba.contact, ba.email as app_email, ba.status, ba.applied_date, 
                   ba.reviewed_date, ba.bed_no, ba.notes
            FROM bed_applications ba
            JOIN users u ON ba.user_id = u.id
            ORDER BY ba.applied_date DESC
        """)
        applications = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('admin_applications.html', applications=applications)
    except Error as e:
        flash('Error loading applications.', 'danger')
        print(f"Applications error: {e}")
        return render_template('admin_applications.html', applications=[])

@app.route('/admin/applications/<int:app_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_application(app_id):
    """Admin approve a bed application"""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return redirect(url_for('view_applications'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get application details
        cursor.execute("SELECT * FROM bed_applications WHERE id = %s", (app_id,))
        application = cursor.fetchone()
        
        if not application:
            flash('Application not found.', 'danger')
            return redirect(url_for('view_applications'))
        
        if application['status'] != 'Pending':
            flash('Application already processed.', 'warning')
            return redirect(url_for('view_applications'))
        
        # Check if all beds are occupied
        cursor.execute("SELECT COUNT(*) as count FROM hostel")
        reserved = cursor.fetchone()['count']
        
        if reserved >= app.config['TOTAL_BEDS']:
            cursor.close()
            conn.close()
            flash('Sorry! No beds available.', 'warning')
            return redirect(url_for('view_applications'))
        
        # Find next available bed
        cursor.execute("SELECT BedNo FROM hostel ORDER BY BedNo")
        occupied = [row['BedNo'] for row in cursor.fetchall()]
        bed_no = None
        for i in range(1, app.config['TOTAL_BEDS'] + 1):
            if i not in occupied:
                bed_no = i
                break
        
        # Create bed allotment
        cursor.execute("""
            INSERT INTO hostel (BedNo, Name, StudentID, Contact, Email, 
                               CheckInDate, PaymentStatus, user_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (bed_no, application['student_name'], application['student_id'], 
              application['contact'], application['email'], datetime.now(), 
              'Pending', application['user_id']))
        
        # Update application status
        cursor.execute("""
            UPDATE bed_applications 
            SET status = 'Approved', reviewed_date = %s, bed_no = %s 
            WHERE id = %s
        """, (datetime.now(), bed_no, app_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Send email notification
        email = application['email'] or application.get('user_email')
        if email and app.config['MAIL_USERNAME']:
            try:
                send_notification_email(email, application['student_name'], bed_no, 'allocation')
            except Exception as e:
                print(f"Email error: {e}")
        
        flash(f'Application approved! Bed {bed_no} allocated.', 'success')
        return redirect(url_for('view_applications'))
    except Error as e:
        flash('Error approving application.', 'danger')
        print(f"Approve error: {e}")
        return redirect(url_for('view_applications'))

@app.route('/admin/applications/<int:app_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_application(app_id):
    """Admin reject a bed application"""
    notes = request.form.get('notes', '')
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection error.', 'danger')
        return redirect(url_for('view_applications'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get application
        cursor.execute("SELECT * FROM bed_applications WHERE id = %s", (app_id,))
        application = cursor.fetchone()
        
        if not application or application['status'] != 'Pending':
            flash('Application not found or already processed.', 'warning')
            return redirect(url_for('view_applications'))
        
        # Update application status
        cursor.execute("""
            UPDATE bed_applications 
            SET status = 'Rejected', reviewed_date = %s, notes = %s 
            WHERE id = %s
        """, (datetime.now(), notes, app_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Application rejected.', 'info')
        return redirect(url_for('view_applications'))
    except Error as e:
        flash('Error rejecting application.', 'danger')
        print(f"Reject error: {e}")
        return redirect(url_for('view_applications'))

def send_notification_email(email, name, bed_no, action):
    """Send email notification"""
    if not app.config['MAIL_USERNAME']:
        return
    
    try:
        if action == 'allocation':
            subject = f'Hostel Bed Allocated - Bed {bed_no}'
            body = f'''
Hello {name},

Your hostel bed has been successfully allocated!

Bed Number: {bed_no}
Check-in Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Payment Status: Pending

Please complete the payment of {app.config['HOSTEL_FEE']} Rupees to confirm your reservation.

Thank you,
Hostel Management System
            '''
        else:  # removal
            subject = f'Hostel Bed Allotment Removed - Bed {bed_no}'
            body = f'''
Hello {name},

Your hostel bed allotment (Bed {bed_no}) has been removed from the system.

If you have any questions, please contact the hostel administration.

Thank you,
Hostel Management System
            '''
        
        msg = Message(subject, recipients=[email], body=body)
        mail.send(msg)
    except Exception as e:
        print(f"Email sending failed: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


