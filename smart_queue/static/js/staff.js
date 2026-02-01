// Staff-facing JavaScript functionality

// Dashboard management
const dashboard = {
    refreshInterval: null,
    
    init: () => {
        if (document.getElementById('pending-count')) {
            dashboard.load();
            dashboard.refreshInterval = setInterval(dashboard.load, 5000);
        }
    },
    
    load: async () => {
        try {
            // Load stats
            const stats = await utils.api('/api/dashboard/stats');
            if (stats) {
                document.getElementById('pending-count').textContent = stats.pending;
                document.getElementById('serving-count').textContent = stats.serving;
                document.getElementById('served-count').textContent = stats.served;
                document.getElementById('avg-wait').textContent = stats.avg_wait;
            }
            
            // Load recent activity
            const activity = await utils.api('/api/dashboard/activity');
            if (activity) {
                dashboard.renderActivity(activity);
            }
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    },
    
    renderActivity: (activity) => {
        const tbody = document.getElementById('activity-tbody');
        if (!tbody) return;
        
        if (activity.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No recent activity</td></tr>';
        } else {
            tbody.innerHTML = activity.map(token => `
                <tr>
                    <td><span class="token-badge">${token.token_id}</span></td>
                    <td>${token.user_name}</td>
                    <td><span class="badge badge-${token.user_type.toLowerCase()}">${token.user_type}</span></td>
                    <td><span class="status-${token.status.toLowerCase()}">${token.status}</span></td>
                    <td>${utils.formatTime(token.timestamp)}</td>
                </tr>
            `).join('');
        }
    }
};

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', dashboard.init);
} else {
    dashboard.init();
}
