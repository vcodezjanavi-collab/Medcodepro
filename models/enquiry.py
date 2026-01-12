from models.user import db
from datetime import datetime

class Enquiry(db.Model):
    """Enquiry form submissions model"""
    __tablename__ = 'enquiry'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Enquiry {self.name} - {self.course}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'course': self.course,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
