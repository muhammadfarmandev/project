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
            
            // Wait a bit longer to ensure cookie is processed
            await new Promise(resolve => setTimeout(resolve, 200));
            
            // Verify session before redirect - use the same origin
            const authCheck = await fetch('http://localhost:5000/api/check-auth', {
                method: 'GET',
                credentials: 'include'
            });
            
            const authData = await authCheck.json();
            console.log('Auth check result:', authData);
            
            if (authData.authenticated) {
                // Set flag to skip auth check on next page load
                localStorage.setItem('just_logged_in', 'true');
                // Redirect after confirming session is set
                window.location.href = 'dashboard.html';
            } else {
                throw new Error('Session not established. Please try again.');
            }
        } catch (error) {
            console.error('Login error:', error);
            errorMessage.textContent = error.message || 'Login failed. Please check your credentials.';
            errorMessage.style.display = 'block';
        }
    });
});

