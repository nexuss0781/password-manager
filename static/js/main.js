// --- Step 1: PIN Verification ---
function verifyPin() {
    const pinInput = document.getElementById('pin').value;
    // In a real application, you would send this PIN to the server for verification.
    // For this example, we'll assume the server-side Flask app handles the actual PIN verification.
    // This client-side JS is primarily for UI flow.
    
    // For now, we'll just proceed to the next step.
    // The actual PIN verification will happen on the server when the user submits the form.
    document.getElementById('pin-step').classList.remove('active');
    document.getElementById('password-step').classList.add('active');
}

// --- Step 2: Password Verification ---
function verifyPassword() {
    // In a real application, you would send this password to the server for verification.
    // For this example, we'll assume the server-side Flask app handles the actual password verification.
    // This client-side JS is primarily for UI flow.
    
    // For now, we'll just proceed to the next step.
    // The actual password verification will happen on the server when the user submits the form.
    document.getElementById('password-step').classList.remove('active');
    document.getElementById('puzzle-step').classList.add('active');
    initializePuzzle();
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