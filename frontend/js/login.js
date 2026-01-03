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
            const response = await fetch('http://localhost:5000/api/login', {
                method: 'POST',
                credentials: 'include', // Important: include cookies
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Login failed');
            }
            
            // Login successful - set flag and redirect
            // The session cookie should be set by Flask automatically
            localStorage.setItem('just_logged_in', 'true');
            
            // Redirect immediately - dashboard will verify session
            window.location.href = 'dashboard.html';
        } catch (error) {
            console.error('Login error:', error);
            errorMessage.textContent = error.message || 'Login failed. Please check your credentials.';
            errorMessage.style.display = 'block';
        }
    });
});

