// Common JavaScript utilities for Smart Campus Queue Management

// Global utility functions
const utils = {
    // Format timestamp to readable time
    formatTime: (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    },
    
    // Format date
    formatDate: (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleDateString('en-US');
    },
    
    // Show notification
    showNotification: (message, type = 'info') => {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    },
    
    // API call wrapper
    api: async (endpoint, method = 'GET', data = null) => {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(endpoint, options);
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
};

// Make utils globally available
window.utils = utils;
