# FileVault Client - Distribution Guide

## How to Share the Client with Other Users

This guide shows you how to distribute the FileVault client so anyone can use it without needing your entire codebase.

## Method 1: Install via pip (Most Professional)

### For You (Publisher):

1. **Update setup.py** with your information:
   - Change `url` to your GitHub repo
   - Update author information

2. **Create distribution packages**:
```bash
cd "c:\Users\Pc5\Documents\password manager"

# Install build tools
pip install build twine

# Build distribution
python -m build
```

3. **Upload to PyPI** (optional - for public distribution):
```bash
twine upload dist/*
```

OR **Host on your own server**:
- Just share the generated `.whl` file from `dist/` folder

### For Users:

Users install with one command:

```bash
# From PyPI (if you uploaded)
pip install filevault-client

# From local file (if you shared .whl)
pip install filevault_client-1.0.0-py3-none-any.whl

# From GitHub
pip install git+https://github.com/yourusername/filevault.git
```

Then they can use the `filevault` command anywhere!

---

## Method 2: Single-File Distribution (Simplest)

### For You (Publisher):

Just share the `filevault_client.py` file:

1. Upload to GitHub, Google Drive, or your server
2. Share the download link

### For Users:

```bash
# Download the file
curl -O https://your-server.com/filevault_client.py

# Use it directly
python filevault_client.py login user@email.com password
python filevault_client.py upload *.pdf
```

That's it! No installation needed.

---

## Method 3: Standalone Executable (No Python Required)

### For You (Publisher):

Create executables for Windows, Linux, and Mac:

```bash
cd "c:\Users\Pc5\Documents\password manager"

# Install PyInstaller
pip install pyinstaller

# Create Windows executable
pyinstaller --onefile --name filevault filevault_client.py

# The executable will be in dist/filevault.exe
```

For **cross-platform** executables:
```bash
# Windows
pyinstaller --onefile --name filevault-windows filevault_client.py

# On Linux (run on Linux machine)
pyinstaller --onefile --name filevault-linux filevault_client.py

# On Mac (run on Mac)
pyinstaller --onefile --name filevault-mac filevault_client.py
```

### For Users:

They just download and run the executable (no Python needed!):

**Windows:**
```cmd
filevault.exe login user@email.com password
filevault.exe upload *.pdf
```

**Linux/Mac:**
```bash
chmod +x filevault-linux
./filevault-linux login user@email.com password
./filevault-linux upload *.pdf
```

---

## Method 4: Docker Container

### For You (Publisher):

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY filevault_client.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "filevault_client.py"]
```

Build and share:
```bash
docker build -t filevault-client .
docker push yourusername/filevault-client
```

### For Users:

```bash
docker pull yourusername/filevault-client

# Use it
docker run filevault-client login user@email.com password
docker run -v $(pwd):/files filevault-client upload /files/*.pdf
```

---

## Quick Start Guide for Users (What to Send Them)

Send users this guide:

### 📥 Getting Started with FileVault Client

#### Step 1: Get the Client

**Option A - Install with pip** (recommended):
```bash
pip install filevault-client
```

**Option B - Download single file**:
```bash
curl -O https://your-server.com/filevault_client.py
```

**Option C - Download executable** (no Python needed):
- Download `filevault.exe` (Windows) or `filevault` (Linux/Mac)
- [Download Link]

#### Step 2: Connect to Server

```bash
# Replace with your email and password
filevault login your@email.com yourpassword

# Or specify server
filevault --server https://files.company.com login your@email.com password
```

#### Step 3: Upload Files

```bash
# Upload all PDFs
filevault upload *.pdf

# Upload all images
filevault upload *.jpg *.png

# Upload entire folder
filevault upload-dir ./my_documents
```

#### Step 4: Manage Files

```bash
# List files
filevault list

# Download file
filevault download 123

# Create folder
filevault mkdir "My Folder"
```

That's it! 🎉

---

## Requirements File for Users

Create `requirements.txt`:
```
requests>=2.28.0
```

Users install dependencies:
```bash
pip install -r requirements.txt
```

---

## Testing the Distribution

Before sharing, test on a clean machine:

1. **Create fresh virtual environment**:
```bash
python -m venv test_env
test_env\Scripts\activate  # Windows
source test_env/bin/activate  # Linux/Mac
```

2. **Test installation**:
```bash
pip install dist/filevault_client-1.0.0-py3-none-any.whl
filevault --version
```

3. **Test functionality**:
```bash
filevault login test@example.com testpass123
filevault upload test.txt
filevault list
```

---

## Update Instructions for Users

When you release a new version:

```bash
# For pip installation
pip install --upgrade filevault-client

# For single file
curl -O https://your-server.com/filevault_client.py --output filevault_client.py

# For executable
# Download new version and replace old file
```

---

## Best Distribution Method by Use Case

| Use Case | Best Method | Pros |
|----------|-------------|------|
| **Internal company tool** | Method 1 (pip) | Professional, easy updates |
| **Quick sharing with colleague** | Method 2 (single file) | Simplest, no installation |
| **Non-technical users** | Method 3 (executable) | No Python required |
| **Enterprise deployment** | Method 4 (Docker) | Isolated, reproducible |

---

## Real-World Distribution Example

Let's say you want to share with your team:

### 1. Create a GitHub repo:
```
filevault-client/
├── filevault_client.py
├── setup.py
├── README_CLIENT.md
├── requirements.txt
└── LICENSE
```

### 2. Users install:
```bash
# Clone and install
git clone https://github.com/yourcompany/filevault-client.git
cd filevault-client
pip install .

# Or install directly from GitHub
pip install git+https://github.com/yourcompany/filevault-client.git
```

### 3. They use it:
```bash
filevault login user@company.com password
filevault upload *.pdf --server https://files.company.com
```

Perfect! Everyone has the same tool, easy to update! 🚀

---

## Support Documentation to Share

Include this in your distribution:

**Server Connection**:
- Internal users: `http://192.168.1.100:5000`
- Remote users: `https://files.yourcompany.com`

**Support Contact**:
- Email: it-support@yourcompany.com
- Slack: #filevault-support

**Common Issues**:
1. Connection refused → Check VPN connection
2. Login failed → Reset password at portal
3. Upload failed → Check file size < 100MB

---

You now have **4 professional ways** to distribute your FileVault client! 🎉
