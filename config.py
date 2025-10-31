import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for Flask application"""
    
    # Database Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Surajab@218318')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'mydb')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
    
    # Email Configuration (for notifications)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@hostel.com')
    
    # Hostel Configuration
    TOTAL_BEDS = int(os.getenv('TOTAL_BEDS', 20))
    
    # Hostel Fee
    HOSTEL_FEE = int(os.getenv('HOSTEL_FEE', 5000))

