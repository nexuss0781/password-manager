# FileVault Client - Installation Guide

## 🚀 One-Line Installation (When Server is Deployed)

### Windows (PowerShell)

**Method 1 - Direct download:**
```powershell
Invoke-WebRequest -Uri "https://your-filevault-server.com/download/client" -OutFile "filevault_client.py"
pip install requests
python filevault_client.py --help
```

**Method 2 - Automated installer:**
```powershell
iwr -useb https://your-filevault-server.com/install.ps1 | iex
```

### Linux/Mac

**Method 1 - Direct download (curl):**
```bash
curl -O https://your-filevault-server.com/download/client
mv client filevault_client.py
pip3 install requests
python3 filevault_client.py --help
```

**Method 2 - Direct download (wget):**
```bash
wget https://your-filevault-server.com/download/client -O filevault_client.py
pip3 install requests
python3 filevault_client.py --help
```

**Method 3 - Automated installer:**
```bash
curl -sSL https://your-filevault-server.com/install.sh | bash
```

---

## 📋 Installation Routes Available

When you deploy your FileVault server, these URLs will be available:

| URL | Description |
|-----|-------------|
| `https://your-server.com/install` | Web page with installation instructions |
| `https://your-server.com/download/client` | Direct download of filevault_client.py |
| `https://your-server.com/install.sh` | Automated installer for Linux/Mac |
| `https://your-server.com/install.ps1` | Automated installer for Windows |

---

## 🎯 Quick Start After Installation

### 1. Login to your server
```bash
# Replace with your actual server URL
python filevault_client.py --server https://your-server.com login your@email.com password
```

### 2. Upload files
```bash
# Upload all PDFs
python filevault_client.py upload *.pdf

# Upload all images
python filevault_client.py upload *.jpg *.png

# Upload entire directory
python filevault_client.py upload-dir ./my_documents
```

### 3. Manage files
```bash
# List files
python filevault_client.py list

# Download file
python filevault_client.py download 123

# Create folder
python filevault_client.py mkdir "My Documents"
```

---

## 🌐 For Users on Your Deployed Server

Share these instructions with your users:

### Installation Page
Direct them to: **https://your-filevault-server.com/install**

This page provides:
- ✅ Copy-paste installation commands
- ✅ Step-by-step guide
- ✅ Usage examples
- ✅ Direct download button

### Quick Install Commands

**Windows users:**
```powershell
Invoke-WebRequest -Uri "https://your-server.com/download/client" -OutFile "filevault_client.py"
pip install requests
```

**Linux/Mac users:**
```bash
curl -O https://your-server.com/download/client
mv client filevault_client.py
pip3 install requests
```

---

## 🔧 Server Configuration

### Serving the Installer Scripts

The installer scripts (`install.sh` and `install.ps1`) need to be accessible from your server.

**Two options:**

#### Option 1: Serve as static files
Put them in the `static` folder and they'll be accessible at:
- `https://your-server.com/static/install.sh`
- `https://your-server.com/static/install.ps1`

Update commands:
```bash
# Linux/Mac
curl -sSL https://your-server.com/static/install.sh | bash

# Windows
iwr -useb https://your-server.com/static/install.ps1 | iex
```

#### Option 2: Add routes (already configured)
The `/download/client` route is already added to `app.py` and serves `filevault_client.py`.

You can add similar routes for the installers if needed.

---

## 📦 Deployment Checklist

When deploying your server:

- [ ] Ensure `filevault_client.py` exists in project root
- [ ] Test `/download/client` endpoint works
- [ ] Update server URLs in documentation
- [ ] Copy `install.sh` and `install.ps1` to `static/` folder (optional)
- [ ] Test installation from a fresh machine
- [ ] Share installation page URL with users

---

## 🎨 Installation Page Features

The `/install` page includes:

✅ **Platform-specific commands** - Detects user's OS  
✅ **Copy buttons** - One-click copy to clipboard  
✅ **Step-by-step guide** - Visual installation steps  
✅ **Usage examples** - Common commands  
✅ **Direct download** - Backup download button  

Access it at: `https://your-server.com/install`

---

## 🔒 Security Notes

1. **HTTPS Required** - Always use HTTPS in production
2. **Download Verification** - Users can verify the downloaded file
3. **Dependency Safety** - Only requires `requests` package
4. **Token Storage** - Tokens stored securely in `~/.filevault_config.json`

---

## 📱 Example User Flow

1. **User visits**: `https://files.company.com/install`
2. **Copies command**: Windows or Linux command
3. **Pastes in terminal**: Downloads and installs client
4. **Logs in**: `python filevault_client.py login user@company.com pass`
5. **Uploads files**: `python filevault_client.py upload *.pdf`

**Done! User can now manage files remotely.** 🎉

---

## 🆘 Troubleshooting

### Download fails
- Check server is running
- Verify URL is correct
- Try direct download from `/download/client`

### "requests" module not found
```bash
pip install requests
# or
pip3 install requests --user
```

### Python not found
- Install Python from python.org
- Make sure Python is in PATH

### Permission denied (Linux/Mac)
```bash
chmod +x filevault_client.py
```

---

## 🌍 Custom Server URL

If your server is at a custom URL, users specify it:

```bash
python filevault_client.py --server https://custom.domain.com login user@email.com pass
```

The server URL is saved after first login!

---

**Your FileVault client is now downloadable and deployable!** 🚀
