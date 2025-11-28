// FileVault - File Manager JavaScript Application

class FileManagerAPI {
    constructor() {
        this.baseURL = '/api';
        this.currentFolderId = null;
        this.authToken = localStorage.getItem('access_token');
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (this.authToken) {
            headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        
        return headers;
    }

    async uploadFile(file, folderId = null) {
        const formData = new FormData();
        formData.append('file', file);
        
        if (folderId) {
            formData.append('folder_id', folderId);
        }

        const response = await fetch(`${this.baseURL}/files/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.authToken}`
            },
            body: formData
        });

        return await response.json();
    }

    async listFiles(folderId = null) {
        const url = folderId 
            ? `${this.baseURL}/files/list?folder_id=${folderId}`
            : `${this.baseURL}/files/list`;

        const response = await fetch(url, {
            headers: this.getHeaders()
        });

        return await response.json();
    }

    async downloadFile(fileId) {
        const response = await fetch(`${this.baseURL}/files/download/${fileId}`, {
            headers: {
                'Authorization': `Bearer ${this.authToken}`
            }
        });

        if (response.ok) {
            const blob = await response.blob();
            const contentDisposition = response.headers.get('Content-Disposition');
            const filename = contentDisposition
                ? contentDisposition.split('filename=')[1].replace(/"/g, '')
                : 'download';

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } else {
            throw new Error('Download failed');
        }
    }

    async createFolder(name, parentFolderId = null) {
        const data = {
            name: name,
            parent_folder_id: parentFolderId
        };

        const response = await fetch(`${this.baseURL}/folders/create`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });

        return await response.json();
    }

    async deleteFile(fileId) {
        const response = await fetch(`${this.baseURL}/files/${fileId}`, {
            method: 'DELETE',
            headers: this.getHeaders()
        });

        return await response.json();
    }

    async deleteFolder(folderId) {
        const response = await fetch(`${this.baseURL}/folders/${folderId}`, {
            method: 'DELETE',
            headers: this.getHeaders()
        });

        return await response.json();
    }

    async renameFile(fileId, newName) {
        const response = await fetch(`${this.baseURL}/files/${fileId}/rename`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify({ new_name: newName })
        });

        return await response.json();
    }

    async renameFolder(folderId, newName) {
        const response = await fetch(`${this.baseURL}/folders/${folderId}/rename`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify({ new_name: newName })
        });

        return await response.json();
    }

    async moveFile(fileId, targetFolderId) {
        const response = await fetch(`${this.baseURL}/files/${fileId}/move`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify({ folder_id: targetFolderId })
        });

        return await response.json();
    }
}

// Global API instance
const api = new FileManagerAPI();

// File type to icon mapping
function getFileIcon(mimeType) {
    if (!mimeType) return 'bi-file-earmark';
    
    if (mimeType.startsWith('image/')) return 'bi-file-earmark-image';
    if (mimeType.startsWith('video/')) return 'bi-file-earmark-play';
    if (mimeType.startsWith('audio/')) return 'bi-file-earmark-music';
    if (mimeType.includes('pdf')) return 'bi-file-earmark-pdf';
    if (mimeType.includes('word') || mimeType.includes('document')) return 'bi-file-earmark-word';
    if (mimeType.includes('excel') || mimeType.includes('spreadsheet')) return 'bi-file-earmark-excel';
    if (mimeType.includes('powerpoint') || mimeType.includes('presentation')) return 'bi-file-earmark-ppt';
    if (mimeType.includes('zip') || mimeType.includes('rar') || mimeType.includes('compressed')) return 'bi-file-earmark-zip';
    if (mimeType.includes('text') || mimeType.includes('json') || mimeType.includes('xml')) return 'bi-file-earmark-text';
    
    return 'bi-file-earmark';
}

// Format file size
function formatFileSize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let size = bytes;
    let unitIndex = 0;
    
    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }
    
    return `${size.toFixed(2)} ${units[unitIndex]}`;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Load and display files
