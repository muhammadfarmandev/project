// API helper functions for making requests to backend

const API_BASE = 'http://localhost:5000/api';

// Helper function to make API calls
async function apiCall(endpoint, method = 'GET', body = null, isFormData = false) {
    const options = {
        method: method,
        credentials: 'include',
        headers: {}
    };

    // Add admin_id header for authentication (localStorage-based)
    const adminId = localStorage.getItem('admin_id');
    if (adminId) {
        options.headers['X-Admin-ID'] = adminId;
    }

    if (body) {
        if (isFormData) {
            options.body = body;
        } else {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(body);
        }
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Auth API
const authAPI = {
    login: (username, password) => apiCall('/login', 'POST', { username, password }),
    logout: () => apiCall('/logout', 'POST'),
    checkAuth: () => apiCall('/check-auth', 'GET')
};

// Officers API
const officersAPI = {
    getAll: () => apiCall('/officers', 'GET'),
    getById: (id) => apiCall(`/officers/${id}`, 'GET'),
    create: (data) => apiCall('/officers', 'POST', data),
    update: (id, data) => apiCall(`/officers/${id}`, 'PUT', data),
    delete: (id) => apiCall(`/officers/${id}`, 'DELETE')
};

// Criminals API
const criminalsAPI = {
    getAll: () => apiCall('/criminals', 'GET'),
    getById: (id) => apiCall(`/criminals/${id}`, 'GET'),
    create: (data) => apiCall('/criminals', 'POST', data),
    update: (id, data) => apiCall(`/criminals/${id}`, 'PUT', data),
    delete: (id) => apiCall(`/criminals/${id}`, 'DELETE')
};

// Cases API
const casesAPI = {
    getAll: () => apiCall('/cases', 'GET'),
    getById: (id) => apiCall(`/cases/${id}`, 'GET'),
    create: (data) => apiCall('/cases', 'POST', data),
    update: (id, data) => apiCall(`/cases/${id}`, 'PUT', data),
    delete: (id) => apiCall(`/cases/${id}`, 'DELETE'),
    getUpdates: (caseId) => apiCall(`/cases/${caseId}/updates`, 'GET'),
    addUpdate: (caseId, data) => apiCall(`/cases/${caseId}/updates`, 'POST', data)
};

// Evidence API
const evidenceAPI = {
    getAll: (caseId = null) => {
        const endpoint = caseId ? `/evidence?case_id=${caseId}` : '/evidence';
        return apiCall(endpoint, 'GET');
    },
    create: (formData) => apiCall('/evidence', 'POST', formData, true)
};

// Duties API
const dutiesAPI = {
    getAll: () => apiCall('/duties', 'GET'),
    create: (data) => apiCall('/duties', 'POST', data),
    delete: (id) => apiCall(`/duties/${id}`, 'DELETE')
};

// Units API
const unitsAPI = {
    getAll: () => apiCall('/units', 'GET')
};

// Search API
const searchAPI = {
    search: (query, type = 'all') => apiCall(`/search?q=${encodeURIComponent(query)}&type=${type}`, 'GET')
};

// Audit API
const auditAPI = {
    getLogs: (limit = 100) => apiCall(`/audit?limit=${limit}`, 'GET')
};

