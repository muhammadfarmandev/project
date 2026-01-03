// Dashboard page functionality

document.addEventListener('DOMContentLoaded', async function() {
    // Check if we just logged in
    const justLoggedIn = localStorage.getItem('just_logged_in');
    
    if (justLoggedIn === 'true') {
        localStorage.removeItem('just_logged_in');
        // Wait for cookie to be fully processed by browser after redirect
        console.log('Just logged in, waiting for session cookie...');
        await new Promise(resolve => setTimeout(resolve, 1000)); // Longer wait
    }
    
    // Check authentication - with multiple retries if needed
    let isAuth = false;
    let retries = justLoggedIn === 'true' ? 3 : 1; // More retries if just logged in
    
    for (let i = 0; i < retries; i++) {
        isAuth = await checkAuth();
        console.log(`Auth check attempt ${i + 1}: ${isAuth ? 'SUCCESS' : 'FAILED'}`);
        
        if (isAuth) {
            break;
        }
        
        if (i < retries - 1) {
            console.log(`Retrying auth check in 500ms...`);
            await new Promise(resolve => setTimeout(resolve, 500));
        }
    }
    
    if (!isAuth) {
        console.error('Authentication failed after all retries. Redirecting to login...');
        window.location.href = 'index.html';
        return;
    }
    
    console.log('Authentication successful! Loading dashboard...');
    
    // Load statistics
    try {
        const officers = await officersAPI.getAll();
        const criminals = await criminalsAPI.getAll();
        const cases = await casesAPI.getAll();
        
        document.getElementById('officerCount').textContent = officers.length;
        document.getElementById('criminalCount').textContent = criminals.length;
        document.getElementById('caseCount').textContent = cases.length;
        
        const openCases = cases.filter(c => c.status === 'Open').length;
        document.getElementById('openCaseCount').textContent = openCases;
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
});

