// Dashboard page functionality

document.addEventListener('DOMContentLoaded', async function() {
    // If we just logged in, skip immediate auth check (give cookie time to set)
    const justLoggedIn = localStorage.getItem('just_logged_in');
    if (justLoggedIn === 'true') {
        localStorage.removeItem('just_logged_in');
        // Wait a bit for cookie to be fully processed
        await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    // Check authentication first
    const isAuth = await requireAuth();
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

