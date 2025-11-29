import os
from flask import Blueprint, request, jsonify, send_file, current_app, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, User, File, Folder
from utils import (secure_filename_custom, get_mime_type, validate_path,
                   create_user_directory, allowed_file, get_unique_filename)
from auth import login_required
from sqlalchemy import or_

file_manager_bp = Blueprint('file_manager', __name__, url_prefix='/api')

def get_user_base_path(user_id):
    """Get base path for user's files"""
    return os.path.join(current_app.config['UPLOAD_FOLDER'], f'user_{user_id}')

@file_manager_bp.route('/files/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """Upload a file to the system"""
    user_id = get_jwt_identity()
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Get folder_id from form data (optional)
    folder_id = request.form.get('folder_id', type=int)
    
    # Validate folder ownership if specified
    folder = None
    if folder_id:
        folder = Folder.query.filter_by(id=folder_id, user_id=user_id).first()
        if not folder:
            return jsonify({'error': 'Folder not found or access denied'}), 404
    
    # Check allowed extensions
    if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Secure the filename
    original_filename = file.filename
    filename = secure_filename_custom(original_filename)
    
    # Create user directory if it doesn't exist
    user_folder = create_user_directory(current_app.config['UPLOAD_FOLDER'], user_id)
    
    # If uploading to a specific folder, use that path
    if folder:
        upload_path = os.path.join(user_folder, folder.folder_path.lstrip('/'))
    else:
        upload_path = user_folder
    
    os.makedirs(upload_path, exist_ok=True)
    
    # Get unique filename to avoid conflicts
    filename = get_unique_filename(upload_path, filename)
    file_path = os.path.join(upload_path, filename)
    
    # Save the file
    file.save(file_path)
    
    # Get file info
    file_size = os.path.getsize(file_path)
    mime_type = get_mime_type(original_filename)
    
    # Store relative path from user folder
    relative_path = os.path.relpath(file_path, user_folder)
    
    # Create database entry
    new_file = File(
        user_id=user_id,
        folder_id=folder_id,
        filename=filename,
        original_filename=original_filename,
        file_path=relative_path,
        file_size=file_size,
        mime_type=mime_type
    )
    
    db.session.add(new_file)
    db.session.commit()
    
    return jsonify({
        'message': 'File uploaded successfully',
        'file': new_file.to_dict()
    }), 201

@file_manager_bp.route('/files/download/<int:file_id>', methods=['GET'])
@jwt_required()
def download_file(file_id):
    """Download a file by ID"""
    user_id = get_jwt_identity()
    
    # Get file and verify ownership
    file = File.query.filter_by(id=file_id, user_id=user_id).first()
    
    if not file:
        return jsonify({'error': 'File not found or access denied'}), 404
    
    # Construct full file path
    user_folder = get_user_base_path(user_id)
    file_path = os.path.join(user_folder, file.file_path)
    
    # Validate path to prevent directory traversal
    try:
        file_path = validate_path(user_folder, file.file_path)
    except ValueError:
        return jsonify({'error': 'Invalid file path'}), 400
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found on disk'}), 404
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=file.original_filename,
        mimetype=file.mime_type
    )

@file_manager_bp.route('/files/list', methods=['GET'])
@login_required
def list_files():
    """List all files and folders for the current user"""
    user_id = session['user_id']
    folder_id = request.args.get('folder_id', type=int)
    
    # Get files in the specified folder (or root if None)
    files = File.query.filter_by(user_id=user_id, folder_id=folder_id).all()
    folders = Folder.query.filter_by(user_id=user_id, parent_folder_id=folder_id).all()
    
    return jsonify({
        'files': [f.to_dict() for f in files],
        'folders': [f.to_dict() for f in folders],
        'current_folder_id': folder_id
    }), 200

