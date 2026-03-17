// REPLACE THIS with your API Gateway Invoke URL
const API_URL = 'https://atoc7ryejb.execute-api.us-east-1.amazonaws.com/prod';

let servers = [];

async function fetchServers() {
    try {
        const response = await fetch(`${API_URL}/servers`);
        const data = await response.json();
        servers = data.servers || [];
        renderTable();
        updateStats();
    } catch (error) {
        console.error('Error fetching servers:', error);
    }
}

function renderTable() {
    const tbody = document.getElementById('server-table');
    if (servers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:2rem;color:#888;">No servers found. Click "+ Add Server" to get started.</td></tr>';
        return;
    }
    tbody.innerHTML = servers.map(server => `
        <tr>
            <td><strong>${server.server_name}</strong></td>
            <td><span class="env-badge env-${server.environment}">${server.environment}</span></td>
            <td>${server.instance_type}</td>
            <td><code>${server.ip_address}</code></td>
            <td>${server.region}</td>
            <td>${server.team}</td>
            <td><span class="status-badge status-${server.status}">${server.status}</span></td>
            <td>
                <div class="action-btns">
                    <button class="btn btn-edit" onclick="editServer('${server.server_id}')">Edit</button>
                    <button class="btn btn-danger" onclick="deleteServer('${server.server_id}')">Delete</button>
                </div>
            </td>
        </tr>
    `).join('');
}

function updateStats() {
    document.getElementById('total-count').textContent = servers.length;
    document.getElementById('running-count').textContent = servers.filter(s => s.status === 'running').length;
    document.getElementById('stopped-count').textContent = servers.filter(s => s.status === 'stopped').length;
}

function openModal() {
    document.getElementById('modal-overlay').classList.add('active');
    document.getElementById('modal-title').textContent = 'Add Server';
    document.getElementById('server-form').reset();
    document.getElementById('edit-id').value = '';
}

function closeModal() {
    document.getElementById('modal-overlay').classList.remove('active');
}

function editServer(id) {
    const server = servers.find(s => s.server_id === id);
    if (!server) return;

    document.getElementById('edit-id').value = server.server_id;
    document.getElementById('server_name').value = server.server_name;
    document.getElementById('environment').value = server.environment;
    document.getElementById('instance_type').value = server.instance_type;
    document.getElementById('ip_address').value = server.ip_address;
    document.getElementById('region').value = server.region;
    document.getElementById('team').value = server.team;
    document.getElementById('status').value = server.status;
    document.getElementById('modal-title').textContent = 'Edit Server';
    document.getElementById('modal-overlay').classList.add('active');
}

async function deleteServer(id) {
    if (!confirm('Are you sure you want to delete this server?')) return;

    try {
        await fetch(`${API_URL}/servers/${id}`, { method: 'DELETE' });
        fetchServers();
    } catch (error) {
        console.error('Error deleting server:', error);
    }
}

document.getElementById('server-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const body = {
        server_name: document.getElementById('server_name').value,
        environment: document.getElementById('environment').value,
        instance_type: document.getElementById('instance_type').value,
        ip_address: document.getElementById('ip_address').value,
        region: document.getElementById('region').value,
        team: document.getElementById('team').value,
        status: document.getElementById('status').value
    };

    const editId = document.getElementById('edit-id').value;

    try {
        if (editId) {
            await fetch(`${API_URL}/servers/${editId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
        } else {
            await fetch(`${API_URL}/servers`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
        }
        closeModal();
        fetchServers();
    } catch (error) {
        console.error('Error saving server:', error);
    }
});

// Load servers on page load
fetchServers();