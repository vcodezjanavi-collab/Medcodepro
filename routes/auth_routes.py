from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import Admin, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find admin by email
        admin = Admin.query.filter_by(email=email).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_email'] = admin.email
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Logout admin"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('pages.home'))
