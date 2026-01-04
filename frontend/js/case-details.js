// Case details page functionality

let caseData = null;
let officers = [];

document.addEventListener('DOMContentLoaded', async function() {
    if (!requireAuth()) {
        return; // Already redirected to login
    }
    
    // Get case ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const caseId = urlParams.get('id');
    
    if (!caseId) {
        document.getElementById('caseDetails').innerHTML = '<p>Case ID not provided</p>';
        return;
    }
    
    // Load officers for update form
    try {
        officers = await officersAPI.getAll();
        const updatedBySelect = document.getElementById('updated_by');
        officers.forEach(officer => {
            const option = document.createElement('option');
            option.value = officer.officer_id;
            option.textContent = officer.name;
            updatedBySelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading officers:', error);
    }
    
    loadCaseDetails(caseId);
    loadCaseUpdates(caseId);
    loadCaseEvidence(caseId);
    
    // Update form handler
    document.getElementById('updateForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        await addUpdate(caseId);
    });
});

async function loadCaseDetails(caseId) {
    try {
        caseData = await casesAPI.getById(caseId);
        renderCaseDetails();
    } catch (error) {
        console.error('Error loading case details:', error);
        document.getElementById('caseDetails').innerHTML = '<p>Error loading case details</p>';
    }
}

function renderCaseDetails() {
    if (!caseData) return;
    
    const statusClass = caseData.status === 'Open' ? 'status-open' : 'status-closed';
    
    document.getElementById('caseDetails').innerHTML = `
        <h3>${caseData.title}</h3>
        <p><strong>Case Number:</strong> ${caseData.case_number}</p>
        <p><strong>Status:</strong> <span class="status-badge ${statusClass}">${caseData.status}</span></p>
        <p><strong>Filed Date:</strong> ${caseData.filed_date || '-'}</p>
        <p><strong>Filed By:</strong> ${caseData.officer_name || '-'}</p>
        <p><strong>Suspect:</strong> ${caseData.suspect_name || 'None'}</p>
        <p><strong>Description:</strong></p>
        <p>${caseData.description || 'No description'}</p>
    `;
    
    document.getElementById('caseId').value = caseData.case_id;
}

async function loadCaseUpdates(caseId) {
    try {
        const updates = await casesAPI.getUpdates(caseId);
        renderUpdates(updates);
    } catch (error) {
        console.error('Error loading updates:', error);
        document.getElementById('caseUpdates').innerHTML = '<p>Error loading updates</p>';
    }
}

function renderUpdates(updates) {
    const container = document.getElementById('caseUpdates');
    
    if (updates.length === 0) {
        container.innerHTML = '<p>No updates yet</p>';
        return;
    }
    
    container.innerHTML = updates.map(update => `
        <div class="update-item">
            <div class="update-meta">
                ${update.officer_name || 'Unknown'} - ${update.update_date || ''}
            </div>
            <div>${update.update_text}</div>
        </div>
    `).join('');
}

async function loadCaseEvidence(caseId) {
    try {
        const evidence = await evidenceAPI.getAll(caseId);
        renderEvidence(evidence);
    } catch (error) {
        console.error('Error loading evidence:', error);
        document.getElementById('caseEvidence').innerHTML = '<p>Error loading evidence</p>';
    }
}

function renderEvidence(evidence) {
    const container = document.getElementById('caseEvidence');
    
    if (evidence.length === 0) {
        container.innerHTML = '<p>No evidence uploaded yet</p>';
        return;
    }
    
    container.innerHTML = evidence.map(ev => `
        <div class="evidence-item">
            <div>
                <strong>${ev.file_name}</strong>
                <p>${ev.description || 'No description'}</p>
                <small>Uploaded: ${ev.upload_date || ''}</small>
            </div>
            <a href="http://localhost:5000/uploads/${ev.file_name}" target="_blank" class="btn btn-primary">Download</a>
        </div>
    `).join('');
}

async function addUpdate(caseId) {
    const data = {
        update_text: document.getElementById('update_text').value,
        updated_by: parseInt(document.getElementById('updated_by').value)
    };
    
    try {
        await casesAPI.addUpdate(caseId, data);
        document.getElementById('updateForm').reset();
        loadCaseUpdates(caseId);
    } catch (error) {
        alert('Error adding update: ' + error.message);
    }
}

