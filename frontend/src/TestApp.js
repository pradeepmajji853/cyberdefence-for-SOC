import React, { useState, useEffect } from 'react';

function TestApp() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/logs?limit=5')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('API Response:', data);
        setLogs(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('API Error:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{color: 'white', background: 'black', padding: '20px'}}>Loading...</div>;
  if (error) return <div style={{color: 'red', background: 'black', padding: '20px'}}>Error: {error}</div>;

  return (
    <div style={{color: 'white', background: 'black', padding: '20px'}}>
      <h1>Cyber Defense Test</h1>
      <p>Found {logs.length} logs</p>
      <ul>
        {logs.map((log, index) => (
          <li key={log.id || index} style={{marginBottom: '10px'}}>
            <strong>{log.event_type}</strong> - {log.severity} - {log.message}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TestApp;
