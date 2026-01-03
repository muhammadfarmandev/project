// Officers page functionality

let officers = [];
let units = [];
let editingOfficerId = null;

document.addEventListener('DOMContentLoaded', async function() {
    await requireAuth();
    
    // Load units for dropdown
    try {
        units = await unitsAPI.getAll();
        const unitSelect = document.getElementById('unit_id');
        units.forEach(unit => {
            const option = document.createElement('option');
            option.value = unit.unit_id;
            option.textContent = unit.unit_name;
            unitSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading units:', error);
    }
    
    // Load officers
    loadOfficers();
    
    // Form handlers
    document.getElementById('addOfficerBtn').addEventListener('click', () => {
        showForm();
    });
    
    document.getElementById('cancelBtn').addEventListener('click', () => {
        hideForm();
    });
    
    document.getElementById('officerFormElement').addEventListener('submit', async function(e) {
        e.preventDefault();
        await saveOfficer();
    });
});

async function loadOfficers() {
    try {
        officers = await officersAPI.getAll();
        renderOfficers();
    } catch (error) {
        console.error('Error loading officers:', error);
        document.getElementById('officersTableBody').innerHTML = 
            '<tr><td colspan="7">Error loading officers</td></tr>';
    }
}

function renderOfficers() {
    const tbody = document.getElementById('officersTableBody');
    
    if (officers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7">No officers found</td></tr>';
        return;
    }
    
    tbody.innerHTML = officers.map(officer => `
        <tr>
            <td>${officer.officer_id}</td>
            <td>${officer.name}</td>
            <td>${officer.badge_no}</td>
            <td>${officer.rank || '-'}</td>
            <td>${officer.contact || '-'}</td>
            <td>${officer.unit_name || '-'}</td>
            <td>
                <div class="action-buttons">
                    <button class="action-btn action-btn-edit" onclick="editOfficer(${officer.officer_id})">Edit</button>
                    <button class="action-btn action-btn-delete" onclick="deleteOfficer(${officer.officer_id})">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

function showForm() {
    document.getElementById('officerForm').style.display = 'flex';
    document.getElementById('formTitle').textContent = 'Add Officer';
    editingOfficerId = null;
    document.getElementById('officerFormElement').reset();
    document.getElementById('officerId').value = '';
}

function hideForm() {
    document.getElementById('officerForm').style.display = 'none';
}

async function editOfficer(id) {
    const officer = officers.find(o => o.officer_id === id);
    if (!officer) return;
    
    editingOfficerId = id;
    document.getElementById('officerId').value = id;
    document.getElementById('name').value = officer.name;
    document.getElementById('address').value = officer.address || '';
    document.getElementById('badge_no').value = officer.badge_no;
    document.getElementById('rank').value = officer.rank || '';
    document.getElementById('contact').value = officer.contact || '';
    document.getElementById('unit_id').value = officer.unit_id || '';
    document.getElementById('formTitle').textContent = 'Edit Officer';
    document.getElementById('officerForm').style.display = 'flex';
}

async function saveOfficer() {
    const data = {
        name: document.getElementById('name').value,
        address: document.getElementById('address').value,
        badge_no: document.getElementById('badge_no').value,
        rank: document.getElementById('rank').value,
        contact: document.getElementById('contact').value,
        unit_id: document.getElementById('unit_id').value || null
    };
    
    try {
        if (editingOfficerId) {
            await officersAPI.update(editingOfficerId, data);
        } else {
            await officersAPI.create(data);
        }
        hideForm();
        loadOfficers();
    } catch (error) {
        alert('Error saving officer: ' + error.message);
    }
}

async function deleteOfficer(id) {
    if (!confirm('Are you sure you want to delete this officer?')) {
        return;
    }
    
    try {
        await officersAPI.delete(id);
        loadOfficers();
    } catch (error) {
        alert('Error deleting officer: ' + error.message);
    }
}

