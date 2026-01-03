// Login page functionality

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    
    // Check if already logged in
    checkAuth().then(isAuth => {
        if (isAuth) {
            window.location.href = 'dashboard.html';
        }
    });
    
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        errorMessage.style.display = 'none';
        
        try {
            await authAPI.login(username, password);
            window.location.href = 'dashboard.html';
        } catch (error) {
            errorMessage.textContent = error.message || 'Login failed. Please check your credentials.';
            errorMessage.style.display = 'block';
        }
    });
});

