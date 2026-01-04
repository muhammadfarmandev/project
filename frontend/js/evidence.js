// Evidence page functionality

let evidence = [];
let cases = [];

document.addEventListener('DOMContentLoaded', async function() {
    if (!requireAuth()) {
        return; // Already redirected to login
    }
    
    // Load cases for dropdown
    try {
        cases = await casesAPI.getAll();
        const caseSelect = document.getElementById('evidence_case_id');
        cases.forEach(caseItem => {
            const option = document.createElement('option');
            option.value = caseItem.case_id;
            option.textContent = `${caseItem.case_number} - ${caseItem.title}`;
            caseSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading cases:', error);
    }
    
    loadEvidence();
    
    // Form handlers
    document.getElementById('addEvidenceBtn').addEventListener('click', () => {
        document.getElementById('evidenceForm').style.display = 'flex';
    });
    
    document.getElementById('cancelBtn').addEventListener('click', () => {
        document.getElementById('evidenceForm').style.display = 'none';
        document.getElementById('evidenceFormElement').reset();
    });
    
    document.getElementById('evidenceFormElement').addEventListener('submit', async function(e) {
        e.preventDefault();
        await uploadEvidence();
    });
});

async function loadEvidence() {
    try {
        evidence = await evidenceAPI.getAll();
        renderEvidence();
    } catch (error) {
        console.error('Error loading evidence:', error);
        document.getElementById('evidenceTableBody').innerHTML = 
            '<tr><td colspan="6">Error loading evidence</td></tr>';
    }
}

function renderEvidence() {
    const tbody = document.getElementById('evidenceTableBody');
    
    if (evidence.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No evidence found</td></tr>';
        return;
    }
    
    tbody.innerHTML = evidence.map(ev => `
        <tr>
            <td>${ev.evidence_id}</td>
            <td>${ev.case_number || '-'}</td>
            <td>${ev.file_name}</td>
            <td>${ev.description || '-'}</td>
            <td>${ev.upload_date || '-'}</td>
            <td>
                <a href="http://localhost:5000/uploads/${ev.file_name}" target="_blank" class="action-btn action-btn-view">Download</a>
            </td>
        </tr>
    `).join('');
}

async function uploadEvidence() {
    const formData = new FormData();
    const fileInput = document.getElementById('evidence_file');
    const caseId = document.getElementById('evidence_case_id').value;
    const description = document.getElementById('evidence_description').value;
    
    if (!fileInput.files[0]) {
        alert('Please select a file');
        return;
    }
    
    formData.append('file', fileInput.files[0]);
    formData.append('case_id', caseId);
    formData.append('description', description);
    
    try {
        await evidenceAPI.create(formData);
        document.getElementById('evidenceForm').style.display = 'none';
        document.getElementById('evidenceFormElement').reset();
        loadEvidence();
    } catch (error) {
        alert('Error uploading evidence: ' + error.message);
    }
}