async function loadFiles(folderId = null) {
    try {
        const data = await api.listFiles(folderId);
        api.currentFolderId = folderId;
        
        const fileGrid = document.getElementById('fileGrid');
        const emptyState = document.getElementById('emptyState');
        
        fileGrid.innerHTML = '';
        
        if (data.files.length === 0 && data.folders.length === 0) {
            fileGrid.style.display = 'none';
            emptyState.style.display = 'block';
            return;
        }
        
        fileGrid.style.display = 'grid';
        emptyState.style.display = 'none';
        
        // Render folders first
        data.folders.forEach(folder => {
            const folderElement = createFolderElement(folder);
            fileGrid.appendChild(folderElement);
        });
        
        // Render files
        data.files.forEach(file => {
            const fileElement = createFileElement(file);
            fileGrid.appendChild(fileElement);
        });
        
    } catch (error) {
        console.error('Error loading files:', error);
        showToast('Failed to load files', 'danger');
    }
}

// Create folder element
function createFolderElement(folder) {
    const div = document.createElement('div');
    div.className = 'folder-item';
    div.onclick = () => navigateToFolder(folder.id, folder.name);
    
    div.innerHTML = `
        <div class="action-buttons">
            <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); showRenameModal(${folder.id}, 'folder', '${folder.name}')">
                <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="event.stopPropagation(); deleteFolder(${folder.id})">
                <i class="bi bi-trash"></i>
            </button>
        </div>
        <div class="folder-icon">
            <i class="bi bi-folder-fill"></i>
        </div>
        <div class="file-name">${folder.name}</div>
        <div class="file-meta">Folder</div>
    `;
    
    return div;
}

// Create file element
function createFileElement(file) {
    const div = document.createElement('div');
    div.className = 'file-item';
    
    const icon = getFileIcon(file.mime_type);
    const iconClass = file.mime_type?.startsWith('image/') ? 'image' : 
                     file.mime_type?.startsWith('video/') ? 'video' :
                     file.mime_type?.startsWith('audio/') ? 'audio' :
                     file.mime_type?.includes('pdf') ? 'pdf' :
                     file.mime_type?.includes('document') ? 'document' : '';
    
    div.innerHTML = `
        <div class="action-buttons">
            <button class="btn btn-sm btn-outline-success" onclick="downloadFile(${file.id})">
                <i class="bi bi-download"></i>
            </button>
            <button class="btn btn-sm btn-outline-primary" onclick="showRenameModal(${file.id}, 'file', '${file.name}')">
                <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="deleteFile(${file.id})">
                <i class="bi bi-trash"></i>
            </button>
        </div>
        <div class="file-icon ${iconClass}">
            <i class="bi ${icon}"></i>
        </div>
        <div class="file-name">${file.name}</div>
        <div class="file-meta">${formatFileSize(file.size)}</div>
    `;
    
    return div;
}

// Navigate to folder
async function navigateToFolder(folderId, folderName = 'Home') {
    await loadFiles(folderId);
    updateBreadcrumb(folderId, folderName);
}

// Update breadcrumb
let breadcrumbPath = [];

function updateBreadcrumb(folderId, folderName) {
    if (folderId === null) {
        breadcrumbPath = [];
    } else {
        const existingIndex = breadcrumbPath.findIndex(item => item.id === folderId);
        
        if (existingIndex !== -1) {
            breadcrumbPath = breadcrumbPath.slice(0, existingIndex + 1);
        } else {
            breadcrumbPath.push({ id: folderId, name: folderName });
        }
    }
    
    const breadcrumb = document.getElementById('breadcrumb');
    breadcrumb.innerHTML = '<li class="breadcrumb-item"><a href="#" onclick="navigateToFolder(null)">Home</a></li>';
    
    breadcrumbPath.forEach((item, index) => {
        const li = document.createElement('li');
        li.className = 'breadcrumb-item';
        
        if (index === breadcrumbPath.length - 1) {
            li.className += ' active';
            li.textContent = item.name;
        } else {
            const a = document.createElement('a');
            a.href = '#';
            a.textContent = item.name;
            a.onclick = () => navigateToFolder(item.id, item.name);
            li.appendChild(a);
        }
        
        breadcrumb.appendChild(li);
    });
}

// File upload handling
function handleFileSelect(event) {
    const files = event.target.files;
    
    if (files.length > 0) {
        uploadFiles(files);
    }
}

