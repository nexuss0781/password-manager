#!/usr/bin/env python3
"""
FileVault Client - Professional CLI for remote file management
Upload, download, and manage files on your FileVault server

Author: FileVault Team
Version: 1.0.0
"""

import os
import sys
import json
import argparse
import requests
import glob
from pathlib import Path
from typing import Optional, List
from datetime import datetime

# Configuration
CONFIG_FILE = os.path.expanduser('~/.filevault_config.json')
DEFAULT_SERVER = 'http://localhost:5000'
VERSION = '1.0.0'

# ANSI color codes for better terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    """Print success message in green"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message):
    """Print error message in red"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}", file=sys.stderr)

def print_warning(message):
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def print_info(message):
    """Print info message in cyan"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.RESET}")

def print_progress(message):
    """Print progress message in blue"""
    print(f"{Colors.BLUE}⬆ {message}{Colors.RESET}")


class FileVaultError(Exception):
    """Base exception for FileVault errors"""
    pass

class AuthenticationError(FileVaultError):
    """Authentication failed"""
    pass

class NetworkError(FileVaultError):
    """Network connection error"""
    pass

class FileNotFoundError(FileVaultError):
    """File not found error"""
    pass


class FileVaultClient:
    """Professional FileVault API client"""
    
    def __init__(self, server_url: str = DEFAULT_SERVER):
        self.server_url = server_url.rstrip('/')
        self.api_url = f"{self.server_url}/api"
        self.token: Optional[str] = None
        self.user_info: Optional[dict] = None
        self.load_config()
    
    def load_config(self) -> None:
        """Load saved configuration (token, server URL)"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.token = config.get('token')
                    self.user_info = config.get('user_info')
                    saved_server = config.get('server_url')
                    if saved_server:
                        self.server_url = saved_server
                        self.api_url = f"{self.server_url}/api"
            except Exception as e:
                print_warning(f"Could not load config: {e}")
    
    def save_config(self) -> None:
        """Save configuration to file"""
        config = {
            'token': self.token,
            'user_info': self.user_info,
            'server_url': self.server_url,
            'last_updated': datetime.now().isoformat()
        }
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
            print_info(f"Configuration saved to {CONFIG_FILE}")
        except Exception as e:
            print_warning(f"Could not save config: {e}")
    
    def get_headers(self) -> dict:
        """Get headers with authentication token"""
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.api_url}{endpoint}"
        
        try:
            response = requests.request(method, url, timeout=30, **kwargs)
            return response
        except requests.exceptions.ConnectionError:
            raise NetworkError(f"Could not connect to server at {self.server_url}")
        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {e}")
    
    def login(self, email: str, password: str) -> bool:
        """Login and get JWT token"""
        data = {'email': email, 'password': password}
        
        try:
            response = self._make_request('POST', '/auth/login', json=data)
            
            if response.status_code == 200:
                result = response.json()
                self.token = result.get('access_token')
                self.user_info = result.get('user')
                self.save_config()
                
                print_success("Login successful!")
                print_info(f"  User: {self.user_info.get('username')}")
                print_info(f"  Email: {self.user_info.get('email')}")
                return True
            else:
                error = response.json().get('error', 'Login failed')
                raise AuthenticationError(error)
                
        except NetworkError as e:
            print_error(str(e))
            return False
        except AuthenticationError as e:
            print_error(f"Authentication failed: {e}")
            return False
        except Exception as e:
            print_error(f"Unexpected error during login: {e}")
            return False
    
    def upload_file(self, file_path: str, folder_id: Optional[int] = None, 
                    show_progress: bool = True) -> bool:
        """Upload a single file to the server"""
        if not self.token:
            raise AuthenticationError("Not logged in. Please login first.")
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise FileNotFoundError(f"Not a file: {file_path}")
        
        try:
            file_size = file_path.stat().st_size
            size_mb = file_size / (1024 * 1024)
            
            if show_progress:
                print_progress(f"Uploading {file_path.name} ({size_mb:.2f} MB)...")
            
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.name, f)}
                data = {}
                
                if folder_id:
                    data['folder_id'] = folder_id
                
                response = self._make_request(
                    'POST',
                    '/files/upload',
                    headers=self.get_headers(),
                    files=files,
                    data=data
                )
                
                if response.status_code == 201:
                    result = response.json()
                    file_info = result.get('file', {})
                    
                    if show_progress:
                        print_success(f"Uploaded {file_path.name}")
                        print_info(f"  File ID: {file_info.get('id')}")
                    
                    return True
                else:
                    error = response.json().get('error', 'Upload failed')
                    raise FileVaultError(error)
                    
        except Exception as e:
            if show_progress:
                print_error(f"Failed to upload {file_path.name}: {e}")
            raise
    
    def upload_files(self, patterns: List[str], folder_id: Optional[int] = None,
                     recursive: bool = False) -> dict:
        """
        Upload multiple files using wildcards
        
        Args:
            patterns: List of file patterns (supports wildcards like *.pdf, *.jpg)
            folder_id: Optional folder ID to upload to
            recursive: If True, search directories recursively
        
        Returns:
            dict with 'success', 'failed', and 'skipped' counts
        """
        if not self.token:
            raise AuthenticationError("Not logged in. Please login first.")
        
        # Expand all patterns to get file list
        all_files = []
        for pattern in patterns:
            if recursive:
                # Recursive glob
                if '**' not in pattern:
                    pattern = f"**/{pattern}"
                files = glob.glob(pattern, recursive=True)
            else:
                files = glob.glob(pattern)
            
            all_files.extend([Path(f) for f in files if os.path.isfile(f)])
        
        # Remove duplicates
        all_files = list(set(all_files))
        
        if not all_files:
            print_warning("No files found matching the pattern(s)")
            return {'success': 0, 'failed': 0, 'skipped': 0}
        
        print_info(f"Found {len(all_files)} file(s) to upload\n")
        
        results = {'success': 0, 'failed': 0, 'skipped': 0}
        
        for i, file_path in enumerate(all_files, 1):
            try:
                print(f"[{i}/{len(all_files)}] ", end='')
                self.upload_file(file_path, folder_id, show_progress=True)
                results['success'] += 1
            except FileVaultError as e:
                print_error(f"Error: {e}")
                results['failed'] += 1
            except Exception as e:
                print_error(f"Unexpected error: {e}")
                results['failed'] += 1
        
        # Print summary
        print(f"\n{'='*60}")
        print_success(f"Successfully uploaded: {results['success']}")
        if results['failed'] > 0:
            print_error(f"Failed: {results['failed']}")
        print(f"{'='*60}\n")
        
        return results
    
    def upload_directory(self, dir_path: str, folder_id: Optional[int] = None,
                        recursive: bool = True) -> dict:
        """Upload all files in a directory"""
        dir_path = Path(dir_path)
        
        if not dir_path.exists() or not dir_path.is_dir():
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        
        # Get all files
        if recursive:
            pattern = str(dir_path / "**" / "*")
            files = [Path(f) for f in glob.glob(pattern, recursive=True) if os.path.isfile(f)]
        else:
            files = [f for f in dir_path.glob('*') if f.is_file()]
        
        if not files:
            print_warning(f"No files found in {dir_path}")
            return {'success': 0, 'failed': 0, 'skipped': 0}
        
        print_info(f"Found {len(files)} file(s) in {dir_path}\n")
        
        return self.upload_files([str(f) for f in files], folder_id)
    
    def list_files(self, folder_id: Optional[int] = None) -> bool:
        """List files and folders"""
        if not self.token:
            raise AuthenticationError("Not logged in. Please login first.")
        
        try:
            endpoint = '/files/list'
            if folder_id:
                endpoint += f"?folder_id={folder_id}"
            
            response = self._make_request('GET', endpoint, headers=self.get_headers())
            
            if response.status_code == 200:
                result = response.json()
                folders = result.get('folders', [])
                files = result.get('files', [])
                
                print(f"\n{Colors.BOLD}📁 Folders:{Colors.RESET}")
                if folders:
                    for folder in folders:
                        print(f"  {Colors.YELLOW}[DIR]{Colors.RESET}  {folder['name']} (ID: {folder['id']})")
                else:
                    print("  (none)")
                
                print(f"\n{Colors.BOLD}📄 Files:{Colors.RESET}")
                if files:
                    for file in files:
                        size_mb = file['size'] / (1024 * 1024)
                        print(f"  {Colors.GREEN}[FILE]{Colors.RESET} {file['name']:<40} {size_mb:>8.2f} MB  (ID: {file['id']})")
                else:
                    print("  (none)")
                
                print()  # Empty line
                return True
            else:
                error = response.json().get('error', 'Failed to list files')
                raise FileVaultError(error)
                
        except Exception as e:
            print_error(f"Error listing files: {e}")
            return False
    
    def download_file(self, file_id: int, output_path: Optional[str] = None) -> bool:
        """Download a file from the server"""
        if not self.token:
            raise AuthenticationError("Not logged in. Please login first.")
        
        try:
            print_progress(f"Downloading file ID {file_id}...")
            
            response = self._make_request(
                'GET',
                f'/files/download/{file_id}',
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                # Get filename from Content-Disposition header
                content_disposition = response.headers.get('Content-Disposition', '')
                filename = 'download'
                
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[1].strip('"')
                
                # Use provided output path or default filename
                save_path = output_path if output_path else filename
                
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                size_mb = len(response.content) / (1024 * 1024)
                print_success("Download complete!")
                print_info(f"  Saved to: {save_path}")
                print_info(f"  Size: {size_mb:.2f} MB")
                return True
            else:
                error_text = response.text
                try:
                    error = response.json().get('error', 'Download failed')
                except:
                    error = 'Download failed'
                raise FileVaultError(error)
                
        except Exception as e:
            print_error(f"Error downloading file: {e}")
            return False
    
    def whoami(self) -> bool:
        """Show current user info"""
        if not self.token:
            print_warning("Not logged in")
            return False
        
        if self.user_info:
            print(f"\n{Colors.BOLD}Current User:{Colors.RESET}")
            print(f"  Username: {self.user_info.get('username')}")
            print(f"  Email: {self.user_info.get('email')}")
            print(f"  Server: {self.server_url}\n")
            return True
        else:
            print_warning("User info not available")
            return False
    
    def create_folder(self, name: str, parent_id: Optional[int] = None) -> bool:
        """Create a new folder"""
        if not self.token:
            raise AuthenticationError("Not logged in. Please login first.")
        
        try:
            data = {'name': name}
            if parent_id:
                data['parent_folder_id'] = parent_id
            
            response = self._make_request(
                'POST',
                '/folders/create',
                headers=self.get_headers(),
                json=data
            )
            
            if response.status_code == 201:
                result = response.json()
                folder = result.get('folder', {})
                print_success(f"Folder created: {name}")
                print_info(f"  Folder ID: {folder.get('id')}")
                return True
            else:
                error = response.json().get('error', 'Failed to create folder')
                raise FileVaultError(error)
                
        except Exception as e:
            print_error(f"Error creating folder: {e}")
            return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description=f'FileVault Client v{VERSION} - Professional remote file management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Login to server
  filevault login user@example.com mypassword
  
  # Upload files with wildcards
  filevault upload *.pdf                    # Upload all PDFs in current directory
  filevault upload *.jpg *.png              # Upload all images
  filevault upload **/*.py                  # Upload all Python files recursively
  
  # Upload specific files
  filevault upload document.pdf photo.jpg
  
  # Upload to a specific folder
  filevault upload *.txt --folder-id 5
  
  # Upload entire directory
  filevault upload-dir ./my_documents
  filevault upload-dir ./project --recursive
  
  # List files
  filevault list
  filevault list --folder-id 10
  
  # Download files
  filevault download 123
  filevault download 123 --output myfile.pdf
  
  # Create folder
  filevault mkdir "My Folder"
  
  # Show current user
  filevault whoami
  
  # Show version
  filevault --version
        """)
    
    parser.add_argument('--version', action='version', version=f'FileVault Client v{VERSION}')
    parser.add_argument('--server', default=DEFAULT_SERVER, 
                       help='Server URL (default: http://localhost:5000)')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Login command
    login_parser = subparsers.add_parser('login', help='Login to server')
    login_parser.add_argument('email', help='Email address')
    login_parser.add_argument('password', help='Password')
    
    # Upload command - supports wildcards
    upload_parser = subparsers.add_parser('upload', help='Upload file(s) - supports wildcards')
    upload_parser.add_argument('files', nargs='+', help='File patterns (supports *, **, etc.)')
    upload_parser.add_argument('--folder-id', type=int, help='Folder ID to upload to')
    upload_parser.add_argument('--recursive', '-r', action='store_true', 
                              help='Search directories recursively')
    
    # Upload directory command
    upload_dir_parser = subparsers.add_parser('upload-dir', help='Upload entire directory')
    upload_dir_parser.add_argument('directory', help='Path to directory')
    upload_dir_parser.add_argument('--folder-id', type=int, help='Folder ID to upload to')
    upload_dir_parser.add_argument('--recursive', '-r', action='store_true', default=True,
                                   help='Include subdirectories (default: true)')
    
    # List files command
    list_parser = subparsers.add_parser('list', help='List files and folders')
    list_parser.add_argument('--folder-id', type=int, help='Folder ID to list')
    
    # Download file command
    download_parser = subparsers.add_parser('download', help='Download a file')
    download_parser.add_argument('file_id', type=int, help='File ID to download')
    download_parser.add_argument('--output', '-o', help='Output file path')
    
    # Create folder command
    mkdir_parser = subparsers.add_parser('mkdir', help='Create a new folder')
    mkdir_parser.add_argument('name', help='Folder name')
    mkdir_parser.add_argument('--parent-id', type=int, help='Parent folder ID')
    
    # Whoami command
    whoami_parser = subparsers.add_parser('whoami', help='Show current user info')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Create client
    try:
        client = FileVaultClient(args.server)
    except Exception as e:
        print_error(f"Failed to initialize client: {e}")
        return 1
    
    # Execute command
    try:
        if args.command == 'login':
            success = client.login(args.email, args.password)
            return 0 if success else 1
        
        elif args.command == 'upload':
            client.upload_files(args.files, args.folder_id, args.recursive)
            return 0
        
        elif args.command == 'upload-dir':
            client.upload_directory(args.directory, args.folder_id, args.recursive)
            return 0
        
        elif args.command == 'list':
            success = client.list_files(args.folder_id)
            return 0 if success else 1
        
        elif args.command == 'download':
            success = client.download_file(args.file_id, args.output)
            return 0 if success else 1
        
        elif args.command == 'mkdir':
            success = client.create_folder(args.name, args.parent_id)
            return 0 if success else 1
        
        elif args.command == 'whoami':
            success = client.whoami()
            return 0 if success else 1
        
    except AuthenticationError as e:
        print_error(f"Authentication error: {e}")
        print_info("Please login first: filevault login <email> <password>")
        return 1
    except NetworkError as e:
        print_error(f"Network error: {e}")
        print_info(f"Make sure the server is running at {args.server}")
        return 1
    except FileVaultError as e:
        print_error(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        return 130
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
