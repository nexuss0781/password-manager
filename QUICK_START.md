# FileVault Client - Quick Start Demo

## 🎉 NEW FEATURES - Enhanced Professional CLI

I've upgraded the FileVault client with these **amazing new features**:

### ✨ What's New

1. **✅ Wildcard Support** - Upload files with patterns like `*.pdf`, `*.jpg`, or `**/*.py`
2. **✅ Better Error Handling** - Custom exceptions and clear error messages
3. **✅ Colored Output** - Beautiful terminal output with colors and symbols
4. **✅ Batch Upload** - Upload multiple files at once with progress tracking
5. **✅ Easy Distribution** - Can be installed globally or shared as standalone file
6. **✅ Professional Features** - `whoami`, version info, help system

---

## 🚀 Quick Examples

### Upload ALL PDFs in current directory
```bash
.\venv\Scripts\python filevault_client.py upload *.pdf
```

### Upload ALL images (multiple patterns)
```bash
.\venv\Scripts\python filevault_client.py upload *.jpg *.png *.gif
```

### Upload ALL Python files recursively (in all subdirectories)
```bash
.\venv\Scripts\python filevault_client.py upload **/*.py --recursive
```

### Upload multiple specific files at once
```bash
.\venv\Scripts\python filevault_client.py upload file1.pdf file2.docx file3.txt
```

### Upload entire directory
```bash
.\venv\Scripts\python filevault_client.py upload-dir "C:\Users\YourName\Documents"
```

---

## 📋 Complete Command Reference

### Login (One Time)
```bash
.\venv\Scripts\python filevault_client.py login test@example.com testpass123
```

Configuration is saved to `~/.filevault_config.json` - you stay logged in!

### Upload Commands

```bash
# Single file
.\venv\Scripts\python filevault_client.py upload document.pdf

# Multiple files
.\venv\Scripts\python filevault_client.py upload file1.txt file2.txt file3.txt

# All PDFs
.\venv\Scripts\python filevault_client.py upload *.pdf

# All images
.\venv\Scripts\python filevault_client.py upload *.jpg *.png

# All text files to specific folder
.\venv\Scripts\python filevault_client.py upload *.txt --folder-id 5

# All Python files recursively
.\venv\Scripts\python filevault_client.py upload **/*.py --recursive

# Entire directory
.\venv\Scripts\python filevault_client.py upload-dir ./my_folder
```

### List Files
```bash
# List all files
.\venv\Scripts\python filevault_client.py list

# List files in folder
.\venv\Scripts\python filevault_client.py list --folder-id 10
```

### Download Files
```bash
# Download by ID
.\venv\Scripts\python filevault_client.py download 123

# Download with custom name
.\venv\Scripts\python filevault_client.py download 123 --output myfile.pdf
```

### Create Folder
```bash
# Create folder at root
.\venv\Scripts\python filevault_client.py mkdir "My Documents"

# Create subfolder
.\venv\Scripts\python filevault_client.py mkdir "Photos" --parent-id 5
```

### Check Current User
```bash
.\venv\Scripts\python filevault_client.py whoami
```

### Get Help
```bash
# General help
.\venv\Scripts\python filevault_client.py --help

# Command-specific help
.\venv\Scripts\python filevault_client.py upload --help
.\venv\Scripts\python filevault_client.py download --help
```

---

## 🎨 Beautiful Output Examples

When you upload files, you'll see colorful, informative output:

```
✓ Login successful!
ℹ User: testuser
ℹ Email: test@example.com

ℹ Found 3 file(s) to upload

[1/3] ⬆ Uploading document.pdf (2.45 MB)...
✓ Uploaded document.pdf
ℹ   File ID: 123

[2/3] ⬆ Uploading report.docx (1.23 MB)...
✓ Uploaded report.docx
ℹ   File ID: 124

[3/3] ⬆ Uploading photo.jpg (0.89 MB)...
✓ Uploaded photo.jpg
ℹ   File ID: 125

============================================================
✓ Successfully uploaded: 3
============================================================
```

---

## 📦 How to Share with Other Users (WITHOUT Your Codebase!)

### Method 1: Simple Download (Easiest)

Just share the `filevault_client.py` file!

**For you:**
1. Upload `filevault_client.py` to GitHub, Google Drive, or your server

