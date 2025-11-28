import os
import re
import mimetypes
from werkzeug.utils import secure_filename as werkzeug_secure_filename

def secure_filename_custom(filename):
    """Enhanced filename sanitization"""
    # Use werkzeug's secure_filename as base
    filename = werkzeug_secure_filename(filename)
    
    # Additional sanitization
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    
    return filename

def get_mime_type(filename):
    """Detect file MIME type"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or 'application/octet-stream'

def format_file_size(bytes_size):
    """Format bytes to human-readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

def validate_path(base_path, user_path):
    """
    Prevent directory traversal attacks
    Ensures the user_path is within base_path
    """
    base = os.path.abspath(base_path)
    target = os.path.abspath(os.path.join(base_path, user_path))
    
    # Check if target path starts with base path
    if not target.startswith(base):
        raise ValueError("Invalid path detected")
    
    return target

def create_user_directory(base_upload_folder, user_id):
    """Create user-specific storage folder"""
    user_folder = os.path.join(base_upload_folder, f'user_{user_id}')
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_unique_filename(directory, filename):
    """Generate unique filename if file already exists"""
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1
    
    return new_filename

def get_file_icon_class(mime_type):
    """Return CSS class for file icon based on MIME type"""
    if not mime_type:
        return 'file'
    
    if mime_type.startswith('image/'):
        return 'file-image'
    elif mime_type.startswith('video/'):
        return 'file-video'
    elif mime_type.startswith('audio/'):
        return 'file-audio'
    elif 'pdf' in mime_type:
        return 'file-pdf'
    elif 'word' in mime_type or 'document' in mime_type:
        return 'file-word'
    elif 'excel' in mime_type or 'spreadsheet' in mime_type:
        return 'file-excel'
    elif 'powerpoint' in mime_type or 'presentation' in mime_type:
        return 'file-powerpoint'
    elif 'zip' in mime_type or 'rar' in mime_type or 'compressed' in mime_type:
        return 'file-archive'
    elif 'text' in mime_type or 'json' in mime_type or 'xml' in mime_type:
        return 'file-text'
    else:
        return 'file'
