// Duties page functionality

let duties = [];
let officers = [];

document.addEventListener('DOMContentLoaded', async function() {
    if (!requireAuth()) {
        return; // Already redirected to login
    }
    
    // Load officers for dropdown
    try {
        officers = await officersAPI.getAll();
        const officerSelect = document.getElementById('duty_officer_id');
        officers.forEach(officer => {
            const option = document.createElement('option');
            option.value = officer.officer_id;
            option.textContent = officer.name;
            officerSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading officers:', error);
    }
    
    loadDuties();
    
    // Form handlers
    document.getElementById('addDutyBtn').addEventListener('click', () => {
        document.getElementById('dutyForm').style.display = 'flex';
    });
    
    document.getElementById('cancelBtn').addEventListener('click', () => {
        document.getElementById('dutyForm').style.display = 'none';
        document.getElementById('dutyFormElement').reset();
    });
    
    document.getElementById('dutyFormElement').addEventListener('submit', async function(e) {
        e.preventDefault();
        await saveDuty();
    });
});

async function loadDuties() {
    try {
        duties = await dutiesAPI.getAll();
        renderDuties();
    } catch (error) {
        console.error('Error loading duties:', error);
        document.getElementById('dutiesTableBody').innerHTML = 
            '<tr><td colspan="6">Error loading duties</td></tr>';
    }
}

function renderDuties() {
    const tbody = document.getElementById('dutiesTableBody');
    
    if (duties.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No duties assigned</td></tr>';
        return;
    }
    
    tbody.innerHTML = duties.map(duty => `
        <tr>
            <td>${duty.duty_id}</td>
            <td>${duty.officer_name || '-'}</td>
            <td>${duty.duty_date || '-'}</td>
            <td>${duty.duty_time || '-'}</td>
            <td>${duty.location}</td>
            <td>
                <button class="action-btn action-btn-delete" onclick="deleteDuty(${duty.duty_id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

async function saveDuty() {
    const data = {
        officer_id: parseInt(document.getElementById('duty_officer_id').value),
        duty_date: document.getElementById('duty_date').value,
        duty_time: document.getElementById('duty_time').value,
        location: document.getElementById('duty_location').value
    };
    
    try {
        await dutiesAPI.create(data);
        document.getElementById('dutyForm').style.display = 'none';
        document.getElementById('dutyFormElement').reset();
        loadDuties();
    } catch (error) {
        alert('Error assigning duty: ' + error.message);
    }
}

async function deleteDuty(id) {
    if (!confirm('Are you sure you want to delete this duty assignment?')) {
        return;
    }
    
    try {
        await dutiesAPI.delete(id);
        loadDuties();
    } catch (error) {
        alert('Error deleting duty: ' + error.message);
    }
}

