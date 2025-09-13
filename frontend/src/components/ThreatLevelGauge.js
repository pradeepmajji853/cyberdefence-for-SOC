import React from 'react';
import { AlertTriangle, Shield, TrendingUp, Activity } from 'lucide-react';

const ThreatLevelGauge = ({ threatLevel, stats }) => {
  const getThreatLevel = () => {
    if (!stats) return { level: 'unknown', color: 'gray', percentage: 0 };
    
    const criticalCount = stats.last_24h_severity?.critical || 0;
    const highCount = stats.last_24h_severity?.high || 0;
    const totalCriticalHigh = criticalCount + highCount;
    
    if (totalCriticalHigh > 10) {
      return { level: 'critical', color: 'red', percentage: 95 };
    } else if (totalCriticalHigh > 5) {
      return { level: 'high', color: 'orange', percentage: 75 };
    } else if (totalCriticalHigh > 2) {
      return { level: 'medium', color: 'yellow', percentage: 50 };
    } else {
      return { level: 'low', color: 'green', percentage: 25 };
    }
  };

  const threat = getThreatLevel();
  
  const getThreatIcon = () => {
    switch (threat.level) {
      case 'critical':
        return <AlertTriangle className="w-8 h-8 text-red-500" />;
      case 'high':
        return <TrendingUp className="w-8 h-8 text-orange-500" />;
      case 'medium':
        return <Activity className="w-8 h-8 text-yellow-500" />;
      case 'low':
        return <Shield className="w-8 h-8 text-green-500" />;
      default:
        return <Shield className="w-8 h-8 text-gray-500" />;
    }
  };

  const getThreatMessage = () => {
    switch (threat.level) {
      case 'critical':
        return 'Multiple critical threats detected. Immediate action required.';
      case 'high':
        return 'High-priority threats identified. Enhanced monitoring active.';
      case 'medium':
        return 'Moderate threat activity. Standard protocols in effect.';
      case 'low':
        return 'Low threat environment. Systems operating normally.';
      default:
        return 'Threat level assessment in progress...';
    }
  };

  const radius = 80;
  const strokeWidth = 12;
  const normalizedRadius = radius - strokeWidth * 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDasharray = `${threat.percentage / 100 * circumference} ${circumference}`;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className={`p-2 bg-${threat.color}-100 rounded-lg`}>
          {getThreatIcon()}
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Threat Level</h3>
          <p className="text-sm text-gray-600">Real-time security posture assessment</p>
        </div>
      </div>

      <div className="flex flex-col items-center">
        {/* Circular Progress Gauge */}
        <div className="relative mb-4">
          <svg
            height={radius * 2}
            width={radius * 2}
            className="transform -rotate-90"
          >
            {/* Background circle */}
            <circle
              stroke="#e5e7eb"
              fill="transparent"
              strokeWidth={strokeWidth}
              r={normalizedRadius}
              cx={radius}
              cy={radius}
            />
            {/* Progress circle */}
            <circle
              stroke={`rgb(${
                threat.color === 'red' ? '239, 68, 68' :
                threat.color === 'orange' ? '249, 115, 22' :
                threat.color === 'yellow' ? '234, 179, 8' :
                threat.color === 'green' ? '34, 197, 94' :
                '107, 114, 128'
              })`}
              fill="transparent"
              strokeWidth={strokeWidth}
              strokeDasharray={strokeDasharray}
              strokeDashoffset={0}
              strokeLinecap="round"
              r={normalizedRadius}
              cx={radius}
              cy={radius}
              className="transition-all duration-1000 ease-in-out"
            />
          </svg>
          
          {/* Center content */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className={`text-3xl font-bold text-${threat.color}-600 mb-1`}>
              {threat.percentage}%
            </div>
            <div className={`text-sm font-medium text-${threat.color}-800 uppercase tracking-wide`}>
              {threat.level}
            </div>
          </div>
        </div>

        {/* Threat Level Description */}
        <div className="text-center mb-6">
          <p className="text-sm text-gray-700 max-w-xs">
            {getThreatMessage()}
          </p>
        </div>

        {/* Quick Stats */}
        {stats && (
          <div className="w-full grid grid-cols-2 gap-4 text-center">
            <div className="bg-red-50 rounded-lg p-3">
              <div className="text-xl font-bold text-red-600">
                {stats.last_24h_severity?.critical || 0}
              </div>
              <div className="text-xs text-red-800">Critical</div>
            </div>
            <div className="bg-orange-50 rounded-lg p-3">
              <div className="text-xl font-bold text-orange-600">
                {stats.last_24h_severity?.high || 0}
              </div>
              <div className="text-xs text-orange-800">High</div>
            </div>
            <div className="bg-yellow-50 rounded-lg p-3">
              <div className="text-xl font-bold text-yellow-600">
                {stats.last_24h_severity?.medium || 0}
              </div>
              <div className="text-xs text-yellow-800">Medium</div>
            </div>
            <div className="bg-blue-50 rounded-lg p-3">
              <div className="text-xl font-bold text-blue-600">
                {stats.last_24h_severity?.low || 0}
              </div>
              <div className="text-xs text-blue-800">Low</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ThreatLevelGauge;
