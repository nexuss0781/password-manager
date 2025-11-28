# FileVault Client

**Professional command-line client for FileVault remote file management**

## Installation

### Method 1: Install from source (Recommended for distribution)

```bash
# Clone or download the client
git clone <your-repo-url>
cd filevault

# Install the client globally
pip install .

# Or install in development mode
pip install -e .
```

After installation, you can use the `filevault` command from anywhere!

### Method 2: Standalone script (No installation)

```bash
# Just download the client script
curl -O https://your-server.com/filevault_client.py

# Or use directly
python filevault_client.py <command>
```

## Quick Start

### 1. Login
```bash
filevault login user@example.com mypassword
```

Your authentication token is saved securely in `~/.filevault_config.json`

### 2. Upload Files

#### Upload all PDFs in current directory
```bash
filevault upload *.pdf
```

#### Upload all images
```bash
filevault upload *.jpg *.png *.gif
```

#### Upload all Python files recursively
```bash
filevault upload **/*.py --recursive
```

#### Upload multiple specific files
```bash
filevault upload document.pdf report.docx presentation.pptx
```

#### Upload to a specific folder
```bash
filevault upload *.txt --folder-id 5
```

### 3. Upload Directories
```bash
# Upload all files in a directory
filevault upload-dir ./my_documents

# Upload directory recursively (default)
filevault upload-dir ./project --recursive
```

### 4. List Files
```bash
# List all files and folders
filevault list

# List files in a specific folder
filevault list --folder-id 10
```

### 5. Download Files
```bash
# Download by file ID
filevault download 123

# Download and save with specific name
filevault download 123 --output myfile.pdf
```

### 6. Create Folders
```bash
# Create a folder at root
filevault mkdir "My Documents"

# Create a subfolder
filevault mkdir "Photos" --parent-id 5
```

### 7. Check Current User
```bash
filevault whoami
```

## Features

✅ **Wildcard Support**: Upload files using `*`, `**`, and other glob patterns  
✅ **Batch Upload**: Upload multiple files at once  
✅ **Directory Upload**: Upload entire directories recursively  
✅ **Error Handling**: Robust exception handling with helpful error messages  
✅ **Color Output**: Beautiful colored terminal output for better UX  
✅ **Progress Tracking**: See upload progress for each file  
✅ **Secure Authentication**: JWT tokens stored securely  
✅ **Network Error Recovery**: Handles connection issues gracefully  
✅ **Cross-Platform**: Works on Windows, Linux, and macOS  

## Configuration

Configuration is automatically saved to `~/.filevault_config.json` after login:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "user_info": {
    "username": "john",
    "email": "john@example.com"
  },
  "server_url": "http://localhost:5000",
  "last_updated": "2025-11-28T13:00:00"
}
```

## Working with Remote Servers

### Connect to a remote server
```bash
filevault --server https://filevault.yourcompany.com login user@email.com pass
```

The server URL is saved after login, so subsequent commands use it automatically:
```bash
filevault upload *.pdf
filevault list
```

## Advanced Usage Examples

### Upload all documents from multiple folders
```bash
filevault upload ~/Documents/**/*.pdf ~/Downloads/**/*.docx --recursive
```

### Upload with folder organization
```bash
# Create folder first
filevault mkdir "Project Files"
# List to get folder ID
filevault list
# Upload to that folder
filevault upload ./project/* --folder-id 42
```

### Batch operations
```bash
# Upload all images
filevault upload ~/Pictures/**/*.{jpg,png,gif} --recursive

# Upload all code files
filevault upload **/*.{py,js,html,css} --recursive
```

## Error Handling

The client provides clear error messages:

- **Authentication errors**: Tells you to login
- **Network errors**: Shows connection issues
- **File not found**: Displays which files couldn't be found
- **Upload failures**: Shows which files failed and why

Example output:
```
✓ Login successful!
ℹ User: john
ℹ Email: john@example.com

ℹ Found 3 file(s) to upload

[1/3] ⬆ Uploading document.pdf (2.45 MB)...
✓ Uploaded document.pdf
ℹ File ID: 123

[2/3] ⬆ Uploading photo.jpg (1.82 MB)...
✓ Uploaded photo.jpg
ℹ File ID: 124

[3/3] ⬆ Uploading report.docx (0.56 MB)...
✓ Uploaded report.docx
ℹ File ID: 125

============================================================
✓ Successfully uploaded: 3
============================================================
```

## Distribution to Other Users

### Option 1: PyPI Distribution (Professional)

1. Package the client:
```bash
python setup.py sdist bdist_wheel
```

2. Upload to PyPI:
```bash
pip install twine
twine upload dist/*
```

3. Users install with:
```bash
pip install filevault-client
```

### Option 2: Direct Download (Simple)

1. Host `filevault_client.py` on your server or GitHub

2. Users download:
```bash
curl -O https://your-server.com/filevault_client.py
chmod +x filevault_client.py  # Unix/Linux/Mac
```

3. Users run:
```bash
python filevault_client.py login user@email.com password
python filevault_client.py upload *.pdf
```

### Option 3: Standalone Executable (No Python Required)

Create standalone executables using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile filevault_client.py

# Distribute the executable from dist/
```

Users can run without Python installed:
- Windows: `filevault_client.exe upload *.pdf`
- Linux/Mac: `./filevault_client upload *.pdf`

## Requirements

- Python 3.7+
- `requests` library

Install dependencies:
```bash
pip install requests
```

## Security Notes

- Tokens are stored in `~/.filevault_config.json` with user-only permissions
- Always use HTTPS in production: `--server https://your-server.com`
- Tokens expire after 24 hours (configurable on server)
- Never share your config file or token

## Troubleshooting

### "Not logged in" error
```bash
filevault login your@email.com password
```

### Connection refused
```bash
# Make sure server is running
python app.py

# Or check if using remote server
filevault --server http://your-server:5000 login user@email.com pass
```

### No files found
```bash
# Check your wildcard pattern
filevault upload *.pdf  # Current directory only
filevault upload **/*.pdf --recursive  # Recursive search
```

## Support

For issues, questions, or feature requests, please visit:
- GitHub: https://github.com/yourusername/filevault
- Email: support@yourcompany.com

## License

MIT License - See LICENSE file for details

---

**FileVault Client v1.0.0** - Professional remote file management at your fingertips 🚀
