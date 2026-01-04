// Criminals page functionality

let criminals = [];
let editingCriminalId = null;

document.addEventListener('DOMContentLoaded', async function() {
    if (!requireAuth()) {
        return; // Already redirected to login
    }
    
    loadCriminals();
    
    // Form handlers
    document.getElementById('addCriminalBtn').addEventListener('click', () => {
        showForm();
    });
    
    document.getElementById('cancelBtn').addEventListener('click', () => {
        hideForm();
    });
    
    document.getElementById('criminalFormElement').addEventListener('submit', async function(e) {
        e.preventDefault();
        await saveCriminal();
    });
});

async function loadCriminals() {
    try {
        criminals = await criminalsAPI.getAll();
        renderCriminals();
    } catch (error) {
        console.error('Error loading criminals:', error);
        document.getElementById('criminalsTableBody').innerHTML = 
            '<tr><td colspan="6">Error loading criminals</td></tr>';
    }
}

function renderCriminals() {
    const tbody = document.getElementById('criminalsTableBody');
    
    if (criminals.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No criminals found</td></tr>';
        return;
    }
    
    tbody.innerHTML = criminals.map(criminal => `
        <tr>
            <td>${criminal.criminal_id}</td>
            <td>${criminal.name}</td>
            <td>${criminal.cnic}</td>
            <td>${criminal.address || '-'}</td>
            <td>${criminal.notes ? (criminal.notes.length > 50 ? criminal.notes.substring(0, 50) + '...' : criminal.notes) : '-'}</td>
            <td>
                <div class="action-buttons">
                    <button class="action-btn action-btn-edit" onclick="editCriminal(${criminal.criminal_id})">Edit</button>
                    <button class="action-btn action-btn-delete" onclick="deleteCriminal(${criminal.criminal_id})">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

function showForm() {
    document.getElementById('criminalForm').style.display = 'flex';
    document.getElementById('formTitle').textContent = 'Add Criminal';
    editingCriminalId = null;
    document.getElementById('criminalFormElement').reset();
    document.getElementById('criminalId').value = '';
}

function hideForm() {
    document.getElementById('criminalForm').style.display = 'none';
}

async function editCriminal(id) {
    const criminal = criminals.find(c => c.criminal_id === id);
    if (!criminal) return;
    
    editingCriminalId = id;
    document.getElementById('criminalId').value = id;
    document.getElementById('cname').value = criminal.name;
    document.getElementById('caddress').value = criminal.address || '';
    document.getElementById('ccnic').value = criminal.cnic;
    document.getElementById('cnotes').value = criminal.notes || '';
    document.getElementById('formTitle').textContent = 'Edit Criminal';
    document.getElementById('criminalForm').style.display = 'flex';
}

async function saveCriminal() {
    const data = {
        name: document.getElementById('cname').value,
        address: document.getElementById('caddress').value,
        cnic: document.getElementById('ccnic').value,
        notes: document.getElementById('cnotes').value
    };
    
    try {
        if (editingCriminalId) {
            await criminalsAPI.update(editingCriminalId, data);
        } else {
            await criminalsAPI.create(data);
        }
        hideForm();
        loadCriminals();
    } catch (error) {
        alert('Error saving criminal: ' + error.message);
    }
}

async function deleteCriminal(id) {
    if (!confirm('Are you sure you want to delete this criminal?')) {
        return;
    }
    
    try {
        await criminalsAPI.delete(id);
        loadCriminals();
    } catch (error) {
        alert('Error deleting criminal: ' + error.message);
    }
}

