// Cases page functionality

let cases = [];
let officers = [];
let criminals = [];
let editingCaseId = null;

document.addEventListener('DOMContentLoaded', async function() {
    await requireAuth();
    
    // Load officers and criminals for dropdowns
    try {
        officers = await officersAPI.getAll();
        criminals = await criminalsAPI.getAll();
        
        const filedBySelect = document.getElementById('filed_by');
        const suspectSelect = document.getElementById('suspect_id');
        
        officers.forEach(officer => {
            const option = document.createElement('option');
            option.value = officer.officer_id;
            option.textContent = officer.name;
            filedBySelect.appendChild(option);
        });
        
        criminals.forEach(criminal => {
            const option = document.createElement('option');
            option.value = criminal.criminal_id;
            option.textContent = criminal.name;
            suspectSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading data:', error);
    }
    
    loadCases();
    
    // Form handlers
    document.getElementById('addCaseBtn').addEventListener('click', () => {
        showForm();
    });
    
    document.getElementById('cancelBtn').addEventListener('click', () => {
        hideForm();
    });
    
    document.getElementById('caseFormElement').addEventListener('submit', async function(e) {
        e.preventDefault();
        await saveCase();
    });
});

async function loadCases() {
    try {
        cases = await casesAPI.getAll();
        renderCases();
    } catch (error) {
        console.error('Error loading cases:', error);
        document.getElementById('casesTableBody').innerHTML = 
            '<tr><td colspan="7">Error loading cases</td></tr>';
    }
}

function renderCases() {
    const tbody = document.getElementById('casesTableBody');
    
    if (cases.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7">No cases found</td></tr>';
        return;
    }
    
    tbody.innerHTML = cases.map(caseItem => {
        const statusClass = caseItem.status === 'Open' ? 'status-open' : 'status-closed';
        return `
        <tr>
            <td>${caseItem.case_number}</td>
            <td>${caseItem.title}</td>
            <td>${caseItem.filed_date || '-'}</td>
            <td>${caseItem.officer_name || '-'}</td>
            <td>${caseItem.suspect_name || '-'}</td>
            <td><span class="status-badge ${statusClass}">${caseItem.status}</span></td>
            <td>
                <div class="action-buttons">
                    <a href="case-details.html?id=${caseItem.case_id}" class="action-btn action-btn-view">View</a>
                    <button class="action-btn action-btn-edit" onclick="editCase(${caseItem.case_id})">Edit</button>
                    <button class="action-btn action-btn-delete" onclick="deleteCase(${caseItem.case_id})">Delete</button>
                </div>
            </td>
        </tr>
    `;
    }).join('');
}

function showForm() {
    document.getElementById('caseForm').style.display = 'flex';
    document.getElementById('formTitle').textContent = 'Register Case';
    editingCaseId = null;
    document.getElementById('caseFormElement').reset();
    document.getElementById('caseId').value = '';
    document.getElementById('filed_date').valueAsDate = new Date();
}

function hideForm() {
    document.getElementById('caseForm').style.display = 'none';
}

async function editCase(id) {
    const caseItem = cases.find(c => c.case_id === id);
    if (!caseItem) return;
    
    editingCaseId = id;
    document.getElementById('caseId').value = id;
    document.getElementById('case_number').value = caseItem.case_number;
    document.getElementById('title').value = caseItem.title;
    document.getElementById('description').value = caseItem.description || '';
    document.getElementById('filed_date').value = caseItem.filed_date;
    document.getElementById('filed_by').value = caseItem.filed_by;
    document.getElementById('suspect_id').value = caseItem.suspect_id || '';
    document.getElementById('status').value = caseItem.status;
    document.getElementById('formTitle').textContent = 'Edit Case';
    document.getElementById('caseForm').style.display = 'flex';
}

async function saveCase() {
    const data = {
        case_number: document.getElementById('case_number').value,
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        filed_date: document.getElementById('filed_date').value,
        filed_by: parseInt(document.getElementById('filed_by').value),
        suspect_id: document.getElementById('suspect_id').value ? parseInt(document.getElementById('suspect_id').value) : null,
        status: document.getElementById('status').value
    };
    
    try {
        if (editingCaseId) {
            await casesAPI.update(editingCaseId, data);
        } else {
            await casesAPI.create(data);
        }
        hideForm();
        loadCases();
    } catch (error) {
        alert('Error saving case: ' + error.message);
    }
}

async function deleteCase(id) {
    if (!confirm('Are you sure you want to delete this case?')) {
        return;
    }
    
    try {
        await casesAPI.delete(id);
        loadCases();
    } catch (error) {
        alert('Error deleting case: ' + error.message);
    }
}

