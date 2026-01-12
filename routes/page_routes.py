from flask import Blueprint, render_template, request, jsonify, current_app
from models.enquiry import Enquiry
from models.user import db
from utils.helpers import validate_email, validate_phone

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@pages_bp.route('/about')
def about():
    """About us page"""
    return render_template('about.html')

@pages_bp.route('/courses')
def courses():
    """Courses page"""
    return render_template('courses.html')

@pages_bp.route('/services')
def services():
    """Services page"""
    return render_template('services.html')

@pages_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with enquiry form"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        
        # Validate inputs
        errors = []
        if not name:
            errors.append('Name is required')
        if not phone or not validate_phone(phone):
            errors.append('Valid phone number is required')
        if not email or not validate_email(email):
            errors.append('Valid email is required')
        if not course:
            errors.append('Please select a course')
        
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
        
        # Create new enquiry
        try:
            enquiry = Enquiry(
                name=name,
                phone=phone,
                email=email,
                course=course
            )
            db.session.add(enquiry)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Thank you for your enquiry! We will contact you soon.'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'errors': ['Failed to submit enquiry. Please try again.']
            }), 500
    
    return render_template('contact.html')
