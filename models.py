from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    files = db.relationship('File', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    folders = db.relationship('Folder', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Folder(db.Model):
    """Folder model for organizing files"""
    __tablename__ = 'folders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    folder_name = db.Column(db.String(255), nullable=False)
    parent_folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)
    folder_path = db.Column(db.String(1000), nullable=False)  # Full path from root
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for nested folders
    subfolders = db.relationship('Folder', backref=db.backref('parent', remote_side=[id]), 
                                 lazy='dynamic', cascade='all, delete-orphan')
    files = db.relationship('File', backref='folder', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert folder to dictionary"""
        return {
            'id': self.id,
            'name': self.folder_name,
            'parent_folder_id': self.parent_folder_id,
            'path': self.folder_path,
            'created_at': self.created_at.isoformat(),
            'type': 'folder'
        }


class File(db.Model):
    """File model for storing file metadata"""
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=True)
    filename = db.Column(db.String(255), nullable=False)  # Stored filename (may be modified for uniqueness)
    original_filename = db.Column(db.String(255), nullable=False)  # Original upload filename
    file_path = db.Column(db.String(1000), nullable=False)  # Physical file path on disk
    file_size = db.Column(db.BigInteger, nullable=False)  # Size in bytes
    mime_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert file to dictionary"""
        return {
            'id': self.id,
            'name': self.original_filename,
            'filename': self.filename,
            'folder_id': self.folder_id,
            'size': self.file_size,
            'mime_type': self.mime_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'type': 'file'
        }
