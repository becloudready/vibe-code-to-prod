const API_BASE_URL = 'http://localhost:5000'; // Change port as needed

const dataService = {
  // Register user with backend API
  async register({ name, age, username, password }) {
    try {
      const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, age, username, password })
      });
      if (!response.ok) {
        const errorData = await response.json();
        return { success: false, message: errorData.message || 'Registration failed' };
      }
      return { success: true };
    } catch (error) {
      console.error('Error registering user:', error);
      return { success: false, message: 'Network error' };
    }
  },
  // Get all users from backend API
  async getAllUsers() {
    try {
      const response = await fetch(`${API_BASE_URL}/getAllUsers`);
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching users:', error);
      return [];
    }
  },
  // Login user with backend API
  async login(username, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      return await response.json();
    } catch (error) {
      console.error('Error logging in:', error);
      return { success: false, message: 'Network error' };
    }
  },
};

export default dataService;
