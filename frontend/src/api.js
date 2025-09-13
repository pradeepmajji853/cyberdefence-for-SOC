const API_BASE_URL = 'http://localhost:8001';

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

  // New API methods for enhanced features
  async simulateAttack(attackType) {
    const response = await fetch(`${API_BASE_URL}/simulate-attack?attack_type=${attackType}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) throw new Error('Failed to simulate attack');
    return response.json();
  },

  async getThreatIntelligence() {
    const response = await fetch(`${API_BASE_URL}/threat-intelligence`);
    if (!response.ok) throw new Error('Failed to fetch threat intelligence');
    return response.json();
  },

  async getAttackMapData() {
    const response = await fetch(`${API_BASE_URL}/attack-map-data`);
    if (!response.ok) throw new Error('Failed to fetch attack map data');
    return response.json();
  },

  async executeAction(action, target) {
    const response = await fetch(`${API_BASE_URL}/execute-action?action=${action}&target=${target}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) throw new Error('Failed to execute action');
    return response.json();
  },

  async getAnomalyDetection() {
    const response = await fetch(`${API_BASE_URL}/anomaly-detection`);
    if (!response.ok) throw new Error('Failed to fetch anomaly detection');
    return response.json();
  },
};

export default api;
