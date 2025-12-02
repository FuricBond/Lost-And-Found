/**
 * Lost & Found API Client
 * Centralized API handling for all frontend pages
 */

const API = {
    BASE_URL: '/api/v1',
    
    // Get auth token from localStorage
    getToken() {
        return localStorage.getItem('authToken');
    },
    
    // Get current user from localStorage
    getUser() {
        try {
            return JSON.parse(localStorage.getItem('currentUser'));
        } catch {
            return null;
        }
    },
    
    // Check if user is logged in
    isLoggedIn() {
        return !!this.getToken();
    },
    
    // Save auth data
    saveAuth(token, user) {
        localStorage.setItem('authToken', token);
        if (user) {
            localStorage.setItem('currentUser', JSON.stringify(user));
        }
    },
    
    // Clear auth data (logout)
    clearAuth() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('currentUser');
    },
    
    // Make API request
    async request(endpoint, options = {}) {
        const url = `${this.BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        // Add auth header if token exists
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(url, {
                ...options,
                headers
            });
            
            // Handle 401 - token expired
            if (response.status === 401) {
                this.clearAuth();
                window.location.href = '/static/login.html';
                throw new Error('Session expired. Please login again.');
            }
            
            // Handle no content
            if (response.status === 204) {
                return null;
            }
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || `Request failed: ${response.status}`);
            }
            
            return data;
        } catch (error) {
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error('Cannot connect to server. Is the backend running?');
            }
            throw error;
        }
    },
    
    // Auth endpoints
    auth: {
        async login(email, password) {
            const data = await API.request('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            return data;
        },
        
        async register(userData) {
            const data = await API.request('/users', {
                method: 'POST',
                body: JSON.stringify(userData)
            });
            return data;
        },
        
        async getProfile() {
            return await API.request('/users/me');
        }
    },
    
    // Items endpoints
    items: {
        async list(params = {}) {
            const query = new URLSearchParams(params).toString();
            return await API.request(`/items?${query}`);
        },
        
        async get(itemId) {
            return await API.request(`/items/${itemId}`);
        },
        
        async create(itemData) {
            return await API.request('/items', {
                method: 'POST',
                body: JSON.stringify(itemData)
            });
        },
        
        async update(itemId, itemData) {
            return await API.request(`/items/${itemId}`, {
                method: 'PATCH',
                body: JSON.stringify(itemData)
            });
        },
        
        async delete(itemId) {
            return await API.request(`/items/${itemId}`, {
                method: 'DELETE'
            });
        },
        
        async uploadImage(itemId, file) {
            const formData = new FormData();
            formData.append('file', file);
            
            const token = API.getToken();
            const response = await fetch(`${API.BASE_URL}/items/${itemId}/images`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Upload failed');
            }
            
            return await response.json();
        },
        
        async findMatches(itemId, params = {}) {
            const query = new URLSearchParams(params).toString();
            return await API.request(`/items/${itemId}/matches?${query}`);
        }
    },
    
    // Matches endpoints
    matches: {
        async list(params = {}) {
            const query = new URLSearchParams(params).toString();
            return await API.request(`/matches?${query}`);
        },
        
        async get(matchId) {
            return await API.request(`/matches/${matchId}`);
        },
        
        async confirm(matchId) {
            return await API.request(`/matches/${matchId}/confirm`, {
                method: 'POST',
                body: JSON.stringify({ confirmed: true })
            });
        },
        
        async reject(matchId, reason = '') {
            return await API.request(`/matches/${matchId}/confirm`, {
                method: 'POST',
                body: JSON.stringify({ confirmed: false, rejection_reason: reason })
            });
        }
    },
    
    // Notifications endpoints
    notifications: {
        async list(params = {}) {
            const query = new URLSearchParams(params).toString();
            return await API.request(`/notifications?${query}`);
        },
        
        async markRead(notificationIds) {
            return await API.request('/notifications/mark-read', {
                method: 'POST',
                body: JSON.stringify({ notification_ids: notificationIds })
            });
        },
        
        async markAllRead() {
            return await API.request('/notifications/mark-all-read', {
                method: 'POST'
            });
        }
    }
};

// UI Helpers
const UI = {
    // Show toast notification
    toast(message, type = 'info') {
        const toast = document.getElementById('toast');
        if (toast) {
            toast.textContent = message;
            toast.className = `toast show ${type}`;
            setTimeout(() => toast.classList.remove('show'), 3000);
        } else {
            console.log(`[${type}] ${message}`);
        }
    },
    
    // Update navigation based on auth state
    updateNav() {
        const authDiv = document.getElementById('navAuth');
        const userDiv = document.getElementById('navUser');
        const userName = document.getElementById('userName');
        const myItemsLink = document.getElementById('myItemsLink');
        
        if (API.isLoggedIn()) {
            const user = API.getUser();
            if (authDiv) authDiv.style.display = 'none';
            if (userDiv) userDiv.style.display = 'flex';
            if (userName) userName.textContent = user?.full_name || user?.email || 'User';
            if (myItemsLink) myItemsLink.style.display = 'inline';
        } else {
            if (authDiv) authDiv.style.display = 'flex';
            if (userDiv) userDiv.style.display = 'none';
            if (myItemsLink) myItemsLink.style.display = 'none';
        }
    },
    
    // Logout function
    logout() {
        API.clearAuth();
        window.location.href = '/';
    },
    
    // Format date
    formatDate(dateString) {
        if (!dateString) return 'Unknown';
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric', month: 'short', day: 'numeric'
        });
    },
    
    // Escape HTML
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    // Get category icon
    getCategoryIcon(category) {
        const icons = {
            phone: '📱', wallet: '👛', keys: '🔑', bag: '👜', laptop: '💻',
            tablet: '📱', watch: '⌚', jewelry: '💍', glasses: '👓',
            headphones: '🎧', camera: '📷', documents: '📄', pet: '🐕',
            clothing: '👕', electronics: '🔌', other: '📦'
        };
        return icons[category] || '📦';
    },
    
    // Require auth - redirect to login if not logged in
    requireAuth() {
        if (!API.isLoggedIn()) {
            window.location.href = '/static/login.html';
            return false;
        }
        return true;
    }
};

// Make logout available globally
window.logout = UI.logout;
