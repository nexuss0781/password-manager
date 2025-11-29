from flask import Flask, render_template, redirect, url_for, session, send_file, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db
from auth import auth_bp, login_required
from file_manager import file_manager_bp
import os

def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(file_manager_bp)
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Web routes (for UI)
    @app.route('/')
    def index():
        """Landing page"""
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return render_template('index.html')
    
    @app.route('/login')
    def login_page():
        """Login page"""
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    
    @app.route('/register')
    def register_page():
        """Registration page"""
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return render_template('register.html')
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """File manager dashboard"""
        return render_template('dashboard.html')
    
    @app.route('/download/client')
    def download_client():
        """Serve the Nexus client for download"""
        client_file = os.path.join(app.config['BASE_DIR'], 'nexus_client.py')
        if os.path.exists(client_file):
            return send_file(
                client_file,
                as_attachment=True,
                download_name='nexus_client.py',
                mimetype='text/x-python'
            )
        else:
            return {'error': 'Client file not found'}, 404
    
    @app.route('/install')
    def install_page():
        """Installation instructions page"""
        server_url = request.host_url.rstrip('/')
        return render_template('install.html', server_url=server_url)

    @app.route('/documentation')
    def documentation_page():
        """Documentation page"""
        return render_template('documentation.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return {'error': 'File too large. Maximum size is 100MB'}, 413
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("File Manager System starting...")
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    print(f"Access the application at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
