import os

class Config:
    """Application configuration class"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'medcodepro-secret-key-change-in-production'
    
    # Database configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Render uses 'postgres://' but SQLAlchemy needs 'postgresql://'
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or \
        'sqlite:///' + os.path.join(BASE_DIR, 'database', 'medcodepro.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Ensure database directory exists for SQLite
    if not DATABASE_URL:
        os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)
    
    # Admin credentials (for initial setup)
    ADMIN_EMAIL = 'admin@medcodepro.com'
    ADMIN_PASSWORD = 'admin123'  # Change this in production
    
    # Social media links - EDIT THESE WITH YOUR ACTUAL LINKS
    FACEBOOK_URL = 'https://www.facebook.com/yourpage'
    LINKEDIN_URL = 'https://www.linkedin.com/company/yourcompany'
    TWITTER_URL = 'https://twitter.com/yourhandle'
    INSTAGRAM_URL = 'https://www.instagram.com/yourhandle'
    
    # Google Maps embed - EDIT THIS WITH YOUR ACTUAL LOCATION
    # Get embed code from: https://www.google.com/maps
    # Replace YOUR_EMBED_URL with your actual Google Maps embed URL
    GOOGLE_MAPS_EMBED = 'https://www.google.com/maps/embed?pb=YOUR_EMBED_URL'
    
    # Contact information - EDIT THESE
    CONTACT_PHONE = '+1 (555) 123-4567'
    CONTACT_EMAIL = 'info@medcodepro.com'
    CONTACT_ADDRESS = '123 Medical Plaza, Healthcare District, City, State 12345'
