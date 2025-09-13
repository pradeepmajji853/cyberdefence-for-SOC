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
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-red-100 rounded-lg">
          <Zap className="w-6 h-6 text-red-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Attack Simulation</h3>
          <p className="text-sm text-gray-600">Simulate cyber attacks to test defense systems</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {attackTypes.map((attack) => (
          <div
            key={attack.id}
            className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
              selectedAttack === attack.id
                ? `border-${attack.color}-500 bg-${attack.color}-50`
                : 'border-gray-200 hover:border-gray-300'
            }`}
            onClick={() => setSelectedAttack(attack.id)}
          >
            <div className="flex items-start gap-3">
              {attack.icon}
              <div className="flex-1">
                <h4 className="font-medium text-gray-900 mb-1">{attack.name}</h4>
                <p className="text-sm text-gray-600 mb-2">{attack.description}</p>
                <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                  attack.severity === 'critical' 
                    ? 'bg-red-100 text-red-800'
                    : 'bg-orange-100 text-orange-800'
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
          className="flex-1 flex items-center justify-center gap-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Play className="w-4 h-4" />
          {isSimulating ? 'Simulating...' : 'Start Simulation'}
        </button>
      </div>

      {simulationResult && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <h4 className="font-medium text-green-900">Simulation Complete</h4>
          </div>
          <p className="text-sm text-green-800 mb-2">{simulationResult.message}</p>
          <div className="text-xs text-green-700">
            <strong>Attack Type:</strong> {simulationResult.attack_type}<br />
            <strong>Events Generated:</strong> {simulationResult.logs_created}
          </div>
        </div>
      )}
    </div>
  );
};

export default AttackSimulator;
