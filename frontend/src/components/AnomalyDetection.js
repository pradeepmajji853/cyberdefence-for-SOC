import React from 'react';
import { AlertTriangle, MapPin, Clock, User, Database, Activity } from 'lucide-react';

const AnomalyDetection = ({ anomalyData }) => {
  if (!anomalyData || !anomalyData.anomalies) {
    return (
      <div className="bg-bg-secondary border border-border-primary rounded-lg shadow-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-cyber-warning bg-opacity-20 rounded-lg">
            <AlertTriangle className="w-6 h-6 text-cyber-warning" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-text-primary">Anomaly Detection</h3>
            <p className="text-sm text-text-muted">Loading anomaly detection results...</p>
          </div>
        </div>
        <div className="animate-pulse space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-bg-tertiary rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  const getAnomalyIcon = (type) => {
    switch (type.toLowerCase()) {
      case 'impossible travel':
        return <MapPin className="w-5 h-5 text-cyber-danger" />;
      case 'unusual data access':
        return <Database className="w-5 h-5 text-cyber-warning" />;
      case 'off-hours activity':
        return <Clock className="w-5 h-5 text-cyber-accent" />;
      default:
        return <Activity className="w-5 h-5 text-cyber-primary" />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'cyber-danger';
      case 'high': return 'cyber-warning';
      case 'medium': return 'cyber-accent';
      case 'low': return 'cyber-success';
      default: return 'text-muted';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.9) return 'cyber-success';
    if (confidence >= 0.7) return 'cyber-accent';
    return 'cyber-danger';
  };

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInMinutes = Math.floor((now - time) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    return `${Math.floor(diffInMinutes / 60)}h ago`;
  };

  const getConfidencePercentage = (confidence) => {
    return Math.round(confidence * 100);
  };

  return (
    <div className="bg-bg-secondary border border-border-primary rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyber-warning bg-opacity-20 rounded-lg">
            <AlertTriangle className="w-6 h-6 text-cyber-warning" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-text-primary">AI Anomaly Detection</h3>
            <p className="text-sm text-text-muted">Machine learning powered behavioral analysis</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-cyber-warning">{anomalyData.total_anomalies}</div>
          <div className="text-sm text-text-muted">Anomalies</div>
        </div>
      </div>

      <div className="space-y-4 mb-6">
        {anomalyData.anomalies.map((anomaly, index) => {
          const severityColor = getSeverityColor(anomaly.severity);
          const confidenceColor = getConfidenceColor(anomaly.confidence);
          const confidencePercentage = getConfidencePercentage(anomaly.confidence);
          
          return (
            <div key={anomaly.id || index} className="border border-border-primary bg-bg-tertiary rounded-lg p-4 hover:border-border-secondary transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-start gap-3">
                  {getAnomalyIcon(anomaly.type)}
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="font-medium text-text-primary">{anomaly.type}</h4>
                      <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                        severityColor === 'cyber-danger' ? 'bg-cyber-danger bg-opacity-20 text-cyber-danger border border-cyber-danger border-opacity-30' :
                        severityColor === 'cyber-warning' ? 'bg-cyber-warning bg-opacity-20 text-cyber-warning border border-cyber-warning border-opacity-30' :
                        severityColor === 'cyber-accent' ? 'bg-cyber-accent bg-opacity-20 text-cyber-accent border border-cyber-accent border-opacity-30' :
                        severityColor === 'cyber-success' ? 'bg-cyber-success bg-opacity-20 text-cyber-success border border-cyber-success border-opacity-30' :
                        'bg-bg-secondary text-text-muted border border-border-primary'
                      }`}>
                        {anomaly.severity.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-text-secondary mb-2">{anomaly.description}</p>
                    
                    {/* User Information */}
                    {anomaly.user && (
                      <div className="flex items-center gap-1 text-xs text-text-muted mb-2">
                        <User className="w-3 h-3" />
                        <span>User: <strong className="text-text-secondary">{anomaly.user}</strong></span>
                      </div>
                    )}
                    
                    {/* Specific Anomaly Details */}
                    {anomaly.locations && (
                      <div className="text-xs text-text-muted mb-2">
                        <strong className="text-text-secondary">Locations:</strong> {anomaly.locations.join(' → ')}
                      </div>
                    )}
                    
                    {anomaly.baseline && anomaly.current && (
                      <div className="text-xs text-text-muted mb-2">
                        <div><strong className="text-text-secondary">Baseline:</strong> {anomaly.baseline}</div>
                        <div><strong className="text-text-secondary">Current:</strong> {anomaly.current}</div>
                      </div>
                    )}
                    
                    {anomaly.expected && (
                      <div className="text-xs text-text-muted mb-2">
                        <strong className="text-text-secondary">Expected:</strong> {anomaly.expected}
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="text-xs text-text-muted mb-1">{formatTimeAgo(anomaly.timestamp)}</div>
                  <div className={`text-xs font-medium ${
                    confidenceColor === 'cyber-success' ? 'text-cyber-success' :
                    confidenceColor === 'cyber-accent' ? 'text-cyber-accent' :
                    confidenceColor === 'cyber-danger' ? 'text-cyber-danger' :
                    'text-text-muted'
                  }`}>
                    {confidencePercentage}% confidence
                  </div>
                </div>
              </div>
              
              {/* Confidence Bar */}
              <div className="mt-3">
                <div className="flex items-center justify-between text-xs text-text-muted mb-1">
                  <span>Detection Confidence</span>
                  <span>{confidencePercentage}%</span>
                </div>
                <div className="w-full bg-bg-secondary rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${
                      confidenceColor === 'cyber-success' ? 'bg-cyber-success' :
                      confidenceColor === 'cyber-accent' ? 'bg-cyber-accent' :
                      confidenceColor === 'cyber-danger' ? 'bg-cyber-danger' :
                      'bg-text-muted'
                    }`}
                    style={{ width: `${confidencePercentage}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="mt-3 pt-3 border-t border-border-primary flex justify-between items-center">
                <span className="text-xs text-text-muted">ID: {anomaly.id}</span>
                <div className="flex gap-2">
                  <button className="text-xs bg-cyber-primary bg-opacity-20 text-cyber-primary px-2 py-1 rounded hover:bg-opacity-30 transition-colors border border-cyber-primary border-opacity-30">
                    Investigate
                  </button>
                  <button className="text-xs bg-bg-tertiary text-text-secondary px-2 py-1 rounded hover:bg-bg-hover transition-colors border border-border-primary">
                    Mark Safe
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="border-t border-border-primary pt-4">
        <div className="flex items-center justify-between text-sm text-text-secondary">
          <span>Last scan completed: {formatTimeAgo(anomalyData.last_scan)}</span>
          <button className="text-cyber-primary hover:text-cyber-accent font-medium">
            Run New Scan
          </button>
        </div>
      </div>
    </div>
  );
};

export default AnomalyDetection;
