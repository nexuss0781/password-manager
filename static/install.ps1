# FileVault Client Installer for Windows
# Usage: iwr -useb https://your-server.com/install.ps1 | iex

param(
    [string]$ServerUrl = "http://localhost:5000"
)

# Configuration
$ClientFile = "filevault_client.py"
$ClientUrl = "$ServerUrl/download/client"

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║   FileVault Client Installer v1.0.0   ║" -ForegroundColor Blue
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    try {
        $pythonVersion = py --version 2>&1
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
        $PythonCmd = "py"
    } catch {
        Write-Host "✗ Python is not installed. Please install Python first." -ForegroundColor Red
        Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
}

if (-not $PythonCmd) {
    $PythonCmd = "python"
}

# Download the client
Write-Host "⬇ Downloading FileVault client from $ServerUrl..." -ForegroundColor Blue

try {
    Invoke-WebRequest -Uri $ClientUrl -OutFile $ClientFile -UseBasicParsing
    Write-Host "✓ Client downloaded successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to download client: $_" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Blue

try {
    & $PythonCmd -m pip install requests --quiet --user
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Failed to install dependencies. You may need to install 'requests' manually." -ForegroundColor Yellow
}

# Test installation
Write-Host ""
Write-Host "Testing installation..." -ForegroundColor Blue
& $PythonCmd $ClientFile --version

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   Installation Complete! 🎉            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "Quick start:" -ForegroundColor White
Write-Host "  $PythonCmd $ClientFile login your@email.com password" -ForegroundColor Cyan
Write-Host "  $PythonCmd $ClientFile upload *.pdf" -ForegroundColor Cyan
Write-Host "  $PythonCmd $ClientFile list" -ForegroundColor Cyan
Write-Host ""
Write-Host "For help: $PythonCmd $ClientFile --help" -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to create a shortcut
$response = Read-Host "Create 'filevault.bat' shortcut? (Y/N)"
if ($response -eq 'Y' -or $response -eq 'y') {
    $currentDir = (Get-Location).Path
    $batContent = "@echo off`n$PythonCmd `"$currentDir\$ClientFile`" %*"
    Set-Content -Path "filevault.bat" -Value $batContent
    
    Write-Host "✓ Created filevault.bat. You can now use: filevault <command>" -ForegroundColor Green
    Write-Host "  Add current directory to PATH to use from anywhere" -ForegroundColor Yellow
}