async function uploadFiles(files) {
    const uploadZone = document.getElementById('uploadZone');
    const progressContainer = document.createElement('div');
    progressContainer.className = 'upload-progress';
    progressContainer.innerHTML = `
        <div class="d-flex justify-content-between mb-2">
            <span>Uploading ${files.length} file(s)...</span>
            <span id="uploadStatus">0%</span>
        </div>
        <div class="progress">
            <div class="progress-bar" id="uploadProgressBar" style="width: 0%"></div>
        </div>
    `;
    uploadZone.appendChild(progressContainer);
    
    let completed = 0;
    
    for (const file of files) {
        try {
            await api.uploadFile(file, api.currentFolderId);
            completed++;
            
            const percentage = Math.round((completed / files.length) * 100);
            document.getElementById('uploadProgressBar').style.width = `${percentage}%`;
            document.getElementById('uploadStatus').textContent = `${percentage}%`;
            
        } catch (error) {
            console.error('Upload error:', error);
            showToast(`Failed to upload ${file.name}`, 'danger');
        }
    }
    
    setTimeout(() => {
        progressContainer.remove();
    }, 2000);
    
    showToast(`Successfully uploaded ${completed} file(s)`, 'success');
    await loadFiles(api.currentFolderId);
}

// Drag and drop handling
const uploadZone = document.getElementById('uploadZone');

if (uploadZone) {
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            uploadFiles(files);
        }
    });
    
    uploadZone.addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });
}

// Create folder
function showCreateFolderModal() {
    const modal = new bootstrap.Modal(document.getElementById('createFolderModal'));
    document.getElementById('folderNameInput').value = '';
    modal.show();
}

async function createFolder() {
    const folderName = document.getElementById('folderNameInput').value.trim();
    
    if (!folderName) {
        showToast('Please enter a folder name', 'danger');
        return;
    }
    
    try {
        const result = await api.createFolder(folderName, api.currentFolderId);
        
        if (result.folder) {
            showToast('Folder created successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('createFolderModal')).hide();
            await loadFiles(api.currentFolderId);
        } else {
            showToast(result.error || 'Failed to create folder', 'danger');
        }
    } catch (error) {
        console.error('Create folder error:', error);
        showToast('An error occurred', 'danger');
    }
}

// Delete file
async function deleteFile(fileId) {
    if (!confirm('Are you sure you want to delete this file?')) {
        return;
    }
    
    try {
        await api.deleteFile(fileId);
        showToast('File deleted successfully', 'success');
        await loadFiles(api.currentFolderId);
    } catch (error) {
        console.error('Delete error:', error);
        showToast('Failed to delete file', 'danger');
    }
}

// Delete folder
async function deleteFolder(folderId) {
    if (!confirm('Are you sure you want to delete this folder and all its contents?')) {
        return;
    }
    
    try {
        await api.deleteFolder(folderId);
        showToast('Folder deleted successfully', 'success');
        await loadFiles(api.currentFolderId);
    } catch (error) {
        console.error('Delete error:', error);
        showToast('Failed to delete folder', 'danger');
    }
}

// Download file
async function downloadFile(fileId) {
    try {
        await api.downloadFile(fileId);
        showToast('Download started', 'success');
    } catch (error) {
        console.error('Download error:', error);
        showToast('Failed to download file', 'danger');
    }
}

// Rename modal
function showRenameModal(itemId, itemType, currentName) {
    const modal = new bootstrap.Modal(document.getElementById('renameModal'));
    document.getElementById('renameInput').value = currentName;
    document.getElementById('renameItemId').value = itemId;
    document.getElementById('renameItemType').value = itemType;
    modal.show();
}

async function performRename() {
    const newName = document.getElementById('renameInput').value.trim();
    const itemId = parseInt(document.getElementById('renameItemId').value);
    const itemType = document.getElementById('renameItemType').value;
    
    if (!newName) {
        showToast('Please enter a name', 'danger');
        return;
    }
    
    try {
        let result;
        
        if (itemType === 'file') {
            result = await api.renameFile(itemId, newName);
        } else {
            result = await api.renameFolder(itemId, newName);
        }
        
        if (result.file || result.folder) {
            showToast('Renamed successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('renameModal')).hide();
            await loadFiles(api.currentFolderId);
        } else {
            showToast(result.error || 'Failed to rename', 'danger');
        }
    } catch (error) {
        console.error('Rename error:', error);
        showToast('An error occurred', 'danger');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/dashboard') {
        loadFiles();
    }
});
