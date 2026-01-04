// Simple authentication using localStorage

// Check if user is authenticated (using localStorage)
function checkAuth() {
    const authToken = localStorage.getItem('auth_token');
    return authToken === 'authenticated';
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!checkAuth()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// Logout function
function logout() {
    localStorage.removeItem('auth_token');
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

