# FileVault API Usage Guide

## Quick Start: Upload Files from Your Local Machine

Yes! Users **can upload their own local files to the remote machine through the API**, similar to `git push`.

## Method 1: Using the Python Client (Recommended)

### Installation
```bash
# No installation needed, just use the client script
cd "c:\Users\Pc5\Documents\password manager"
```

### 1. Login to Your Account
```bash
python filevault_client.py login test@example.com testpass123
```

This saves your authentication token in `~/.filevault_config.json`

### 2. Upload a Single File
```bash
# Upload from anywhere on your local machine
python filevault_client.py upload C:\Users\YourName\Documents\report.pdf

# Upload to a specific folder
python filevault_client.py upload C:\Users\YourName\Pictures\photo.jpg --folder-id 5
```

### 3. Upload an Entire Directory
```bash
# Upload all files in a directory
python filevault_client.py upload-dir C:\Users\YourName\Documents\MyFiles

# Upload to a specific folder on the server
python filevault_client.py upload-dir C:\Projects\SourceCode --folder-id 3
```

### 4. List Your Files
```bash
# List all files at root
python filevault_client.py list

# List files in a specific folder
python filevault_client.py list --folder-id 5
```

### 5. Download Files
```bash
# Download a file by its ID
python filevault_client.py download 123

# Download and save with custom name
python filevault_client.py download 123 --output myfile.pdf
```

---

## Method 2: Using cURL (Command Line)

### 1. Login and Get Token
```bash
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"testpass123\"}"
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "user": {...}
}
```

### 2. Upload a File
```bash
# Replace YOUR_TOKEN with the token from login
curl -X POST http://localhost:5000/api/files/upload ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  -F "file=@C:\Users\YourName\Documents\document.pdf"
```

### 3. Upload to a Specific Folder
```bash
curl -X POST http://localhost:5000/api/files/upload ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  -F "file=@C:\path\to\file.txt" ^
  -F "folder_id=5"
```

### 4. List Files
```bash
curl http://localhost:5000/api/files/list ^
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5. Download a File
```bash
curl http://localhost:5000/api/files/download/123 ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  --output downloaded_file.pdf
```

---

## Method 3: Using PowerShell

### Upload a File
```powershell
# Login first
$loginData = @{
    email = "test@example.com"
    password = "testpass123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $loginData

$token = $response.access_token

# Upload file
$filePath = "C:\Users\YourName\Documents\file.pdf"
$headers = @{
    Authorization = "Bearer $token"
}

$form = @{
    file = Get-Item -Path $filePath
}

Invoke-RestMethod -Uri "http://localhost:5000/api/files/upload" `
    -Method POST `
    -Headers $headers `
    -Form $form
```

---

## Method 4: Using Python Requests Library

### Simple Upload Script
```python
import requests

# Login
login_data = {
    'email': 'test@example.com',
    'password': 'testpass123'
}
response = requests.post('http://localhost:5000/api/auth/login', json=login_data)
token = response.json()['access_token']

# Upload file
headers = {'Authorization': f'Bearer {token}'}
files = {'file': open('C:/Users/YourName/Documents/report.pdf', 'rb')}

response = requests.post(
    'http://localhost:5000/api/files/upload',
    headers=headers,
    files=files
)

print(response.json())
```

---

## Method 5: Using JavaScript/Node.js

### Upload from Node.js
```javascript
const fetch = require('node-fetch');
const FormData = require('form-data');
const fs = require('fs');

// Login
async function uploadFile() {
    // 1. Login
    const loginResponse = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            email: 'test@example.com',
            password: 'testpass123'
        })
    });
    
    const loginData = await loginResponse.json();
    const token = loginData.access_token;
    
    // 2. Upload file
    const form = new FormData();
    form.append('file', fs.createReadStream('C:/path/to/file.pdf'));
    
    const uploadResponse = await fetch('http://localhost:5000/api/files/upload', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: form
    });
    
    const uploadData = await uploadResponse.json();
    console.log('Upload successful:', uploadData);
}

uploadFile();
```

---

## Complete API Reference

### Authentication Endpoints

#### POST `/api/auth/register`
Register a new user
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "secure123"
}
```

#### POST `/api/auth/login`
Login and get JWT token
```json
{
  "email": "john@example.com",
  "password": "secure123"
}
```

#### POST `/api/auth/logout`
Logout current session

#### GET `/api/auth/me`
Get current user info (requires token)

---

### File Management Endpoints

#### POST `/api/files/upload`
Upload a file
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `multipart/form-data`
  - `file`: file data
  - `folder_id`: (optional) folder ID

#### GET `/api/files/download/<file_id>`
Download a file by ID
- **Headers**: `Authorization: Bearer <token>`

#### GET `/api/files/list`
List all files and folders
- **Headers**: `Authorization: Bearer <token>`
- **Query Params**: `folder_id` (optional)

#### DELETE `/api/files/<file_id>`
Delete a file
- **Headers**: `Authorization: Bearer <token>`

#### PUT `/api/files/<file_id>/rename`
Rename a file
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
```json
{
  "new_name": "newfilename.pdf"
}
```

#### PUT `/api/files/<file_id>/move`
Move a file to another folder
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
```json
{
  "folder_id": 5
}
```

---

### Folder Management Endpoints

#### POST `/api/folders/create`
Create a new folder
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
```json
{
  "name": "My Folder",
  "parent_folder_id": null
}
```

#### DELETE `/api/folders/<folder_id>`
Delete a folder and its contents
- **Headers**: `Authorization: Bearer <token>`

#### PUT `/api/folders/<folder_id>/rename`
Rename a folder
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
```json
{
  "new_name": "New Folder Name"
}
```

---

## Example Workflow: Push Files Like Git

### Scenario: Upload your project files to the server

```bash
# 1. Login once
python filevault_client.py login your@email.com yourpassword

# 2. Create a folder for your project
# (Use the web interface or API to get the folder ID)

# 3. Upload all files in your project directory
python filevault_client.py upload-dir C:\Projects\MyProject --folder-id 10

# 4. Update a single file
python filevault_client.py upload C:\Projects\MyProject\updated_file.txt --folder-id 10

# 5. List files to verify
python filevault_client.py list --folder-id 10
```

---

## Remote Server Configuration

If your FileVault server is on a remote machine (not localhost):

```bash
# Specify server URL
python filevault_client.py --server http://192.168.1.100:5000 login user@email.com pass

# Or for remote servers
python filevault_client.py --server https://filevault.yourcompany.com login user@email.com pass
```

---

## Security Notes

1. **HTTPS**: In production, always use HTTPS
2. **Token Storage**: Tokens are stored in `~/.filevault_config.json`
3. **Token Expiry**: Tokens expire after 24 hours (configurable)
4. **File Size Limit**: Maximum upload size is 100MB (configurable)

---

## Troubleshooting

### "Not logged in" error
```bash
# Login again
python filevault_client.py login your@email.com password
```

### Connection refused
```bash
# Make sure the server is running
python app.py
```

### File size too large
- Default limit is 100MB
- Configure in `config.py`: `MAX_CONTENT_LENGTH`

---

**FileVault API** - Upload files from anywhere to your remote server! 🚀
