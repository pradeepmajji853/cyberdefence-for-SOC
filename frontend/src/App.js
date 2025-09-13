import React, { useState, useEffect, useRef } from 'react';
import { 
  Shield, 
  AlertTriangle, 
  Activity, 
  MessageSquare, 
  RefreshCw,
  Eye,
  Ban,
  Zap,
  TrendingUp,
  Users,
  AlertCircle,
  Info,
  Search,
  Filter,
  XCircle,
  Globe,
  MapPin,
  Target,
  Settings
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import api from './api';

// Import new components
import AttackSimulator from './components/AttackSimulator';
import ThreatIntelligence from './components/ThreatIntelligence';
import AttackMap from './components/AttackMap';
import AutomatedActions from './components/AutomatedActions';
import AnomalyDetection from './components/AnomalyDetection';
import EnhancedChat from './components/EnhancedChat';
import ThreatLevelGauge from './components/ThreatLevelGauge';

function App() {
  const [logs, setLogs] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedTab, setSelectedTab] = useState('dashboard');
  const [analysisResponse, setAnalysisResponse] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const chatContainerRef = useRef(null);

  // New state for enhanced features
  const [threatIntelligence, setThreatIntelligence] = useState(null);
  const [attackMapData, setAttackMapData] = useState(null);
  const [anomalyData, setAnomalyData] = useState(null);
  const [simulationResult, setSimulationResult] = useState(null);

  // Fetch data functions
  const fetchLogs = async () => {
    try {
      console.log('Fetching logs...');
      const data = await api.getLogs({ limit: 100 }); // Increased limit to show more logs
      console.log('Logs received:', data?.length);
      setLogs(data);
    } catch (error) {
      console.error('Failed to fetch logs:', error);
    }
  };

  const fetchAnalysis = async () => {
    try {
      console.log('Fetching analysis...');
      const data = await api.getAnalysis(24); // Look back 24 hours instead of 2
      console.log('Analysis received:', data);
      setAnalysis(data);
    } catch (error) {
      console.error('Failed to fetch analysis:', error);
    }
  };

  const fetchStats = async () => {
    try {
      console.log('Fetching stats...');
      const data = await api.getStats();
      console.log('Stats received:', data);
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  // New fetch functions for enhanced features
  const fetchThreatIntelligence = async () => {
    try {
      const data = await api.getThreatIntelligence();
      setThreatIntelligence(data);
    } catch (error) {
      console.error('Failed to fetch threat intelligence:', error);
    }
  };

  const fetchAttackMapData = async () => {
    try {
      const data = await api.getAttackMapData();
      setAttackMapData(data);
    } catch (error) {
      console.error('Failed to fetch attack map data:', error);
    }
  };

  const fetchAnomalyData = async () => {
    try {
      const data = await api.getAnomalyDetection();
      setAnomalyData(data);
    } catch (error) {
      console.error('Failed to fetch anomaly data:', error);
    }
  };

  const handleSimulateAttack = async (attackType) => {
    try {
      const result = await api.simulateAttack(attackType);
      setSimulationResult(result);
      // Refresh data after simulation
      await fetchLogs();
      await fetchStats();
    } catch (error) {
      console.error('Failed to simulate attack:', error);
      throw error;
    }
  };

  const handleExecuteAction = async (action, target) => {
    try {
      const result = await api.executeAction(action, target);
      return result;
    } catch (error) {
      console.error('Failed to execute action:', error);
      throw error;
    }
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim()) return;
    
    const userMessage = { type: 'user', content: currentMessage };
    setChatHistory(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setLoading(true);

    try {
      const response = await api.chat(currentMessage);
      const aiMessage = { type: 'ai', content: response.answer };
      setChatHistory(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = { type: 'ai', content: 'Sorry, I encountered an error. Please try again.' };
      setChatHistory(prev => [...prev, errorMessage]);
    }
    setLoading(false);
  };

  // Security action handlers
  const handleQuickAction = async (action, data = null) => {
    setAnalysisLoading(true);
    setAnalysisResponse(null);
    
    let message = '';
    
    try {
      switch (action) {
        case 'block_ip':
          message = 'WHAT ARE THE IPS THAT ARE NEEDED TO BE BLOCKED';
          break;
        case 'isolate_host':
          message = 'What hosts need to be isolated immediately?';
          break;
        case 'escalate':
          message = 'What critical incidents need immediate escalation?';
          break;
        case 'monitor':
          message = 'What systems require enhanced monitoring?';
          break;
        case 'execute_recommendation':
          message = `Execute this recommendation: ${data}. Provide specific steps.`;
          break;
        default:
          message = `Analyze security action: ${action}`;
      }
      
      // Send query directly to AI for analysis response (not chat)
      const response = await api.chat(message);
      
      setAnalysisResponse({
        action: action,
        query: message,
        response: response.answer,
        timestamp: new Date().toISOString()
      });
      
    } catch (error) {
      console.error('Failed to execute action:', error);
      setAnalysisResponse({
        action: action,
        query: message,
        response: 'Error: Unable to process the security action. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      });
    }
    setAnalysisLoading(false);
  };

  // Auto-refresh effect
  useEffect(() => {
    // Initial fetch
    fetchLogs();
    fetchAnalysis();
    fetchStats();
    fetchThreatIntelligence();
    fetchAttackMapData();
    fetchAnomalyData();

    if (autoRefresh) {
      const interval = setInterval(() => {
        fetchLogs();
        fetchAnalysis();
        fetchStats();
        fetchThreatIntelligence();
        fetchAttackMapData();
        fetchAnomalyData();
      }, 10000); // Refresh every 10 seconds
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  // Auto-scroll chat
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return 'bg-cyber-danger text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-cyber-warning text-white';
      case 'low': return 'bg-cyber-success text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return <XCircle className="h-4 w-4" />;
      case 'high': return <AlertTriangle className="h-4 w-4" />;
      case 'medium': return <AlertCircle className="h-4 w-4" />;
      case 'low': return <Info className="h-4 w-4" />;
      default: return <Info className="h-4 w-4" />;
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  // Generate chart data from logs
  const generateChartData = () => {
    if (!logs.length) return [];
    
    const hourlyData = {};
    logs.forEach(log => {
      const hour = new Date(log.timestamp).toISOString().slice(0, 13) + ':00:00Z';
      if (!hourlyData[hour]) {
        hourlyData[hour] = { time: hour, count: 0 };
      }
      hourlyData[hour].count++;
    });

    return Object.values(hourlyData).sort((a, b) => new Date(a.time) - new Date(b.time));
  };

  const StatCard = ({ icon, title, value, subtitle, color = "cyber-primary" }) => (
    <div className="bg-bg-secondary border border-border-primary rounded-lg p-4 hover:border-border-accent transition-colors">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-text-muted text-sm font-medium">{title}</p>
          <p className={`text-2xl font-bold text-${color}`}>{value}</p>
          {subtitle && <p className="text-text-secondary text-xs mt-1">{subtitle}</p>}
        </div>
        <div className={`text-${color} opacity-75`}>
          {icon}
        </div>
      </div>
    </div>
  );

  const LogCard = ({ log, index }) => (
    <div className="bg-bg-secondary border border-border-primary rounded-lg p-4 hover:border-border-accent transition-colors">
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center space-x-2">
          {getSeverityIcon(log.severity)}
          <span className={`px-2 py-1 rounded text-xs font-semibold ${getSeverityColor(log.severity)}`}>
            {log.severity?.toUpperCase()}
          </span>
        </div>
        <span className="text-text-muted text-xs">
          {formatTimestamp(log.timestamp)}
        </span>
      </div>
      <h4 className="text-text-accent font-medium text-sm mb-2">{log.event_type}</h4>
      <div className="text-text-secondary text-sm mb-2">
        <span className="font-medium">Source:</span> {log.source_ip} 
        <span className="mx-2">→</span>
        <span className="font-medium">Dest:</span> {log.dest_ip}
      </div>
      <p className="text-text-muted text-xs line-clamp-2">{log.message}</p>
    </div>
  );

  const handleGenerateLog = async () => {
    setLoading(true);
    try {
      // More realistic log generation with varied scenarios
      const logTemplates = [
        {
          event_type: 'Malware Detection',
          severity: 'critical',
          message_templates: [
            'Trojan.Win32.Agent detected in email attachment. Immediate quarantine initiated.',
            'Advanced persistent threat signature detected. C2 communication blocked.',
            'Ransomware activity detected. File encryption prevented by endpoint protection.',
            'Zero-day exploit attempt blocked by behavioral analysis system.'
          ]
        },
        {
          event_type: 'Unauthorized Access Attempt',
          severity: 'high',
          message_templates: [
            'Multiple failed authentication attempts from foreign IP address.',
            'Privilege escalation attempt detected on critical server.',
            'Suspicious login pattern indicates potential account compromise.',
            'Administrative account accessed from unauthorized location.'
          ]
        },
        {
          event_type: 'Network Intrusion',
          severity: 'high',
          message_templates: [
            'Port scanning activity detected from external source.',
            'Suspicious network traffic patterns indicate reconnaissance.',
            'Unauthorized network mapping attempt blocked.',
            'Lateral movement detected across network segments.'
          ]
        },
        {
          event_type: 'Phishing Attempt',
          severity: 'medium',
          message_templates: [
            'Sophisticated spear-phishing email targeting military personnel.',
            'Credential harvesting website blocked by security filters.',
            'Social engineering attempt via fake military communication.',
            'Suspicious email with military-themed content intercepted.'
          ]
        },
        {
          event_type: 'Firewall Alert',
          severity: 'medium',
          message_templates: [
            'Blocked connection attempt to known malicious domain.',
            'Unusual outbound traffic to suspicious geographic location.',
            'Multiple connections blocked to blacklisted IP addresses.',
            'Protocol violation detected and connection terminated.'
          ]
        },
        {
          event_type: 'System Monitoring',
          severity: 'low',
          message_templates: [
            'Routine security scan completed successfully.',
            'System integrity check passed all validation tests.',
            'Automated backup completed without errors.',
            'Security patch installation completed successfully.'
          ]
        }
      ];

      const template = logTemplates[Math.floor(Math.random() * logTemplates.length)];
      const message = template.message_templates[Math.floor(Math.random() * template.message_templates.length)];
      
      // Generate more realistic IP addresses
      const externalIPs = ['203.0.113.45', '198.51.100.23', '93.184.216.34', '185.220.101.42', '172.16.254.78'];
      const internalIPs = ['192.168.1.100', '192.168.1.50', '192.168.1.205', '192.168.1.150', '192.168.1.75'];
      
      const isInbound = Math.random() > 0.5;
      const source_ip = isInbound 
        ? externalIPs[Math.floor(Math.random() * externalIPs.length)]
        : internalIPs[Math.floor(Math.random() * internalIPs.length)];
      const dest_ip = isInbound
        ? internalIPs[Math.floor(Math.random() * internalIPs.length)]
        : externalIPs[Math.floor(Math.random() * externalIPs.length)];

      const logEntry = {
        timestamp: new Date().toISOString(),
        source_ip: source_ip,
        dest_ip: dest_ip,
        event_type: template.event_type,
        severity: template.severity,
        message: message + ' [Generated for demonstration]'
      };

      await api.createLog(logEntry);
      await fetchLogs(); // Refresh logs
    } catch (error) {
      console.error('Failed to generate log:', error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-bg-primary text-text-primary">
      {/* Professional Header */}
      <header className="bg-bg-secondary border-b border-border-primary shadow-lg">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <Shield className="h-8 w-8 text-cyber-primary" />
                <div>
                  <h1 className="text-xl font-bold text-text-primary">
                    Cyber Defense Assistant
                  </h1>
                  <p className="text-text-muted text-sm">Military Security Operations Center</p>
                </div>
              </div>
            </div>              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 px-3 py-2 bg-bg-tertiary rounded-lg">
                  <div className="w-2 h-2 bg-cyber-success rounded-full animate-pulse"></div>
                  <span className="text-cyber-success text-sm font-medium">System Online</span>
                </div>
                
                {analysis && (
                  <div className="flex items-center space-x-2 px-3 py-2 bg-bg-tertiary rounded-lg">
                    <div className={`w-2 h-2 rounded-full ${
                      analysis.severity_classification === 'critical' ? 'bg-cyber-danger animate-pulse' :
                      analysis.severity_classification === 'high' ? 'bg-cyber-warning animate-pulse' :
                      analysis.severity_classification === 'medium' ? 'bg-cyber-accent' :
                      'bg-cyber-success'
                    }`}></div>
                    <span className={`text-sm font-medium ${
                      analysis.severity_classification === 'critical' ? 'text-cyber-danger' :
                      analysis.severity_classification === 'high' ? 'text-cyber-warning' :
                      analysis.severity_classification === 'medium' ? 'text-cyber-accent' :
                      'text-cyber-success'
                    }`}>
                      Threat Level: {analysis.severity_classification?.toUpperCase()}
                    </span>
                  </div>
                )}
                
                <button
                  onClick={() => setAutoRefresh(!autoRefresh)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                    autoRefresh 
                      ? 'bg-cyber-primary text-white' 
                      : 'bg-bg-tertiary text-text-secondary hover:bg-bg-hover'
                  }`}
                >
                  <RefreshCw className={`h-4 w-4 ${autoRefresh ? 'animate-spin' : ''}`} />
                  <span className="text-sm">Auto Refresh</span>
                </button>
              </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-bg-secondary border-b border-border-primary px-6">
        <div className="flex space-x-6 overflow-x-auto">
          {[
            { id: 'dashboard', label: 'Dashboard', icon: Activity },
            { id: 'simulation', label: 'Attack Simulation', icon: Target },
            { id: 'intelligence', label: 'Threat Intel', icon: Globe },
            { id: 'map', label: 'Attack Map', icon: MapPin },
            { id: 'actions', label: 'Auto Actions', icon: Settings },
            { id: 'anomalies', label: 'Anomalies', icon: AlertTriangle },
            { id: 'logs', label: 'Security Logs', icon: Eye },
            { id: 'analysis', label: 'AI Analysis', icon: Zap },
            { id: 'chat', label: 'AI Assistant', icon: MessageSquare }
          ].map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setSelectedTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-3 border-b-2 transition-colors whitespace-nowrap ${
                  selectedTab === tab.id
                    ? 'border-cyber-primary text-cyber-primary'
                    : 'border-transparent text-text-secondary hover:text-text-primary hover:border-border-secondary'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span className="text-sm font-medium">{tab.label}</span>
              </button>
            );
          })}
        </div>
      </nav>

      {/* Main Content */}
      <main className="p-6">
        {selectedTab === 'dashboard' && (
          <div className="space-y-6">
            {/* Stats Overview */}
            <div>
              <h2 className="text-lg font-semibold text-text-primary mb-4">Security Overview</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <StatCard
                  icon={<AlertTriangle className="h-6 w-6" />}
                  title="Total Threats"
                  value={logs.length}
                  subtitle="Last 24 hours"
                  color="cyber-danger"
                />
                <StatCard
                  icon={<Shield className="h-6 w-6" />}
                  title="Critical Alerts"
                  value={stats?.last_24h_severity?.critical || 0}
                  subtitle="Requires attention"
                  color="cyber-danger"
                />
                <StatCard
                  icon={<Activity className="h-6 w-6" />}
                  title="Active Monitoring"
                  value="24/7"
                  subtitle="System status"
                  color="cyber-success"
                />
                <StatCard
                  icon={<Users className="h-6 w-6" />}
                  title="Unique IPs"
                  value={new Set(logs.map(log => log.source_ip)).size}
                  subtitle="Distinct sources"
                  color="cyber-primary"
                />
              </div>
            </div>

            {/* Charts and Threat Level */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Activity Timeline */}
              <div className="lg:col-span-2 bg-bg-secondary border border-border-primary rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-text-primary">Activity Timeline</h3>
                  <TrendingUp className="h-5 w-5 text-cyber-primary" />
                </div>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={generateChartData()}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis 
                        dataKey="time" 
                        tick={{fontSize: 12, fill: '#94a3b8'}} 
                        stroke="#94a3b8"
                        tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                      />
                      <YAxis tick={{fontSize: 12, fill: '#94a3b8'}} stroke="#94a3b8" />
                      <Tooltip 
                        contentStyle={{
                          backgroundColor: '#1e293b',
                          border: '1px solid #3b82f6',
                          borderRadius: '8px',
                          color: '#f8fafc'
                        }}
                      />
                      <Area 
                        type="monotone" 
                        dataKey="count" 
                        stroke="#3b82f6" 
                        fill="#3b82f6" 
                        fillOpacity={0.3}
                        strokeWidth={2}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Real-time Threat Level Gauge */}
              <div>
                <ThreatLevelGauge threatLevel="dynamic" stats={stats} />
              </div>
            </div>

            {/* Quick Actions Overview */}
            <div className="bg-bg-secondary border border-border-primary rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-text-primary">Quick Security Actions</h3>
                <Shield className="h-5 w-5 text-cyber-primary" />
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button 
                  onClick={() => setSelectedTab('simulation')}
                  className="flex flex-col items-center p-4 bg-red-50 hover:bg-red-100 rounded-lg transition-colors border border-red-200"
                >
                  <Target className="w-8 h-8 text-red-600 mb-2" />
                  <span className="text-sm font-medium text-red-800">Attack Simulation</span>
                </button>
                <button 
                  onClick={() => setSelectedTab('intelligence')}
                  className="flex flex-col items-center p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors border border-blue-200"
                >
                  <Globe className="w-8 h-8 text-blue-600 mb-2" />
                  <span className="text-sm font-medium text-blue-800">Threat Intelligence</span>
                </button>
                <button 
                  onClick={() => setSelectedTab('map')}
                  className="flex flex-col items-center p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors border border-green-200"
                >
                  <MapPin className="w-8 h-8 text-green-600 mb-2" />
                  <span className="text-sm font-medium text-green-800">Global Attack Map</span>
                </button>
                <button 
                  onClick={() => setSelectedTab('actions')}
                  className="flex flex-col items-center p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors border border-purple-200"
                >
                  <Settings className="w-8 h-8 text-purple-600 mb-2" />
                  <span className="text-sm font-medium text-purple-800">Auto Actions</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* NEW ENHANCED FEATURES */}
        {selectedTab === 'simulation' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <AttackSimulator 
                  onSimulateAttack={handleSimulateAttack} 
                  simulationResult={simulationResult}
                />
              </div>
              <div>
                <ThreatLevelGauge threatLevel="dynamic" stats={stats} />
              </div>
            </div>
          </div>
        )}

        {selectedTab === 'intelligence' && (
          <div className="space-y-6">
            <ThreatIntelligence threatData={threatIntelligence} />
          </div>
        )}

        {selectedTab === 'map' && (
          <div className="space-y-6">
            <AttackMap attackMapData={attackMapData} />
          </div>
        )}

        {selectedTab === 'actions' && (
          <div className="space-y-6">
            <AutomatedActions onExecuteAction={handleExecuteAction} />
          </div>
        )}

        {selectedTab === 'anomalies' && (
          <div className="space-y-6">
            <AnomalyDetection anomalyData={anomalyData} />
          </div>
        )}

        {selectedTab === 'logs' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-text-primary">Security Event Logs</h2>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Search className="h-4 w-4 text-text-muted" />
                  <input
                    type="text"
                    placeholder="Search logs..."
                    className="bg-bg-secondary border border-border-primary rounded-lg px-3 py-2 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:border-cyber-primary"
                  />
                </div>
                <button className="flex items-center space-x-2 px-4 py-2 bg-cyber-primary text-white rounded-lg hover:bg-blue-600 transition-colors">
                  <Filter className="h-4 w-4" />
                  <span className="text-sm">Filter</span>
                </button>
                <button
                  className="flex items-center space-x-2 px-4 py-2 bg-cyber-success text-white rounded-lg hover:bg-green-600 transition-colors"
                  onClick={handleGenerateLog}
                  disabled={loading}
                >
                  <Activity className="h-4 w-4" />
                  <span className="text-sm">Generate Log</span>
                </button>
              </div>
            </div>

            <div className="grid gap-4">
              {logs.map((log, index) => (
                <LogCard key={log.id || index} log={log} index={index} />
              ))}
              
              {logs.length === 0 && (
                <div className="bg-bg-secondary border border-border-primary rounded-lg p-8 text-center">
                  <Eye className="h-12 w-12 text-text-muted mx-auto mb-4" />
                  <p className="text-text-secondary">No security logs available</p>
                </div>
              )}
            </div>
          </div>
        )}

        {selectedTab === 'analysis' && (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold text-text-primary">AI Threat Analysis</h2>
            
            {analysis ? (
              <div className="grid gap-6">
                {/* Analysis Summary */}
                <div className="bg-bg-secondary border border-border-primary rounded-lg p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <Zap className="h-6 w-6 text-cyber-warning" />
                    <h3 className="text-lg font-semibold text-text-primary">Analysis Summary</h3>
                  </div>
                  <p className="text-text-secondary leading-relaxed">{analysis.summary}</p>
                </div>

                {/* Action Response Display */}
                {(analysisResponse || analysisLoading) && (
                  <div className="bg-bg-secondary border border-border-primary rounded-lg p-6">
                    <div className="flex items-center space-x-3 mb-4">
                      <MessageSquare className="h-6 w-6 text-cyber-primary" />
                      <h3 className="text-lg font-semibold text-text-primary">Action Response</h3>
                      {analysisLoading && (
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-cyber-primary"></div>
                      )}
                    </div>
                    
                    {analysisLoading ? (
                      <div className="flex items-center space-x-3 p-4 bg-bg-tertiary rounded-lg">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-cyber-primary"></div>
                        <p className="text-text-secondary">Processing security action...</p>
                      </div>
                    ) : analysisResponse && (
                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-3 bg-bg-tertiary rounded-lg">
                          <div className="flex items-center space-x-3">
                            <div className={`w-3 h-3 rounded-full ${
                              analysisResponse.isError ? 'bg-cyber-danger' : 'bg-cyber-success'
                            }`}></div>
                            <span className="text-text-primary font-medium">
                              {analysisResponse.action?.toUpperCase().replace('_', ' ')} ACTION
                            </span>
                          </div>
                          <span className="text-text-muted text-sm">
                            {new Date(analysisResponse.timestamp).toLocaleTimeString()}
                          </span>
                        </div>
                        
                        <div className={`p-4 rounded-lg border-l-4 ${
                          analysisResponse.isError 
                            ? 'bg-red-900/20 border-cyber-danger' 
                            : 'bg-blue-900/20 border-cyber-primary'
                        }`}>
                          <div className="space-y-3">
                            <div>
                              <p className="text-text-muted text-sm mb-2">Query:</p>
                              <p className="text-text-secondary text-sm font-medium">{analysisResponse.query}</p>
                            </div>
                            <div>
                              <p className="text-text-muted text-sm mb-2">Response:</p>
                              <div className="bg-bg-tertiary p-4 rounded-lg">
                                <pre className="text-text-secondary text-sm whitespace-pre-wrap font-mono leading-relaxed">
                                  {analysisResponse.response}
                                </pre>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <div className="flex justify-end">
                          <button
                            onClick={() => setAnalysisResponse(null)}
                            className="px-4 py-2 text-text-muted hover:text-text-primary transition-colors text-sm"
                          >
                            Clear Response
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Threats Identified */}
                <div className="bg-bg-secondary border border-border-primary rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-text-primary mb-4">Identified Threats</h3>
                  <div className="space-y-3">
                    {analysis.threats_identified.map((threat, i) => (
                      <div key={i} className="flex items-start space-x-3 p-3 bg-bg-tertiary rounded-lg">
                        <AlertTriangle className="h-5 w-5 text-cyber-danger mt-0.5 flex-shrink-0" />
                        <p className="text-text-secondary">{threat}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Recommendations */}
                <div className="bg-bg-secondary border border-border-primary rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-text-primary mb-4">Recommended Actions</h3>
                  <div className="space-y-3">
                    {analysis.recommendations?.map((rec, i) => (
                      <div key={i} className="flex items-center justify-between p-3 bg-bg-tertiary rounded-lg">
                        <p className="text-text-secondary flex-1">{rec}</p>
                        <button 
                          onClick={() => handleQuickAction('execute_recommendation', rec)}
                          disabled={analysisLoading}
                          className="ml-4 px-4 py-2 bg-cyber-success text-white rounded-lg hover:bg-green-600 transition-colors text-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                        >
                          <span>Execute</span>
                          {analysisLoading && (
                            <div className="animate-spin rounded-full h-3 w-3 border-2 border-white border-t-transparent"></div>
                          )}
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Quick Security Actions */}
                <div className="bg-bg-secondary border border-border-primary rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-text-primary mb-4">Quick Security Actions</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <button
                      onClick={() => handleQuickAction('block_ip')}
                      disabled={analysisLoading}
                      className="flex items-center justify-center space-x-2 px-4 py-3 bg-cyber-danger text-white rounded-lg hover:bg-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Ban className="h-4 w-4" />
                      <span>Block All IPs</span>
                      {analysisLoading && (
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                      )}
                    </button>
                    <button
                      onClick={() => handleQuickAction('isolate_host')}
                      disabled={analysisLoading}
                      className="flex items-center justify-center space-x-2 px-4 py-3 bg-cyber-warning text-white rounded-lg hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Shield className="h-4 w-4" />
                      <span>Isolate Hosts</span>
                    </button>
                    <button
                      onClick={() => handleQuickAction('escalate')}
                      disabled={analysisLoading}
                      className="flex items-center justify-center space-x-2 px-4 py-3 bg-cyber-primary text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <AlertTriangle className="h-4 w-4" />
                      <span>Escalate Incident</span>
                    </button>
                    <button
                      onClick={() => handleQuickAction('monitor')}
                      disabled={analysisLoading}
                      className="flex items-center justify-center space-x-2 px-4 py-3 bg-cyber-success text-white rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Activity className="h-4 w-4" />
                      <span>Enhanced Monitor</span>
                    </button>
                  </div>
                </div>

                {/* Overall Severity */}
                <div className="bg-bg-secondary border border-border-primary rounded-lg p-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-text-primary">Overall Risk Assessment</h3>
                    <div className="flex items-center space-x-2">
                      {getSeverityIcon(analysis.severity_classification)}
                      <span className={`px-3 py-1 rounded-lg font-semibold ${getSeverityColor(analysis.severity_classification)}`}>
                        {analysis.severity_classification?.toUpperCase()}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-bg-secondary border border-border-primary rounded-lg p-8 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-cyber-primary mx-auto mb-4"></div>
                <p className="text-text-secondary">Analyzing security data...</p>
              </div>
            )}
          </div>
        )}

        {selectedTab === 'chat' && (
          <div className="space-y-6">
            <EnhancedChat 
              onSendMessage={handleSendMessage}
              chatHistory={chatHistory}
              loading={loading}
            />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