@file_manager_bp.route('/folders/create', methods=['POST'])
@jwt_required()
def create_folder():
    """Create a new folder"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Folder name is required'}), 400
    
    folder_name = data['name']
    parent_folder_id = data.get('parent_folder_id')
    
    # Validate parent folder if specified
    parent_folder = None
    folder_path = folder_name
    
    if parent_folder_id:
        parent_folder = Folder.query.filter_by(id=parent_folder_id, user_id=user_id).first()
        if not parent_folder:
            return jsonify({'error': 'Parent folder not found'}), 404
        folder_path = os.path.join(parent_folder.folder_path, folder_name).replace('\\', '/')
    
    # Check if folder already exists
    existing = Folder.query.filter_by(
        user_id=user_id,
        folder_name=folder_name,
        parent_folder_id=parent_folder_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Folder already exists'}), 400
    
    # Create folder in filesystem
    user_folder = get_user_base_path(user_id)
    physical_path = os.path.join(user_folder, folder_path)
    os.makedirs(physical_path, exist_ok=True)
    
    # Create database entry
    new_folder = Folder(
        user_id=user_id,
        folder_name=folder_name,
        parent_folder_id=parent_folder_id,
        folder_path=folder_path
    )
    
    db.session.add(new_folder)
    db.session.commit()
    
    return jsonify({
        'message': 'Folder created successfully',
        'folder': new_folder.to_dict()
    }), 201

@file_manager_bp.route('/files/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    """Delete a file"""
    user_id = get_jwt_identity()
    
    # Get file and verify ownership
    file = File.query.filter_by(id=file_id, user_id=user_id).first()
    
    if not file:
        return jsonify({'error': 'File not found or access denied'}), 404
    
    # Delete physical file
    user_folder = get_user_base_path(user_id)
    file_path = os.path.join(user_folder, file.file_path)
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete database entry
    db.session.delete(file)
    db.session.commit()
    
    return jsonify({'message': 'File deleted successfully'}), 200

@file_manager_bp.route('/folders/<int:folder_id>', methods=['DELETE'])
@jwt_required()
def delete_folder(folder_id):
    """Delete a folder and all its contents"""
    user_id = get_jwt_identity()
    
    # Get folder and verify ownership
    folder = Folder.query.filter_by(id=folder_id, user_id=user_id).first()
    
    if not folder:
        return jsonify({'error': 'Folder not found or access denied'}), 404
    
    # Delete physical folder
    user_folder = get_user_base_path(user_id)
    folder_path = os.path.join(user_folder, folder.folder_path)
    
    if os.path.exists(folder_path):
        import shutil
        shutil.rmtree(folder_path)
    
    # Delete database entry (cascade will handle files and subfolders)
    db.session.delete(folder)
    db.session.commit()
    
    return jsonify({'message': 'Folder deleted successfully'}), 200

@file_manager_bp.route('/files/<int:file_id>/rename', methods=['PUT'])
@jwt_required()
def rename_file(file_id):
    """Rename a file"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('new_name'):
        return jsonify({'error': 'New name is required'}), 400
    
    # Get file and verify ownership
    file = File.query.filter_by(id=file_id, user_id=user_id).first()
    
    if not file:
        return jsonify({'error': 'File not found or access denied'}), 404
    
    new_name = secure_filename_custom(data['new_name'])
    
    # Rename physical file
    user_folder = get_user_base_path(user_id)
    old_path = os.path.join(user_folder, file.file_path)
    new_path = os.path.join(os.path.dirname(old_path), new_name)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
    
    # Update database entry
    file.filename = new_name
    file.original_filename = data['new_name']
    file.file_path = os.path.relpath(new_path, user_folder)
    file.mime_type = get_mime_type(new_name)
    
    db.session.commit()
    
    return jsonify({
        'message': 'File renamed successfully',
        'file': file.to_dict()
    }), 200

@file_manager_bp.route('/folders/<int:folder_id>/rename', methods=['PUT'])
@jwt_required()
def rename_folder(folder_id):
    """Rename a folder"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('new_name'):
        return jsonify({'error': 'New name is required'}), 400
    
    # Get folder and verify ownership
    folder = Folder.query.filter_by(id=folder_id, user_id=user_id).first()
    
    if not folder:
        return jsonify({'error': 'Folder not found or access denied'}), 404
    
    new_name = data['new_name']
    
    # Update folder path
    old_path = folder.folder_path
    if folder.parent_folder_id:
        parent = Folder.query.get(folder.parent_folder_id)
        new_folder_path = os.path.join(parent.folder_path, new_name).replace('\\', '/')
    else:
        new_folder_path = new_name
    
    # Rename physical folder
    user_folder = get_user_base_path(user_id)
    old_physical_path = os.path.join(user_folder, old_path)
    new_physical_path = os.path.join(user_folder, new_folder_path)
    
    if os.path.exists(old_physical_path):
        os.rename(old_physical_path, new_physical_path)
    
    # Update database entry
    folder.folder_name = new_name
    folder.folder_path = new_folder_path
    
    db.session.commit()
    
    return jsonify({
        'message': 'Folder renamed successfully',
        'folder': folder.to_dict()
    }), 200

@file_manager_bp.route('/files/<int:file_id>/move', methods=['PUT'])
@jwt_required()
def move_file(file_id):
    """Move a file to a different folder"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_folder_id = data.get('folder_id')  # None for root
    
    # Get file and verify ownership
    file = File.query.filter_by(id=file_id, user_id=user_id).first()
    
    if not file:
        return jsonify({'error': 'File not found or access denied'}), 404
    
    # Validate new folder if specified
    new_folder = None
    if new_folder_id:
        new_folder = Folder.query.filter_by(id=new_folder_id, user_id=user_id).first()
        if not new_folder:
            return jsonify({'error': 'Target folder not found'}), 404
    
    # Move physical file
    user_folder = get_user_base_path(user_id)
    old_path = os.path.join(user_folder, file.file_path)
    
    if new_folder:
        new_dir = os.path.join(user_folder, new_folder.folder_path.lstrip('/'))
    else:
        new_dir = user_folder
    
    os.makedirs(new_dir, exist_ok=True)
    new_path = os.path.join(new_dir, file.filename)
    
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
    
    # Update database entry
    file.folder_id = new_folder_id
    file.file_path = os.path.relpath(new_path, user_folder)
    
    db.session.commit()
    
    return jsonify({
        'message': 'File moved successfully',
        'file': file.to_dict()
    }), 200
