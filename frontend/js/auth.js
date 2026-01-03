// Authentication helper functions

// Check if user is authenticated
async function checkAuth() {
    try {
        const response = await fetch('http://localhost:5000/api/check-auth', {
            method: 'GET',
            credentials: 'include', // Important: include cookies
            cache: 'no-store', // Don't cache this request
            headers: {
                'Cache-Control': 'no-cache'
            }
        });
        
        if (!response.ok) {
            console.error('Auth check failed:', response.status);
            return false;
        }
        
        const data = await response.json();
        console.log('checkAuth result:', data);
        
        // Also log cookies being sent (for debugging)
        console.log('Cookies available:', document.cookie || 'No cookies found');
        
        return data.authenticated || false;
    } catch (error) {
        console.error('Error checking auth:', error);
        return false;
    }
}

// Redirect to login if not authenticated
async function requireAuth() {
    const isAuth = await checkAuth();
    if (!isAuth) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// Logout function
async function logout() {
    try {
        await authAPI.logout();
        window.location.href = 'index.html';
    } catch (error) {
        console.error('Logout error:', error);
        // Still redirect even if logout fails
        window.location.href = 'index.html';
    }
}

// Setup logout button if it exists
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    
    // Don't auto-check auth here - let each page handle it
    // This prevents duplicate checks and timing issues
});

