#!/bin/bash
# FileVault Client Installer for Linux/Mac
# Usage: curl -sSL https://your-server.com/install.sh | bash

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SERVER_URL="${FILEVAULT_SERVER:-http://localhost:5000}"
INSTALL_DIR="$HOME/.local/bin"
CLIENT_FILE="filevault_client.py"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   FileVault Client Installer v1.0.0   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠ pip3 not found. Installing dependencies might fail.${NC}"
fi

# Download the client
echo -e "${BLUE}⬇ Downloading FileVault client from ${SERVER_URL}...${NC}"

if command -v curl &> /dev/null; then
    curl -sSL "${SERVER_URL}/download/client" -o "${CLIENT_FILE}"
elif command -v wget &> /dev/null; then
    wget -q "${SERVER_URL}/download/client" -O "${CLIENT_FILE}"
else
    echo -e "${RED}✗ Neither curl nor wget found. Please install one of them.${NC}"
    exit 1
fi

if [ ! -f "${CLIENT_FILE}" ]; then
    echo -e "${RED}✗ Failed to download client${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Client downloaded successfully${NC}"

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip3 install requests --quiet --user || pip3 install requests --user

echo -e "${GREEN}✓ Dependencies installed${NC}"

# Make executable
chmod +x "${CLIENT_FILE}"

# Optional: Install to PATH
read -p "Install to PATH? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p "${INSTALL_DIR}"
    
    # Create wrapper script
    cat > "${INSTALL_DIR}/filevault" << EOF
#!/bin/bash
python3 "$(pwd)/${CLIENT_FILE}" "\$@"
EOF
    
    chmod +x "${INSTALL_DIR}/filevault"
    
    # Check if directory is in PATH
    if [[ ":$PATH:" != *":${INSTALL_DIR}:"* ]]; then
        echo ""
        echo -e "${YELLOW}⚠ ${INSTALL_DIR} is not in your PATH${NC}"
        echo -e "Add this line to your ~/.bashrc or ~/.zshrc:"
        echo -e "${GREEN}export PATH=\"${INSTALL_DIR}:\$PATH\"${NC}"
    else
        echo -e "${GREEN}✓ Installed to ${INSTALL_DIR}/filevault${NC}"
    fi
fi

# Test installation
echo ""
echo -e "${BLUE}Testing installation...${NC}"
python3 "${CLIENT_FILE}" --version

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Installation Complete! 🎉            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "Quick start:"
echo -e "  ${BLUE}python3 ${CLIENT_FILE} login your@email.com password${NC}"
echo -e "  ${BLUE}python3 ${CLIENT_FILE} upload *.pdf${NC}"
echo -e "  ${BLUE}python3 ${CLIENT_FILE} list${NC}"
echo ""
echo -e "For help: ${BLUE}python3 ${CLIENT_FILE} --help${NC}"
