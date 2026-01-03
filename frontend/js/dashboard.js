// Dashboard page functionality

document.addEventListener('DOMContentLoaded', async function() {
    await requireAuth();
    
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

