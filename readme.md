# 🚀 FileVault - Remote File Manager System

A modern, secure web-based file management system that allows users to remotely manage their files through a REST API and intuitive web interface.

![FileVault](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

## ✨ Features

- 🔐 **User Authentication** - Secure registration and login with JWT tokens
- 📤 **File Upload** - Upload files via web interface or API with drag-and-drop support
- 📥 **File Download** - Download files with original names preserved
- 📁 **Folder Management** - Create, rename, and delete folders
- ✏️ **File Operations** - Rename, move, and delete files
- 🎨 **Modern UI** - Beautiful interface with glassmorphism and smooth animations
- 🔒 **Security** - User isolation, path validation, and file type restrictions
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- 🌐 **REST API** - Full-featured API for programmatic access

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Authentication**: Flask-JWT-Extended
- **Styling**: Custom CSS with glassmorphism effects

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "password manager"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables** (optional)
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and set your secret keys.

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 🎯 Usage

### Web Interface

1. **Register** a new account at `/register`
2. **Login** to your account at `/login`
3. **Upload files** by clicking the "Upload File" button or drag-and-drop
4. **Create folders** to organize your files
5. **Manage files** - rename, move, download, or delete files and folders

### API Endpoints

#### Authentication

**Register**
```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Login**
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure_password"
}
```

Response:
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### File Management

**Upload File**
```bash
POST /api/files/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <file_data>
folder_id: <optional_folder_id>
```

**List Files**
```bash
GET /api/files/list?folder_id=<optional_folder_id>
Authorization: Bearer <access_token>
```

**Download File**
```bash
GET /api/files/download/<file_id>
Authorization: Bearer <access_token>
```

**Delete File**
```bash
DELETE /api/files/<file_id>
Authorization: Bearer <access_token>
```

**Rename File**
```bash
PUT /api/files/<file_id>/rename
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "new_name": "new_filename.txt"
}
```

**Move File**
```bash
PUT /api/files/<file_id>/move
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "folder_id": <target_folder_id>
}
```

#### Folder Management

**Create Folder**
```bash
POST /api/folders/create
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "My Folder",
  "parent_folder_id": <optional_parent_id>
}
```

**Delete Folder**
```bash
DELETE /api/folders/<folder_id>
Authorization: Bearer <access_token>
```

**Rename Folder**
```bash
PUT /api/folders/<folder_id>/rename
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "new_name": "New Folder Name"
}
```

## 🔒 Security Features

- **Password Hashing**: Werkzeug's secure password hashing
- **JWT Authentication**: Secure token-based API authentication
- **User Isolation**: Each user has their own isolated storage space
- **Path Validation**: Prevents directory traversal attacks
- **File Type Restrictions**: Configurable allowed file extensions
- **File Size Limits**: Maximum upload size of 100MB (configurable)

## 🎨 Features Showcase

### Modern UI Design
- Glassmorphism effects
- Gradient backgrounds
- Smooth animations and transitions
- Responsive layout
- Dark mode compatible

### File Operations
- Upload multiple files simultaneously
- Drag-and-drop file upload
- Real-time upload progress
- File preview icons by type
- Breadcrumb navigation

## 📝 Configuration

Edit `config.py` to customize:

- **UPLOAD_FOLDER**: Directory for file storage
- **MAX_CONTENT_LENGTH**: Maximum file size (default: 100MB)
- **ALLOWED_EXTENSIONS**: Permitted file types
- **JWT_ACCESS_TOKEN_EXPIRES**: Token expiration time
- **CORS_ORIGINS**: Allowed CORS origins

## 🚀 Deployment

For production deployment:

1. Set strong secret keys in `.env`
2. Use a production WSGI server (e.g., Gunicorn)
3. Use a production database (e.g., PostgreSQL)
4. Configure HTTPS with SSL/TLS
5. Set up proper CORS origins
6. Enable logging and monitoring

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Built with ❤️ for secure and efficient file management.

## 🆘 Support

For issues and questions, please open an issue on the repository.

---

**FileVault** - Your files, anywhere, anytime. 🔐
