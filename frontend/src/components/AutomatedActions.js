import React, { useState } from 'react';
import { Shield, Ban, AlertCircle, Play, CheckCircle, Clock, XCircle } from 'lucide-react';

const AutomatedActions = ({ onExecuteAction }) => {
  const [executionResults, setExecutionResults] = useState([]);
  const [executingAction, setExecutingAction] = useState(null);

  const recommendedActions = [
    {
      id: 'block_ip_203',
      type: 'block_ip',
      target: '203.0.113.45',
      title: 'Block Malicious IP',
      description: 'Block IP address 203.0.113.45 detected in multiple attack attempts',
      severity: 'high',
      icon: <Ban className="w-5 h-5 text-red-500" />,
      urgency: 'immediate'
    },
    {
      id: 'isolate_host_65',
      type: 'isolate_host',
      target: '192.168.1.65',
      title: 'Isolate Compromised Host',
      description: 'Isolate host 192.168.1.65 showing signs of ransomware infection',
      severity: 'critical',
      icon: <Shield className="w-5 h-5 text-orange-500" />,
      urgency: 'immediate'
    },
    {
      id: 'escalate_breach',
      type: 'escalate_incident',
      target: 'BREACH-2024-001',
      title: 'Escalate Security Breach',
      description: 'Escalate critical system breach to SOC Level 2',
      severity: 'critical',
      icon: <AlertCircle className="w-5 h-5 text-red-600" />,
      urgency: 'immediate'
    },
    {
      id: 'monitor_admin',
      type: 'enable_monitoring',
      target: 'admin_miller',
      title: 'Enhanced User Monitoring',
      description: 'Enable enhanced monitoring for user admin_miller after anomaly detection',
      severity: 'medium',
      icon: <Clock className="w-5 h-5 text-yellow-500" />,
      urgency: 'scheduled'
    }
  ];

  const handleExecuteAction = async (action) => {
    setExecutingAction(action.id);
    
    try {
      const result = await onExecuteAction(action.type, action.target);
      
      const executionRecord = {
        id: Date.now(),
        action: action,
        result: result,
        timestamp: new Date().toISOString(),
        status: 'success'
      };
      
      setExecutionResults(prev => [executionRecord, ...prev.slice(0, 4)]); // Keep last 5 results
    } catch (error) {
      const executionRecord = {
        id: Date.now(),
        action: action,
        result: { message: 'Execution failed: ' + error.message },
        timestamp: new Date().toISOString(),
        status: 'error'
      };
      
      setExecutionResults(prev => [executionRecord, ...prev.slice(0, 4)]);
    }
    
    setExecutingAction(null);
  };

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'red';
      case 'high': return 'orange';
      case 'medium': return 'yellow';
      default: return 'blue';
    }
  };

  const getUrgencyBadge = (urgency) => {
    const colors = {
      immediate: 'bg-red-100 text-red-800',
      scheduled: 'bg-yellow-100 text-yellow-800',
      routine: 'bg-blue-100 text-blue-800'
    };
    
    return colors[urgency] || colors.routine;
  };

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInSeconds = Math.floor((now - time) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
    return `${Math.floor(diffInSeconds / 3600)}h ago`;
  };

  return (
    <div className="space-y-6">
      {/* Recommended Actions */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Shield className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Automated Recommendations</h3>
            <p className="text-sm text-gray-600">AI-suggested security actions for immediate execution</p>
          </div>
        </div>

        <div className="space-y-4">
          {recommendedActions.map((action) => {
            const severityColor = getSeverityColor(action.severity);
            const isExecuting = executingAction === action.id;
            
            return (
              <div key={action.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-start gap-3">
                    {action.icon}
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 mb-1">{action.title}</h4>
                      <p className="text-sm text-gray-600 mb-2">{action.description}</p>
                      <div className="flex items-center gap-2">
                        <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium bg-${severityColor}-100 text-${severityColor}-800`}>
                          {action.severity.toUpperCase()}
                        </span>
                        <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${getUrgencyBadge(action.urgency)}`}>
                          {action.urgency.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleExecuteAction(action)}
                    disabled={isExecuting}
                    className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <Play className="w-4 h-4" />
                    {isExecuting ? 'Executing...' : 'Execute'}
                  </button>
                </div>
                
                <div className="text-xs text-gray-500">
                  <strong>Target:</strong> {action.target}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Execution History */}
      {executionResults.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Recent Executions</h3>
              <p className="text-sm text-gray-600">History of automated security actions</p>
            </div>
          </div>

          <div className="space-y-3">
            {executionResults.map((execution) => (
              <div key={execution.id} className={`p-4 rounded-lg border ${
                execution.status === 'success' 
                  ? 'bg-green-50 border-green-200' 
                  : 'bg-red-50 border-red-200'
              }`}>
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {execution.status === 'success' ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-600" />
                    )}
                    <h4 className="font-medium text-gray-900">{execution.action.title}</h4>
                  </div>
                  <span className="text-xs text-gray-500">{formatTimeAgo(execution.timestamp)}</span>
                </div>
                
                <p className={`text-sm ${
                  execution.status === 'success' ? 'text-green-800' : 'text-red-800'
                } mb-2`}>
                  {execution.result.message}
                </p>
                
                {execution.result.execution_id && (
                  <div className="text-xs text-gray-600">
                    <strong>Execution ID:</strong> {execution.result.execution_id}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AutomatedActions;
