"""
Database Setup Script
Run this script to initialize the database with required tables.
"""

import mysql.connector
from mysql.connector import Error
from config import Config
from werkzeug.security import generate_password_hash

def setup_database():
    """Initialize database tables"""
    try:
        # Connect to MySQL server (without database)
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE}")
        cursor.execute(f"USE {Config.MYSQL_DATABASE}")
        print(f"[OK] Database '{Config.MYSQL_DATABASE}' ready")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'user') DEFAULT 'user',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_username (username),
                INDEX idx_email (email)
            )
        """)
        print("[OK] Users table created")
        
        # Create/Update hostel table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hostel (
                BedNo INT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                StudentID VARCHAR(50),
                Contact VARCHAR(20),
                Email VARCHAR(100),
                CheckInDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                PaymentStatus ENUM('Paid', 'Pending') DEFAULT 'Pending',
                INDEX idx_name (Name),
                INDEX idx_student_id (StudentID),
                INDEX idx_payment (PaymentStatus),
                INDEX idx_checkin (CheckInDate)
            )
        """)
        print("[OK] Hostel table created")
        
        # Create bed_applications table for student applications
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bed_applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                student_name VARCHAR(100) NOT NULL,
                student_id VARCHAR(50),
                contact VARCHAR(20),
                email VARCHAR(100),
                status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
                applied_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                reviewed_date DATETIME NULL,
                bed_no INT NULL,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_status (status),
                INDEX idx_applied_date (applied_date)
            )
        """)
        print("[OK] Bed applications table created")
        
        # Add user_id to hostel table to link beds to users
        try:
            cursor.execute("SHOW COLUMNS FROM hostel LIKE 'user_id'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE hostel ADD COLUMN user_id INT NULL AFTER PaymentStatus")
                print("[OK] Added user_id column to hostel table")
                # Add foreign key constraint separately
                try:
                    cursor.execute("ALTER TABLE hostel ADD CONSTRAINT fk_hostel_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL")
                    print("[OK] Added foreign key constraint")
                except Error as e:
                    # Foreign key might already exist or table might have data
                    print(f"Note: Foreign key constraint - {e}")
        except Error as e:
            print(f"Note: {e}")
        
        # Migrate existing hostel table if it has old schema
        try:
            # Check if old columns exist
            cursor.execute("SHOW COLUMNS FROM hostel LIKE 'StudentID'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE hostel ADD COLUMN StudentID VARCHAR(50) AFTER Name")
                print("[OK] Added StudentID column to hostel table")
            
            cursor.execute("SHOW COLUMNS FROM hostel LIKE 'Contact'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE hostel ADD COLUMN Contact VARCHAR(20) AFTER StudentID")
                print("[OK] Added Contact column to hostel table")
            
            cursor.execute("SHOW COLUMNS FROM hostel LIKE 'Email'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE hostel ADD COLUMN Email VARCHAR(100) AFTER Contact")
                print("[OK] Added Email column to hostel table")
            
            cursor.execute("SHOW COLUMNS FROM hostel LIKE 'CheckInDate'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE hostel ADD COLUMN CheckInDate DATETIME DEFAULT CURRENT_TIMESTAMP AFTER Email")
                print("[OK] Added CheckInDate column to hostel table")
            
            cursor.execute("SHOW COLUMNS FROM hostel LIKE 'PaymentStatus'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE hostel ADD COLUMN PaymentStatus ENUM('Paid', 'Pending') DEFAULT 'Pending' AFTER CheckInDate")
                print("[OK] Added PaymentStatus column to hostel table")
        except Error as e:
            print(f"Migration note: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n[OK] Database setup completed successfully!")
        return True
        
    except Error as e:
        print(f"\n[ERROR] Database setup failed: {e}")
        return False

def create_admin_user():
    """Create default admin user"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        # Check if any users exist
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Create default admin
            default_username = "admin"
            default_password = "admin123"  # Change this after first login!
            default_email = "admin@hostel.com"
            
            hashed_password = generate_password_hash(default_password)
            cursor.execute("""
                INSERT INTO users (username, email, password, role) 
                VALUES (%s, %s, %s, 'admin')
            """, (default_username, default_email, hashed_password))
            
            conn.commit()
            print(f"\n[OK] Default admin user created!")
            print(f"  Username: {default_username}")
            print(f"  Password: {default_password}")
            print(f"  [WARNING] Please change the password after first login!")
        else:
            print("\n[OK] Users already exist. Skipping default admin creation.")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print(f"\n[ERROR] Failed to create admin user: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Hostel Management System - Database Setup")
    print("=" * 50)
    
    if setup_database():
        create_admin_user()
        print("\n" + "=" * 50)
        print("Setup completed! You can now run the application.")
        print("=" * 50)
    else:
        print("\nSetup failed. Please check your MySQL connection settings.")

