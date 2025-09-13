import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, Activity } from 'lucide-react';

function SimpleApp() {
  const [logs, setLogs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching data...');
        
        // Fetch logs
        const logsResponse = await fetch('http://localhost:8000/logs?limit=10');
        const logsData = await logsResponse.json();
        console.log('Logs:', logsData);
        setLogs(logsData || []);
        
        // Fetch stats
        const statsResponse = await fetch('http://localhost:8000/stats');
        const statsData = await statsResponse.json();
        console.log('Stats:', statsData);
        setStats(statsData);
        
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  const containerStyle = {
    minHeight: '100vh',
    backgroundColor: '#0a0e16',
    color: 'white',
    fontFamily: 'monospace',
    padding: '20px'
  };

  const headerStyle = {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '30px',
    padding: '20px',
    backgroundColor: '#1a1f2e',
    border: '1px solid #00d4ff',
    borderRadius: '8px'
  };

  const logItemStyle = {
    backgroundColor: '#2a3441',
    padding: '15px',
    margin: '10px 0',
    borderRadius: '5px',
    border: '1px solid #00d4ff'
  };

  if (loading) {
    return (
      <div style={containerStyle}>
        <h1>CYBER DEFENSE ASSISTANT - Loading...</h1>
      </div>
    );
  }

  return (
    <div style={containerStyle}>
      <header style={headerStyle}>
        <Shield size={32} color="#00d4ff" style={{ marginRight: '15px' }} />
        <div>
          <h1 style={{ margin: 0, color: '#00d4ff', fontSize: '28px' }}>
            CYBER DEFENSE ASSISTANT
          </h1>
          <p style={{ margin: 0, color: '#888' }}>MILITARY SOC v1.0</p>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center' }}>
          <Activity size={16} color="#00ff41" style={{ marginRight: '8px' }} />
          <span style={{ color: '#00ff41' }}>OPERATIONAL</span>
        </div>
      </header>

      <div style={{ display: 'flex', gap: '20px' }}>
        {/* Stats Panel */}
        <div style={{ flex: 1, backgroundColor: '#1a1f2e', padding: '20px', borderRadius: '8px', border: '1px solid #00d4ff' }}>
          <h2 style={{ color: '#00ff41', marginTop: 0 }}>THREAT OVERVIEW</h2>
          {stats && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px', textAlign: 'center' }}>
              <div>
                <div style={{ color: '#ff0040', fontSize: '24px', fontWeight: 'bold' }}>{stats.last_24h_severity.critical}</div>
                <div>Critical</div>
              </div>
              <div>
                <div style={{ color: '#ff6b6b', fontSize: '24px', fontWeight: 'bold' }}>{stats.last_24h_severity.high}</div>
                <div>High</div>
              </div>
              <div>
                <div style={{ color: '#ffff00', fontSize: '24px', fontWeight: 'bold' }}>{stats.last_24h_severity.medium}</div>
                <div>Medium</div>
              </div>
              <div>
                <div style={{ color: '#00ff41', fontSize: '24px', fontWeight: 'bold' }}>{stats.last_24h_severity.low}</div>
                <div>Low</div>
              </div>
            </div>
          )}
        </div>

        {/* Logs Panel */}
        <div style={{ flex: 2, backgroundColor: '#1a1f2e', padding: '20px', borderRadius: '8px', border: '1px solid #00d4ff' }}>
          <h2 style={{ color: '#00d4ff', marginTop: 0 }}>RECENT SECURITY EVENTS ({logs.length})</h2>
          <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
            {logs.map((log, index) => (
              <div key={log.id || index} style={logItemStyle}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ 
                    color: log.severity === 'critical' ? '#ff0040' : 
                           log.severity === 'high' ? '#ff6b6b' :
                           log.severity === 'medium' ? '#ffff00' : '#00ff41',
                    fontWeight: 'bold'
                  }}>
                    {log.severity?.toUpperCase()}
                  </span>
                  <span style={{ color: '#888', fontSize: '12px' }}>
                    {new Date(log.timestamp).toLocaleString()}
                  </span>
                </div>
                <div style={{ color: '#00d4ff', fontWeight: 'bold', marginBottom: '5px' }}>
                  {log.event_type}
                </div>
                <div style={{ color: '#ccc', fontSize: '14px', marginBottom: '5px' }}>
                  {log.source_ip} → {log.dest_ip}
                </div>
                <div style={{ color: '#aaa', fontSize: '13px' }}>
                  {log.message}
                </div>
              </div>
            ))}
          </div>
          
          {logs.length === 0 && (
            <div style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
              No security events found
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SimpleApp;
