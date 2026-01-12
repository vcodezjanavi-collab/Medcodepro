from flask import Blueprint, render_template, redirect, url_for, send_file
from models.enquiry import Enquiry
from models.user import db
from utils.helpers import login_required
import csv
import io

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard - view all enquiries"""
    enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).all()
    
    # Calculate statistics
    total_enquiries = len(enquiries)
    courses_count = {}
    for enq in enquiries:
        courses_count[enq.course] = courses_count.get(enq.course, 0) + 1
    
    return render_template('admin_dashboard.html', 
                         enquiries=enquiries,
                         total_enquiries=total_enquiries,
                         courses_count=courses_count)

@admin_bp.route('/export-enquiries')
@login_required
def export_enquiries():
    """Export enquiries to CSV"""
    enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Name', 'Phone', 'Email', 'Course', 'Date'])
    
    # Write data
    for enq in enquiries:
        writer.writerow([
            enq.id,
            enq.name,
            enq.phone,
            enq.email,
            enq.course,
            enq.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    # Prepare file for download
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='medcodepro_enquiries.csv'
    )
