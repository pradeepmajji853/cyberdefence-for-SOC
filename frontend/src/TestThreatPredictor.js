// Test file to debug ThreatPredictor issues
import React from 'react';
import ThreatPredictor from './components/ThreatPredictor';

// Mock data for testing
const mockLogs = [
  {
    id: 1,
    timestamp: new Date().toISOString(),
    event_type: 'Malware Detection',
    severity: 'high',
    source_ip: '192.168.1.100',
    dest_ip: '10.0.0.1',
    message: 'Test malware detected'
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 3600000).toISOString(),
    event_type: 'Phishing Attempt',
    severity: 'medium',
    source_ip: '203.0.113.45',
    dest_ip: '192.168.1.50',
    message: 'Suspicious email detected'
  }
];

function TestThreatPredictor() {
  console.log('Testing ThreatPredictor with mock logs:', mockLogs);
  
  return (
    <div className="p-4">
      <h1>ThreatPredictor Test</h1>
      <ThreatPredictor logs={mockLogs} />
    </div>
  );
}

export default TestThreatPredictor;
