// Search page functionality

document.addEventListener('DOMContentLoaded', async function() {
    if (!requireAuth()) {
        return; // Already redirected to login
    }
    
    document.getElementById('searchForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        await performSearch();
    });
});

async function performSearch() {
    const query = document.getElementById('searchQuery').value;
    const searchType = document.querySelector('input[name="searchType"]:checked').value;
    
    if (!query.trim()) {
        alert('Please enter a search query');
        return;
    }
    
    try {
        const results = await searchAPI.search(query, searchType);
        renderResults(results);
    } catch (error) {
        console.error('Error searching:', error);
        document.getElementById('searchResults').innerHTML = '<p>Error performing search</p>';
    }
}

function renderResults(results) {
    const container = document.getElementById('searchResults');
    
    let html = '';
    
    if (results.cases && results.cases.length > 0) {
        html += '<div class="result-section"><h3>Cases</h3>';
        html += '<div class="table-container"><table class="data-table"><thead><tr>';
        html += '<th>Case #</th><th>Title</th><th>Officer</th><th>Status</th><th>Actions</th>';
        html += '</tr></thead><tbody>';
        
        results.cases.forEach(caseItem => {
            const statusClass = caseItem.status === 'Open' ? 'status-open' : 'status-closed';
            html += `
                <tr>
                    <td>${caseItem.case_number}</td>
                    <td>${caseItem.title}</td>
                    <td>${caseItem.officer_name || '-'}</td>
                    <td><span class="status-badge ${statusClass}">${caseItem.status}</span></td>
                    <td><a href="case-details.html?id=${caseItem.case_id}" class="action-btn action-btn-view">View</a></td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div></div>';
    }
    
    if (results.criminals && results.criminals.length > 0) {
        html += '<div class="result-section"><h3>Criminals</h3>';
        html += '<div class="table-container"><table class="data-table"><thead><tr>';
        html += '<th>ID</th><th>Name</th><th>CNIC</th><th>Address</th>';
        html += '</tr></thead><tbody>';
        
        results.criminals.forEach(criminal => {
            html += `
                <tr>
                    <td>${criminal.criminal_id}</td>
                    <td>${criminal.name}</td>
                    <td>${criminal.cnic}</td>
                    <td>${criminal.address || '-'}</td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div></div>';
    }
    
    if (!html) {
        html = '<p>No results found</p>';
    }
    
    container.innerHTML = html;
}

