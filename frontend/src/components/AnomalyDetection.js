import React from 'react';
import { AlertTriangle, MapPin, Clock, User, Database, Activity } from 'lucide-react';

const AnomalyDetection = ({ anomalyData }) => {
  if (!anomalyData || !anomalyData.anomalies) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-orange-100 rounded-lg">
            <AlertTriangle className="w-6 h-6 text-orange-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Anomaly Detection</h3>
            <p className="text-sm text-gray-600">Loading anomaly detection results...</p>
          </div>
        </div>
        <div className="animate-pulse space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  const getAnomalyIcon = (type) => {
    switch (type.toLowerCase()) {
      case 'impossible travel':
        return <MapPin className="w-5 h-5 text-red-500" />;
      case 'unusual data access':
        return <Database className="w-5 h-5 text-orange-500" />;
      case 'off-hours activity':
        return <Clock className="w-5 h-5 text-yellow-500" />;
      default:
        return <Activity className="w-5 h-5 text-blue-500" />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'red';
      case 'high': return 'orange';
      case 'medium': return 'yellow';
      case 'low': return 'blue';
      default: return 'gray';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.9) return 'green';
    if (confidence >= 0.7) return 'yellow';
    return 'red';
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
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-orange-100 rounded-lg">
            <AlertTriangle className="w-6 h-6 text-orange-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">AI Anomaly Detection</h3>
            <p className="text-sm text-gray-600">Machine learning powered behavioral analysis</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-orange-600">{anomalyData.total_anomalies}</div>
          <div className="text-sm text-gray-600">Anomalies</div>
        </div>
      </div>

      <div className="space-y-4 mb-6">
        {anomalyData.anomalies.map((anomaly, index) => {
          const severityColor = getSeverityColor(anomaly.severity);
          const confidenceColor = getConfidenceColor(anomaly.confidence);
          const confidencePercentage = getConfidencePercentage(anomaly.confidence);
          
          return (
            <div key={anomaly.id || index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-start gap-3">
                  {getAnomalyIcon(anomaly.type)}
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="font-medium text-gray-900">{anomaly.type}</h4>
                      <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium bg-${severityColor}-100 text-${severityColor}-800`}>
                        {anomaly.severity.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 mb-2">{anomaly.description}</p>
                    
                    {/* User Information */}
                    {anomaly.user && (
                      <div className="flex items-center gap-1 text-xs text-gray-600 mb-2">
                        <User className="w-3 h-3" />
                        <span>User: <strong>{anomaly.user}</strong></span>
                      </div>
                    )}
                    
                    {/* Specific Anomaly Details */}
                    {anomaly.locations && (
                      <div className="text-xs text-gray-600 mb-2">
                        <strong>Locations:</strong> {anomaly.locations.join(' → ')}
                      </div>
                    )}
                    
                    {anomaly.baseline && anomaly.current && (
                      <div className="text-xs text-gray-600 mb-2">
                        <div><strong>Baseline:</strong> {anomaly.baseline}</div>
                        <div><strong>Current:</strong> {anomaly.current}</div>
                      </div>
                    )}
                    
                    {anomaly.expected && (
                      <div className="text-xs text-gray-600 mb-2">
                        <strong>Expected:</strong> {anomaly.expected}
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="text-right">
                  <div className="text-xs text-gray-500 mb-1">{formatTimeAgo(anomaly.timestamp)}</div>
                  <div className={`text-xs font-medium text-${confidenceColor}-600`}>
                    {confidencePercentage}% confidence
                  </div>
                </div>
              </div>
              
              {/* Confidence Bar */}
              <div className="mt-3">
                <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                  <span>Detection Confidence</span>
                  <span>{confidencePercentage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full bg-${confidenceColor}-500`}
                    style={{ width: `${confidencePercentage}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="mt-3 pt-3 border-t border-gray-100 flex justify-between items-center">
                <span className="text-xs text-gray-500">ID: {anomaly.id}</span>
                <div className="flex gap-2">
                  <button className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded hover:bg-blue-200 transition-colors">
                    Investigate
                  </button>
                  <button className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded hover:bg-gray-200 transition-colors">
                    Mark Safe
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="border-t border-gray-200 pt-4">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <span>Last scan completed: {formatTimeAgo(anomalyData.last_scan)}</span>
          <button className="text-blue-600 hover:text-blue-800 font-medium">
            Run New Scan
          </button>
        </div>
      </div>
    </div>
  );
};

export default AnomalyDetection;