**For users:**
```bash
# Download the file
curl -O https://your-server.com/filevault_client.py

# Install dependency
pip install requests

# Use it!
python filevault_client.py login user@email.com password
python filevault_client.py upload *.pdf
```

### Method 2: Install Globally (Professional)

**Make it a real command!**

```bash
# Install globally
cd "c:\Users\Pc5\Documents\password manager"
pip install .

# Now use 'filevault' command from ANYWHERE!
filevault login user@email.com password
filevault upload *.pdf
filevault list
```

Users can install from:
- GitHub: `pip install git+https://github.com/you/filevault.git`
- Local: `pip install filevault_client-1.0.0-py3-none-any.whl`
- PyPI: `pip install filevault-client` (if you publish it)

### Method 3: Standalone Executable (No Python!)

Create `.exe` file for Windows users:

```bash
pip install pyinstaller
pyinstaller --onefile --name filevault filevault_client.py
```

Users just double-click `filevault.exe`!

---

## 🔧 Real-World Usage Scenarios

### Scenario 1: Backup Your Documents
```bash
# Login once
.\venv\Scripts\python filevault_client.py login you@email.com password

# Upload all documents
.\venv\Scripts\python filevault_client.py upload-dir "C:\Users\You\Documents"

# Verify
.\venv\Scripts\python filevault_client.py list
```

### Scenario 2: Share Project Files with Team
```bash
# Create project folder (use web UI to get folder ID)
.\venv\Scripts\python filevault_client.py mkdir "Project Alpha"

# Upload all project files
.\venv\Scripts\python filevault_client.py upload-dir "C:\Projects\Alpha" --folder-id 42
```

### Scenario 3: Organize Photos
```bash
# Create folders
.\venv\Scripts\python filevault_client.py mkdir "Photos"
# Get folder ID from list command, then:

# Upload all photos
.\venv\Scripts\python filevault_client.py upload *.jpg *.png --folder-id 10
```

### Scenario 4: Code Backup
```bash
# Upload all code files from entire project
.\venv\Scripts\python filevault_client.py upload **/*.{py,js,html,css} --recursive
```

---

## 🌐 Remote Server Usage

### Connect to remote server
```bash
.\venv\Scripts\python filevault_client.py --server https://files.yourcompany.com login user@email.com pass
```

Server URL is saved, so next commands use it automatically:
```bash
.\venv\Scripts\python filevault_client.py upload *.pdf
```

---

## 🛡️ Error Handling Examples

The client gives clear, helpful errors:

**Not logged in:**
```
✗ Authentication error: Not logged in. Please login first.
ℹ Please login first: filevault login <email> <password>
```

**Network error:**
```
✗ Network error: Could not connect to server at http://localhost:5000
ℹ Make sure the server is running at http://localhost:5000
```

**File not found:**
```
✗ Error: File not found: C:\nonexistent.pdf
```

---

## 📚 Additional Documentation

- **[README_CLIENT.md](file:///c:/Users/Pc5/Documents/password%20manager/README_CLIENT.md)** - Complete client documentation
- **[DISTRIBUTION_GUIDE.md](file:///c:/Users/Pc5/Documents/password%20manager/DISTRIBUTION_GUIDE.md)** - How to share with users
- **[API_USAGE.md](file:///c:/Users/Pc5/Documents/password%20manager/API_USAGE.md)** - API reference

---

## 🎯 Summary

**You asked for:**
1. ✅ Easy wildcard upload (`*.pdf`)
2. ✅ Better exceptions and error handling
3. ✅ More features (colored output, batch upload, progress)
4. ✅ Easy distribution to users without codebase

**You got:**
- Professional CLI tool
- Wildcard support with glob patterns
- Beautiful colored output
- Robust error handling
- 4 distribution methods
- Complete documentation

**Test it now:**
```bash
cd "c:\Users\Pc5\Documents\password manager"

# Make sure server is running
.\venv\Scripts\python app.py

# In another terminal, try the new client:
.\venv\Scripts\python filevault_client.py login test@example.com testpass123
.\venv\Scripts\python filevault_client.py upload *.md *.txt
.\venv\Scripts\python filevault_client.py list
```

🎉 **Your FileVault client is now professional-grade and ready to distribute!**
