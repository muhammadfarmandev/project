// Simple authentication using localStorage

// Check if user is authenticated (using localStorage)
function checkAuth() {
    const adminId = localStorage.getItem('admin_id');
    return adminId !== null && adminId !== '';
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!checkAuth()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}
    
// Logout function - clears both localStorage and server session
async function logout() {
    // Clear server session
    try {
        await fetch('http://localhost:5000/api/logout', {
            method: 'POST',
            credentials: 'include'
        });
    } catch (error) {
        console.error('Logout error:', error);
    }

    // Clear localStorage
    localStorage.removeItem('admin_id');
    localStorage.removeItem('username');
    window.location.href = 'index.html';
}

// Setup logout button if it exists
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});

