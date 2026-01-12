from flask import Flask, render_template
from config import Config
from models.user import db, Admin
from models.enquiry import Enquiry
from routes.auth_routes import auth_bp
from routes.page_routes import pages_bp
from routes.admin_routes import admin_bp

def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(admin_bp)
    
    # Create database tables and initial admin
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        if not Admin.query.filter_by(email=Config.ADMIN_EMAIL).first():
            admin = Admin(email=Config.ADMIN_EMAIL)
            admin.set_password(Config.ADMIN_PASSWORD)
            db.session.add(admin)
            db.session.commit()
            print(f'Default admin created: {Config.ADMIN_EMAIL}')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Make config available in templates
    @app.context_processor
    def inject_config():
        return dict(config=app.config)
    
    return app

# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    print('=' * 60)
    print('MedCodePro Application Starting...')
    print('=' * 60)
    print(f'Admin Login: {Config.ADMIN_EMAIL}')
    print(f'Admin Password: {Config.ADMIN_PASSWORD}')
    print('IMPORTANT: Change admin password in production!')
    print('=' * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
