// Dashboard page functionality

document.addEventListener('DOMContentLoaded', async function() {
    // If we just logged in, wait longer for cookie to be processed
    const justLoggedIn = localStorage.getItem('just_logged_in');
    let wasJustLoggedIn = false;
    
    if (justLoggedIn === 'true') {
        wasJustLoggedIn = true;
        localStorage.removeItem('just_logged_in');
        // Wait longer for cookie to be fully processed by browser
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // Check authentication first
    let isAuth = await requireAuth();
    
    // If auth failed but we just logged in, try once more after a delay
    if (!isAuth && wasJustLoggedIn) {
        console.log('Auth failed after login, retrying...');
        await new Promise(resolve => setTimeout(resolve, 300));
        isAuth = await requireAuth();
    }
    
    if (!isAuth) {
        return; // requireAuth already redirected, just exit
    }
    
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

