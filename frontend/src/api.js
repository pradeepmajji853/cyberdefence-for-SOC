const API_BASE_URL = 'http://localhost:8000';

export const api = {
  async getLogs(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(`${API_BASE_URL}/logs?${queryString}`);
    if (!response.ok) throw new Error('Failed to fetch logs');
    return response.json();
  },

  async createLog(logEntry) {
    const response = await fetch(`${API_BASE_URL}/logs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(logEntry),
    });
    if (!response.ok) throw new Error('Failed to create log');
    return response.json();
  },

  async getAnalysis(hoursBack = 2) {
    const response = await fetch(`${API_BASE_URL}/analysis?hours_back=${hoursBack}`);
    if (!response.ok) throw new Error('Failed to get analysis');
    return response.json();
  },

  async chat(question) {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });
    if (!response.ok) throw new Error('Failed to get chat response');
    return response.json();
  },

  async getStats() {
    const response = await fetch(`${API_BASE_URL}/stats`);
    if (!response.ok) throw new Error('Failed to get stats');
    return response.json();
  },
};

export default api;
