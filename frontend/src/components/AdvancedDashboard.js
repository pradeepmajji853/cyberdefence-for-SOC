import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, Activity, Shield, AlertTriangle, Eye, Zap } from 'lucide-react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const AdvancedDashboard = ({ logs, stats, analysis }) => {
  const [realTimeMetrics, setRealTimeMetrics] = useState({
    activeThreats: 0,
    blockedAttacks: 0,
    systemHealth: 98,
    responseTime: 0.45
  });

  const [threatTrends, setThreatTrends] = useState([]);
  const [severityDistribution, setSeverityDistribution] = useState([]);
  const [attackTypes, setAttackTypes] = useState([]);
  const [timeline, setTimeline] = useState([]);

  // Colors for professional look
  const colors = {
    primary: '#00D9FF',
    danger: '#FF4444',
    warning: '#FFB800',
    success: '#00FF88',
    info: '#8B8BFF'
  };

  useEffect(() => {
    if (logs && logs.length > 0) {
      generateDashboardData();
      
      // Simulate real-time updates
      const interval = setInterval(() => {
        setRealTimeMetrics(prev => ({
          ...prev,
          activeThreats: Math.max(0, prev.activeThreats + Math.floor(Math.random() * 3) - 1),
          blockedAttacks: prev.blockedAttacks + Math.floor(Math.random() * 2),
          systemHealth: Math.min(100, Math.max(85, prev.systemHealth + Math.random() * 2 - 1)),
          responseTime: Math.max(0.1, prev.responseTime + (Math.random() - 0.5) * 0.1)
        }));
      }, 3000);

      return () => clearInterval(interval);
    }
  }, [logs]);

  const generateDashboardData = () => {
    if (!logs || logs.length === 0) return;

    // Generate severity distribution
    const severityCounts = logs.reduce((acc, log) => {
      acc[log.severity] = (acc[log.severity] || 0) + 1;
      return acc;
    }, {});

    const severityColors = {
      critical: colors.danger,
      high: colors.warning,
      medium: colors.info,
      low: colors.success
    };

    setSeverityDistribution(
      Object.entries(severityCounts).map(([severity, count]) => ({
        name: severity.charAt(0).toUpperCase() + severity.slice(1),
        value: count,
        color: severityColors[severity] || colors.info
      }))
    );

    // Generate attack types data
    const eventTypes = logs.reduce((acc, log) => {
      acc[log.event_type] = (acc[log.event_type] || 0) + 1;
      return acc;
    }, {});

    setAttackTypes(
      Object.entries(eventTypes)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 8)
        .map(([type, count]) => ({
          name: type.replace(/([A-Z])/g, ' $1').trim(),
          count,
          percentage: ((count / logs.length) * 100).toFixed(1)
        }))
    );

    // Generate timeline data
    const timelineData = logs
      .slice(0, 20)
      .reverse()
      .map((log, index) => ({
        time: new Date(log.timestamp).toLocaleTimeString(),
        threats: Math.floor(Math.random() * 10) + 1,
        blocked: Math.floor(Math.random() * 8),
        severity: log.severity === 'critical' ? 10 : log.severity === 'high' ? 7 : log.severity === 'medium' ? 4 : 2
      }));

    setTimeline(timelineData);

    // Generate threat trends
    const trendData = Array.from({length: 24}, (_, i) => ({
      hour: `${23 - i}:00`,
      threats: Math.floor(Math.random() * 50) + 10,
      blocked: Math.floor(Math.random() * 30) + 5,
      resolved: Math.floor(Math.random() * 40) + 15
    })).reverse();

    setThreatTrends(trendData);
  };

  const MetricCard = ({ title, value, change, icon, color, subtitle }) => (
    <div className="bg-bg-secondary border border-border-primary rounded-xl p-6 hover:border-border-accent transition-all duration-300 shadow-lg hover:shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-lg bg-opacity-20`} style={{backgroundColor: color + '33'}}>
          {React.cloneElement(icon, { className: "w-6 h-6", style: { color } })}
        </div>
        {change && (
          <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${
            change > 0 ? 'bg-success bg-opacity-20 text-success' : 'bg-danger bg-opacity-20 text-danger'
          }`}>
            {change > 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
            {Math.abs(change)}%
          </div>
        )}
      </div>
      <h3 className="text-sm font-medium text-text-muted mb-1">{title}</h3>
      <div className="text-2xl font-bold text-text-primary mb-1">{value}</div>
      {subtitle && <p className="text-xs text-text-muted">{subtitle}</p>}
    </div>
  );

  const ThreatIndicator = ({ level, description }) => {
    const getColor = () => {
      switch(level) {
        case 'critical': return colors.danger;
        case 'high': return colors.warning;
        case 'medium': return colors.info;
        default: return colors.success;
      }
    };

    return (
      <div className="flex items-center gap-3 p-4 bg-bg-tertiary rounded-lg border border-border-primary">
        <div className={`w-3 h-3 rounded-full animate-pulse`} style={{backgroundColor: getColor()}}></div>
        <div>
          <div className="font-medium text-text-primary capitalize">{level} Threat Level</div>
          <div className="text-sm text-text-muted">{description}</div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header with Real-time Status */}
      <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-text-primary">Security Operations Center</h1>
            <p className="text-text-muted">Real-time threat monitoring and analysis</p>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-success bg-opacity-20 text-success rounded-full border border-success border-opacity-30">
            <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
            <span className="text-sm font-medium">System Operational</span>
          </div>
        </div>

        {/* Real-time Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <MetricCard
            title="Active Threats"
            value={realTimeMetrics.activeThreats}
            change={-12}
            icon={<AlertTriangle />}
            color={colors.danger}
            subtitle="Actively monitored"
          />
          <MetricCard
            title="Blocked Attacks"
            value={realTimeMetrics.blockedAttacks.toLocaleString()}
            change={25}
            icon={<Shield />}
            color={colors.success}
            subtitle="Last 24 hours"
          />
          <MetricCard
            title="System Health"
            value={`${realTimeMetrics.systemHealth.toFixed(1)}%`}
            change={3}
            icon={<Activity />}
            color={colors.primary}
            subtitle="All systems operational"
          />
          <MetricCard
            title="Response Time"
            value={`${realTimeMetrics.responseTime.toFixed(2)}s`}
            change={-8}
            icon={<Zap />}
            color={colors.warning}
            subtitle="Average detection time"
          />
        </div>
      </div>

      {/* Threat Intelligence Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Real-time Threat Timeline */}
        <div className="lg:col-span-2 bg-bg-secondary border border-border-primary rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-text-primary">Threat Activity Timeline</h3>
            <div className="flex items-center gap-2 text-sm text-text-muted">
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full" style={{backgroundColor: colors.danger}}></div>
                <span>Critical</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full" style={{backgroundColor: colors.primary}}></div>
                <span>Blocked</span>
              </div>
            </div>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={timeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" strokeOpacity={0.3} />
                <XAxis 
                  dataKey="time" 
                  stroke="#9CA3AF" 
                  fontSize={12}
                  tickLine={false}
                />
                <YAxis 
                  stroke="#9CA3AF" 
                  fontSize={12}
                  tickLine={false}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#F3F4F6'
                  }}
                />
                <defs>
                  <linearGradient id="threatsGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={colors.danger} stopOpacity={0.8}/>
                    <stop offset="95%" stopColor={colors.danger} stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="blockedGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={colors.primary} stopOpacity={0.8}/>
                    <stop offset="95%" stopColor={colors.primary} stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <Area
                  type="monotone"
                  dataKey="threats"
                  stroke={colors.danger}
                  strokeWidth={2}
                  fill="url(#threatsGradient)"
                />
                <Area
                  type="monotone"
                  dataKey="blocked"
                  stroke={colors.primary}
                  strokeWidth={2}
                  fill="url(#blockedGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Threat Level Indicators */}
        <div className="space-y-4">
          <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
            <h3 className="text-lg font-semibold text-text-primary mb-4">Current Threat Level</h3>
            <ThreatIndicator 
              level={analysis?.severity_classification || 'medium'} 
              description="Based on recent activity analysis"
            />
          </div>

          {/* Quick Stats */}
          <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
            <h3 className="text-lg font-semibold text-text-primary mb-4">Security Overview</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-text-muted">Total Events</span>
                <span className="font-semibold text-text-primary">{logs?.length || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-text-muted">Critical Alerts</span>
                <span className="font-semibold text-danger">
                  {logs?.filter(log => log.severity === 'critical').length || 0}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-text-muted">Systems Monitored</span>
                <span className="font-semibold text-text-primary">247</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-text-muted">Response Teams</span>
                <span className="font-semibold text-success">4 Active</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Attack Types and Severity Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Attack Types Distribution */}
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-6">Top Attack Vectors</h3>
          <div className="space-y-4">
            {attackTypes.map((attack, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-bg-tertiary rounded-lg border border-border-primary hover:border-border-accent transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-cyber-primary bg-opacity-20 flex items-center justify-center text-cyber-primary font-semibold text-sm">
                    {index + 1}
                  </div>
                  <div>
                    <div className="font-medium text-text-primary">{attack.name}</div>
                    <div className="text-sm text-text-muted">{attack.count} incidents</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-text-primary">{attack.percentage}%</div>
                  <div className="text-sm text-text-muted">of total</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Severity Distribution Pie Chart */}
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-6">Severity Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={severityDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {severityDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#F3F4F6'
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-4 mt-4">
            {severityDistribution.map((item, index) => (
              <div key={index} className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{backgroundColor: item.color}}></div>
                <span className="text-sm text-text-muted">{item.name}: {item.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 24-Hour Trend Analysis */}
      <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-text-primary">24-Hour Security Trends</h3>
          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{backgroundColor: colors.danger}}></div>
              <span className="text-text-muted">Threats Detected</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{backgroundColor: colors.primary}}></div>
              <span className="text-text-muted">Attacks Blocked</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{backgroundColor: colors.success}}></div>
              <span className="text-text-muted">Issues Resolved</span>
            </div>
          </div>
        </div>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={threatTrends}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" strokeOpacity={0.3} />
              <XAxis 
                dataKey="hour" 
                stroke="#9CA3AF" 
                fontSize={12}
                tickLine={false}
              />
              <YAxis 
                stroke="#9CA3AF" 
                fontSize={12}
                tickLine={false}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#1F2937',
                  border: '1px solid #374151',
                  borderRadius: '8px',
                  color: '#F3F4F6'
                }}
              />
              <Line
                type="monotone"
                dataKey="threats"
                stroke={colors.danger}
                strokeWidth={3}
                dot={{ fill: colors.danger, strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6 }}
              />
              <Line
                type="monotone"
                dataKey="blocked"
                stroke={colors.primary}
                strokeWidth={3}
                dot={{ fill: colors.primary, strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6 }}
              />
              <Line
                type="monotone"
                dataKey="resolved"
                stroke={colors.success}
                strokeWidth={3}
                dot={{ fill: colors.success, strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AdvancedDashboard;
