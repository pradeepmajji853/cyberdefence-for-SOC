import React, { useState } from 'react';
import { Zap, Shield, AlertTriangle, Target, Play, CheckCircle } from 'lucide-react';

const AttackSimulator = ({ onSimulateAttack, simulationResult }) => {
  const [selectedAttack, setSelectedAttack] = useState('');
  const [isSimulating, setIsSimulating] = useState(false);

  const attackTypes = [
    {
      id: 'ddos',
      name: 'DDoS Attack',
      description: 'Distributed Denial of Service attack overwhelming network resources',
      icon: <Zap className="w-6 h-6 text-red-500" />,
      severity: 'critical',
      color: 'red'
    },
    {
      id: 'phishing',
      name: 'Phishing Campaign',
      description: 'Social engineering attack targeting user credentials',
      icon: <Target className="w-6 h-6 text-orange-500" />,
      severity: 'high',
      color: 'orange'
    },
    {
      id: 'insider_threat',
      name: 'Insider Threat',
      description: 'Malicious activity from privileged internal user',
      icon: <AlertTriangle className="w-6 h-6 text-red-600" />,
      severity: 'critical',
      color: 'red'
    },
    {
      id: 'ransomware',
      name: 'Ransomware Attack',
      description: 'File encryption and system compromise attack',
      icon: <Shield className="w-6 h-6 text-purple-500" />,
      severity: 'critical',
      color: 'purple'
    }
  ];

  const handleSimulate = async (attackType) => {
    setSelectedAttack(attackType);
    setIsSimulating(true);
    
    try {
      await onSimulateAttack(attackType);
    } catch (error) {
      console.error('Simulation failed:', error);
    }
    
    setIsSimulating(false);
  };

  return (
    <div className="bg-bg-secondary border border-border-primary rounded-lg shadow-lg p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-cyber-danger bg-opacity-20 rounded-lg">
          <Zap className="w-6 h-6 text-cyber-danger" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-text-primary">Attack Simulation</h3>
          <p className="text-sm text-text-muted">Simulate cyber attacks to test defense systems</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {attackTypes.map((attack) => (
          <div
            key={attack.id}
            className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
              selectedAttack === attack.id
                ? 'border-cyber-danger bg-cyber-danger bg-opacity-20'
                : 'border-border-primary hover:border-border-secondary'
            }`}
            onClick={() => setSelectedAttack(attack.id)}
          >
            <div className="flex items-start gap-3">
              {attack.icon}
              <div className="flex-1">
                <h4 className="font-medium text-text-primary mb-1">{attack.name}</h4>
                <p className="text-sm text-text-secondary mb-2">{attack.description}</p>
                <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                  attack.severity === 'critical' 
                    ? 'bg-cyber-danger bg-opacity-20 text-cyber-danger border border-cyber-danger border-opacity-30'
                    : 'bg-cyber-warning bg-opacity-20 text-cyber-warning border border-cyber-warning border-opacity-30'
                }`}>
                  {attack.severity.toUpperCase()}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => handleSimulate(selectedAttack)}
          disabled={!selectedAttack || isSimulating}
          className="flex-1 flex items-center justify-center gap-2 bg-cyber-danger text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Play className="w-4 h-4" />
          {isSimulating ? 'Simulating...' : 'Start Simulation'}
        </button>
      </div>

      {simulationResult && (
        <div className="mt-6 p-4 bg-cyber-success bg-opacity-20 border border-cyber-success border-opacity-30 rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="w-5 h-5 text-cyber-success" />
            <h4 className="font-medium text-cyber-success">Simulation Complete</h4>
          </div>
          <p className="text-sm text-text-secondary mb-2">{simulationResult.message}</p>
          <div className="text-xs text-text-muted">
            <strong>Attack Type:</strong> {simulationResult.attack_type}<br />
            <strong>Events Generated:</strong> {simulationResult.logs_created}
          </div>
        </div>
      )}
    </div>
  );
};

export default AttackSimulator;
