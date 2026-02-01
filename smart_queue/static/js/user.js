// User-facing JavaScript functionality

// Token request handler
const tokenRequest = {
    form: null,
    
    init: () => {
        tokenRequest.form = document.getElementById('token-form');
        if (tokenRequest.form) {
            tokenRequest.form.addEventListener('submit', tokenRequest.handleSubmit);
        }
    },
    
    handleSubmit: async (e) => {
        e.preventDefault();
        
        const formData = {
            user_name: document.getElementById('user-name').value,
            user_type: document.getElementById('user-type').value,
            department: document.getElementById('department').value
        };
        
        try {
            const result = await utils.api('/api/token/request', 'POST', formData);
            
            if (result.success) {
                tokenRequest.showResult(result);
            } else {
                utils.showNotification(result.error || 'Failed to generate token', 'error');
            }
        } catch (error) {
            utils.showNotification('Failed to request token. Please try again.', 'error');
        }
    },
    
    showResult: (result) => {
        const tokenResult = document.getElementById('token-result');
        const form = document.getElementById('token-form');
        
        form.style.display = 'none';
        tokenResult.style.display = 'block';
        
        document.getElementById('result-token-id').textContent = result.token_id;
        document.getElementById('result-position').textContent = result.queue_position;
        document.getElementById('result-wait').textContent = result.waiting_time + ' mins';
        document.getElementById('result-counter').textContent = result.counter;
        document.getElementById('result-department').textContent = result.department;
    }
};

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', tokenRequest.init);
} else {
    tokenRequest.init();
}
