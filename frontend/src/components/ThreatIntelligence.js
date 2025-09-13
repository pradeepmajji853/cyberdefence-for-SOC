import React from 'react';
import { AlertTriangle, Globe, Clock, TrendingUp, ExternalLink } from 'lucide-react';

const ThreatIntelligence = ({ threatData }) => {
  if (!threatData || !threatData.feeds) {
    return (
      <div className="bg-bg-secondary border border-border-primary rounded-lg shadow-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-cyber-danger bg-opacity-20 rounded-lg">
            <Globe className="w-6 h-6 text-cyber-danger" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-text-primary">Global Threat Intelligence</h3>
            <p className="text-sm text-text-muted">Loading threat intelligence feeds...</p>
          </div>
        </div>
        <div className="animate-pulse space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-20 bg-bg-tertiary border border-border-primary rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  const getSeverityColor = (severity) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'red';
      case 'high': return 'orange';
      case 'medium': return 'yellow';
      default: return 'blue';
    }
  };

  const getConfidenceColor = (confidence) => {
    switch (confidence.toLowerCase()) {
      case 'confirmed': return 'green';
      case 'high': return 'blue';
      case 'medium': return 'yellow';
      default: return 'gray';
    }
  };

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInHours = Math.floor((now - time) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours === 1) return '1 hour ago';
    return `${diffInHours} hours ago`;
  };

  return (
    <div className="bg-bg-secondary border border-border-primary rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyber-danger bg-opacity-20 rounded-lg">
            <Globe className="w-6 h-6 text-cyber-danger" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-text-primary">Global Threat Intelligence</h3>
            <p className="text-sm text-text-muted">Real-time military cyber threat feeds</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-sm text-text-secondary">Last Updated</div>
          <div className="text-xs text-text-muted">{formatTimeAgo(threatData.last_updated)}</div>
        </div>
      </div>

      <div className="space-y-4">
        {threatData.feeds.map((threat, index) => {
          const severityColor = getSeverityColor(threat.severity);
          const confidenceColor = getConfidenceColor(threat.confidence);
          
          return (
            <div key={threat.id || index} className="border border-border-primary bg-bg-tertiary rounded-lg p-4 hover:border-border-secondary transition-colors">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <AlertTriangle className={`w-5 h-5 text-cyber-${severityColor === 'red' ? 'danger' : severityColor === 'orange' ? 'warning' : severityColor === 'yellow' ? 'accent' : 'primary'}`} />
                  <h4 className="font-medium text-text-primary">{threat.title}</h4>
                </div>
                <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                  severityColor === 'red' ? 'bg-cyber-danger bg-opacity-20 text-cyber-danger border border-cyber-danger border-opacity-30' :
                  severityColor === 'orange' ? 'bg-cyber-warning bg-opacity-20 text-cyber-warning border border-cyber-warning border-opacity-30' :
                  severityColor === 'yellow' ? 'bg-cyber-accent bg-opacity-20 text-cyber-accent border border-cyber-accent border-opacity-30' :
                  'bg-cyber-primary bg-opacity-20 text-cyber-primary border border-cyber-primary border-opacity-30'
                }`}>
                  {threat.severity.toUpperCase()}
                </span>
              </div>
              
              <p className="text-sm text-text-secondary mb-3">{threat.description}</p>
              
              <div className="flex flex-wrap gap-4 mb-3 text-xs">
                <div className="flex items-center gap-1">
                  <Globe className="w-3 h-3 text-text-muted" />
                  <span className="text-text-secondary">{threat.region}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3 text-text-muted" />
                  <span className="text-text-secondary">{formatTimeAgo(threat.timestamp)}</span>
                </div>
                <div className="flex items-center gap-1">
                  <TrendingUp className="w-3 h-3 text-text-muted" />
                  <span className={`${
                    confidenceColor === 'green' ? 'text-cyber-success' :
                    confidenceColor === 'blue' ? 'text-cyber-primary' :
                    confidenceColor === 'yellow' ? 'text-cyber-accent' :
                    'text-text-muted'
                  } font-medium`}>
                    {threat.confidence} confidence
                  </span>
                </div>
              </div>
              
              {threat.indicators && threat.indicators.length > 0 && (
                <div>
                  <div className="text-xs font-medium text-text-primary mb-1">Indicators:</div>
                  <div className="flex flex-wrap gap-1">
                    {threat.indicators.map((indicator, i) => (
                      <span 
                        key={i} 
                        className="inline-flex px-2 py-1 bg-bg-primary bg-opacity-20 text-text-primary text-xs rounded font-mono border border-border-primary"
                      >
                        {indicator}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="mt-3 pt-3 border-t border-border-primary flex justify-between items-center">
                <span className="text-xs text-text-muted">ID: {threat.id}</span>
                <button className="flex items-center gap-1 text-xs text-cyber-primary hover:text-cyber-accent transition-colors">
                  <ExternalLink className="w-3 h-3" />
                  View Details
                </button>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="mt-6 p-3 bg-cyber-primary bg-opacity-20 border border-cyber-primary border-opacity-30 rounded-lg">
        <div className="flex items-center gap-2 text-sm text-cyber-primary">
          <AlertTriangle className="w-4 h-4" />
          <span className="font-medium">
            {threatData.total_threats} active threats detected globally
          </span>
        </div>
      </div>
    </div>
  );
};

export default ThreatIntelligence;
