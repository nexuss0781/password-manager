// Helper function to display errors
function displayError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

// Helper function to clear errors
function clearError(elementId) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = '';
    errorElement.style.display = 'none';
}

// --- Step 1: PIN Verification ---
async function verifyPin() {
    clearError('pin-error');
    const pinInput = document.getElementById('pin').value;

    try {
        const response = await fetch('/verify_login_pin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `pin=${pinInput}`
        });
        const data = await response.json();

        if (data.success) {
            document.getElementById('pin-step').classList.remove('active');
            document.getElementById('password-step').classList.add('active');
        } else {
            displayError('pin-error', data.message || 'Invalid PIN');
        }
    } catch (error) {
        console.error('Error during PIN verification:', error);
        displayError('pin-error', 'An unexpected error occurred.');
    }
}

// --- Step 2: Password Verification ---
async function verifyPassword() {
    clearError('password-error');
    const usernameInput = document.getElementById('username').value;
    const passwordInput = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Indicate JSON content for Flask
            },
            body: JSON.stringify({ username: usernameInput, password: passwordInput })
        });
        const data = await response.json();

        if (data.success) {
            document.getElementById('password-step').classList.remove('active');
            document.getElementById('puzzle-step').classList.add('active');
            initializePuzzle();
        } else {
            displayError('password-error', data.message || 'Invalid credentials');
        }
    } catch (error) {
        console.error('Error during password verification:', error);
        displayError('password-error', 'An unexpected error occurred.');
    }
}

let puzzleClickedCount = 0;
let pieceClickedSet = new Set();
function initializePuzzle() {
    const pieces = document.querySelectorAll('#puzzle-container .piece');
    const puzzleContainer = document.getElementById('puzzle-container');
    pieces.forEach((piece) => {
        piece.addEventListener('click', handlePieceClick);
        piece.addEventListener('dragstart', handleDragAttempt);
    });
    let isMouseDown = false;
    let startPos = null;
    puzzleContainer.addEventListener('mousedown', (e) => {
        isMouseDown = true;
        startPos = { x: e.clientX, y: e.clientY };
    });
    puzzleContainer.addEventListener('mouseup', () => {
        isMouseDown = false;
        startPos = null;
    });
    puzzleContainer.addEventListener('mousemove', (e) => {
        if (isMouseDown && startPos) {
            const dx = Math.abs(e.clientX - startPos.x);
            const dy = Math.abs(e.clientY - startPos.y);
            if (dx + dy > 20) {
                triggerLock();
            }
        }
    });
}
function handlePieceClick(e) {
    const piece = e.currentTarget;
    if (piece.dataset.clicked === 'true') return;
    piece.dataset.clicked = 'true';
    piece.classList.add('clicked');
    pieceClickedSet.add(piece.dataset.index);
    puzzleClickedCount = pieceClickedSet.size;
    if (puzzleClickedCount === 4) revealSubmitButton();
}
function handleDragAttempt() {
    triggerLock();
}
function triggerLock() {
    window.location.href = '/logout';
}
function revealSubmitButton() {
    const submitButton = document.getElementById('hidden-submit');
    const instruction = document.getElementById('puzzle-instruction');
    submitButton.classList.add('show');
    instruction.textContent = 'Button revealed. Click Submit to continue.';
    document.querySelectorAll('#puzzle-container .piece').forEach((p) => {
        p.removeEventListener('click', handlePieceClick);
        p.removeEventListener('dragstart', handleDragAttempt);
    });
}

// --- Final Login Submission ---
function finalLogin() {
    // Instead of an alert, we now redirect to a server route
    // that will create the user's session.
    window.location.href = '/login_success';
}