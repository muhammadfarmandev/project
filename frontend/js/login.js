// Login page functionality

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    
    // Check if already logged in
    if (checkAuth()) {
        window.location.href = 'dashboard.html';
        return;
    }
    
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        errorMessage.style.display = 'none';
        
        try {
            const response = await fetch('http://localhost:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Login failed');
            }
            
            const data = await response.json();
            
            // Login successful - store in localStorage
            localStorage.setItem('auth_token', 'authenticated');
            localStorage.setItem('username', data.username || username);
            
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        } catch (error) {
            console.error('Login error:', error);
            errorMessage.textContent = error.message || 'Login failed. Please check your credentials.';
            errorMessage.style.display = 'block';
        }
    });
});

