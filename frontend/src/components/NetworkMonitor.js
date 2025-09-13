import React, { useState, useEffect, useRef } from 'react';
import { Wifi, Server, Shield, AlertTriangle, Activity, Globe, Network, Zap, Eye, Lock } from 'lucide-react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const NetworkMonitor = ({ logs }) => {
  const [networkData, setNetworkData] = useState([]);
  const [activeConnections, setActiveConnections] = useState(0);
  const [throughput, setThroughput] = useState({ in: 0, out: 0 });
  const [securityStatus, setSecurityStatus] = useState('secure');
  const [blockedIPs, setBlockedIPs] = useState([]);
  const [topTalkers, setTopTalkers] = useState([]);
  const [protocolStats, setProtocolStats] = useState({});
  const [networkAlerts, setNetworkAlerts] = useState([]);
  const [trafficFlow, setTrafficFlow] = useState([]);
  const canvasRef = useRef(null);
  const animationRef = useRef();

  // Simulate real-time network data
  useEffect(() => {
    const interval = setInterval(() => {
      generateNetworkData();
    }, 2000);

    // Start network visualization
    startNetworkVisualization();

    return () => {
      clearInterval(interval);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  const generateNetworkData = () => {
    const now = new Date();
    const timestamp = now.toLocaleTimeString();

    // Generate realistic network metrics
    const baseTraffic = 100 + Math.sin(Date.now() / 10000) * 50;
    const inTraffic = baseTraffic + Math.random() * 200;
    const outTraffic = baseTraffic * 0.8 + Math.random() * 150;

    setThroughput({
      in: Math.round(inTraffic * 10) / 10,
      out: Math.round(outTraffic * 10) / 10
    });

    setActiveConnections(450 + Math.floor(Math.random() * 100));

    // Update traffic flow data
    setTrafficFlow(prev => {
      const newData = {
        time: timestamp,
        inbound: inTraffic,
        outbound: outTraffic,
        total: inTraffic + outTraffic
      };
      return [...prev.slice(-19), newData];
    });

    // Generate network data points
    setNetworkData(prev => {
      const newPoint = {
        time: timestamp,
        latency: 15 + Math.random() * 30,
        packetLoss: Math.random() * 2,
        bandwidth: 85 + Math.random() * 15
      };
      return [...prev.slice(-29), newPoint];
    });

    // Update top talkers
    if (logs && logs.length > 0) {
      const ipCounts = {};
      logs.slice(0, 50).forEach(log => {
        ipCounts[log.source_ip] = (ipCounts[log.source_ip] || 0) + 1;
      });

      const talkers = Object.entries(ipCounts)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 10)
        .map(([ip, count], index) => ({
          ip,
          requests: count,
          bytes: Math.floor(count * 1024 * (1 + Math.random())),
          status: Math.random() > 0.8 ? 'suspicious' : 'normal',
          country: ['US', 'CN', 'RU', 'DE', 'UK', 'FR', 'JP', 'AU'][index % 8]
        }));

      setTopTalkers(talkers);

      // Generate blocked IPs
      const suspicious = talkers.filter(t => t.status === 'suspicious');
      setBlockedIPs(suspicious.map(t => ({
        ip: t.ip,
        reason: 'Multiple failed attempts',
        timestamp: new Date().toLocaleTimeString(),
        severity: 'high'
      })));
    }

    // Update protocol statistics
    setProtocolStats({
      HTTP: 35 + Math.random() * 20,
      HTTPS: 40 + Math.random() * 15,
      TCP: 15 + Math.random() * 10,
      UDP: 8 + Math.random() * 5,
      Other: 2 + Math.random() * 3
    });

    // Generate network alerts
    if (Math.random() > 0.7) {
      const alertTypes = [
        'Unusual traffic spike detected',
        'Potential DDoS activity',
        'Suspicious connection pattern',
        'High latency detected',
        'Port scan activity'
      ];
      
      const newAlert = {
        id: Date.now(),
        message: alertTypes[Math.floor(Math.random() * alertTypes.length)],
        severity: Math.random() > 0.6 ? 'high' : 'medium',
        timestamp: new Date().toLocaleTimeString()
      };

      setNetworkAlerts(prev => [newAlert, ...prev.slice(0, 4)]);
    }

    // Update security status
    const riskFactors = [
      inTraffic > 300,
      outTraffic > 250,
      blockedIPs.length > 3,
      Math.random() > 0.9
    ];

    const riskCount = riskFactors.filter(Boolean).length;
    setSecurityStatus(riskCount > 2 ? 'critical' : riskCount > 1 ? 'warning' : 'secure');
  };

  const startNetworkVisualization = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    const nodes = [];
    const connections = [];

    // Create network nodes
    for (let i = 0; i < 50; i++) {
      nodes.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        size: 2 + Math.random() * 4,
        type: Math.random() > 0.8 ? 'server' : 'client',
        active: Math.random() > 0.3
      });
    }

    // Create connections
    for (let i = 0; i < 30; i++) {
      connections.push({
        from: Math.floor(Math.random() * nodes.length),
        to: Math.floor(Math.random() * nodes.length),
        strength: Math.random(),
        active: Math.random() > 0.5
      });
    }

    const animate = () => {
      ctx.fillStyle = '#0F172A';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw connections
      connections.forEach(conn => {
        if (conn.from !== conn.to) {
          const fromNode = nodes[conn.from];
          const toNode = nodes[conn.to];
          
          ctx.beginPath();
          ctx.strokeStyle = conn.active ? 
            `rgba(0, 217, 255, ${0.1 + conn.strength * 0.3})` : 
            `rgba(139, 139, 255, ${0.05 + conn.strength * 0.1})`;
          ctx.lineWidth = conn.strength * 2;
          ctx.moveTo(fromNode.x, fromNode.y);
          ctx.lineTo(toNode.x, toNode.y);
          ctx.stroke();

          // Animate data packets
          if (conn.active && Math.random() > 0.98) {
            const progress = Math.random();
            const packetX = fromNode.x + (toNode.x - fromNode.x) * progress;
            const packetY = fromNode.y + (toNode.y - fromNode.y) * progress;
            
            ctx.beginPath();
            ctx.fillStyle = '#00FF88';
            ctx.arc(packetX, packetY, 2, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      });

      // Draw nodes
      nodes.forEach(node => {
        // Update position
        node.x += node.vx;
        node.y += node.vy;

        // Bounce off edges
        if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
        if (node.y < 0 || node.y > canvas.height) node.vy *= -1;

        // Keep in bounds
        node.x = Math.max(0, Math.min(canvas.width, node.x));
        node.y = Math.max(0, Math.min(canvas.height, node.y));

        // Draw node
        ctx.beginPath();
        if (node.type === 'server') {
          ctx.fillStyle = node.active ? '#FF4444' : '#666666';
          ctx.arc(node.x, node.y, node.size + 2, 0, Math.PI * 2);
          ctx.fill();
          
          // Server halo
          if (node.active) {
            ctx.beginPath();
            ctx.strokeStyle = 'rgba(255, 68, 68, 0.3)';
            ctx.arc(node.x, node.y, node.size + 8, 0, Math.PI * 2);
            ctx.stroke();
          }
        } else {
          ctx.fillStyle = node.active ? '#00D9FF' : '#444444';
          ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2);
          ctx.fill();
        }
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'critical': return 'text-red-400';
      case 'warning': return 'text-yellow-400';
      case 'secure': return 'text-green-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'critical': return <AlertTriangle className="w-5 h-5 text-red-400" />;
      case 'warning': return <AlertTriangle className="w-5 h-5 text-yellow-400" />;
      case 'secure': return <Shield className="w-5 h-5 text-green-400" />;
      default: return <Activity className="w-5 h-5 text-gray-400" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Network Status Header */}
      <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-cyber-primary bg-opacity-20 rounded-lg">
              <Network className="w-6 h-6 text-cyber-primary" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-text-primary">Real-time Network Monitor</h2>
              <p className="text-text-muted">Live network traffic analysis and security monitoring</p>
            </div>
          </div>
          <div className={`flex items-center gap-2 px-4 py-2 rounded-full border ${
            securityStatus === 'secure' ? 'bg-green-500 bg-opacity-20 text-green-400 border-green-500 border-opacity-30' :
            securityStatus === 'warning' ? 'bg-yellow-500 bg-opacity-20 text-yellow-400 border-yellow-500 border-opacity-30' :
            'bg-red-500 bg-opacity-20 text-red-400 border-red-500 border-opacity-30'
          }`}>
            {getStatusIcon(securityStatus)}
            <span className="text-sm font-medium capitalize">{securityStatus}</span>
          </div>
        </div>

        {/* Real-time Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-bg-tertiary p-4 rounded-lg border border-border-primary">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-5 h-5 text-blue-400" />
              <span className="text-sm font-medium text-text-muted">Active Connections</span>
            </div>
            <div className="text-2xl font-bold text-text-primary">{activeConnections.toLocaleString()}</div>
            <div className="text-xs text-text-muted">Currently active</div>
          </div>

          <div className="bg-bg-tertiary p-4 rounded-lg border border-border-primary">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="w-5 h-5 text-green-400" />
              <span className="text-sm font-medium text-text-muted">Inbound Traffic</span>
            </div>
            <div className="text-2xl font-bold text-text-primary">{throughput.in} Mbps</div>
            <div className="text-xs text-text-muted">Current rate</div>
          </div>

          <div className="bg-bg-tertiary p-4 rounded-lg border border-border-primary">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="w-5 h-5 text-orange-400" />
              <span className="text-sm font-medium text-text-muted">Outbound Traffic</span>
            </div>
            <div className="text-2xl font-bold text-text-primary">{throughput.out} Mbps</div>
            <div className="text-xs text-text-muted">Current rate</div>
          </div>

          <div className="bg-bg-tertiary p-4 rounded-lg border border-border-primary">
            <div className="flex items-center gap-2 mb-2">
              <Lock className="w-5 h-5 text-red-400" />
              <span className="text-sm font-medium text-text-muted">Blocked IPs</span>
            </div>
            <div className="text-2xl font-bold text-text-primary">{blockedIPs.length}</div>
            <div className="text-xs text-text-muted">Actively blocked</div>
          </div>
        </div>
      </div>

      {/* Network Visualization and Traffic Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Network Topology Visualization */}
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-4">Network Topology</h3>
          <div className="relative">
            <canvas
              ref={canvasRef}
              className="w-full h-80 rounded-lg border border-border-primary"
              style={{ background: '#0F172A' }}
            />
            <div className="absolute top-4 left-4 bg-black bg-opacity-50 rounded-lg p-3 text-xs">
              <div className="flex items-center gap-2 mb-1">
                <div className="w-2 h-2 bg-red-400 rounded-full"></div>
                <span className="text-gray-300">Servers</span>
              </div>
              <div className="flex items-center gap-2 mb-1">
                <div className="w-2 h-2 bg-cyan-400 rounded-full"></div>
                <span className="text-gray-300">Clients</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span className="text-gray-300">Data Packets</span>
              </div>
            </div>
          </div>
        </div>

        {/* Traffic Flow Chart */}
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-4">Traffic Flow Analysis</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trafficFlow}>
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
                  <linearGradient id="inboundGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00FF88" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#00FF88" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="outboundGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#FFB800" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#FFB800" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <Area
                  type="monotone"
                  dataKey="inbound"
                  stackId="1"
                  stroke="#00FF88"
                  fill="url(#inboundGradient)"
                />
                <Area
                  type="monotone"
                  dataKey="outbound"
                  stackId="2"
                  stroke="#FFB800"
                  fill="url(#outboundGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Network Performance Metrics */}
      <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
        <h3 className="text-lg font-semibold text-text-primary mb-4">Network Performance</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={networkData}>
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
              <Line
                type="monotone"
                dataKey="latency"
                stroke="#00D9FF"
                strokeWidth={2}
                name="Latency (ms)"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="packetLoss"
                stroke="#FF4444"
                strokeWidth={2}
                name="Packet Loss (%)"
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="bandwidth"
                stroke="#00FF88"
                strokeWidth={2}
                name="Bandwidth (%)"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Network Intelligence */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top Talkers */}
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-4">Top Talkers</h3>
          <div className="space-y-3 max-h-80 overflow-y-auto">
            {topTalkers.map((talker, index) => (
              <div key={index} className={`flex items-center justify-between p-3 rounded-lg border ${
                talker.status === 'suspicious' 
                  ? 'bg-red-500 bg-opacity-10 border-red-500 border-opacity-30' 
                  : 'bg-bg-tertiary border-border-primary'
              }`}>
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold ${
                    talker.status === 'suspicious' ? 'bg-red-500 text-white' : 'bg-blue-500 text-white'
                  }`}>
                    {talker.country}
                  </div>
                  <div>
                    <div className="font-mono text-sm text-text-primary">{talker.ip}</div>
                    <div className="text-xs text-text-muted">{talker.requests} requests</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-text-primary">
                    {(talker.bytes / 1024).toFixed(1)}KB
                  </div>
                  {talker.status === 'suspicious' && (
                    <div className="text-xs text-red-400">Suspicious</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Protocol Statistics */}
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-4">Protocol Distribution</h3>
          <div className="space-y-4">
            {Object.entries(protocolStats).map(([protocol, percentage]) => (
              <div key={protocol} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-text-primary font-medium">{protocol}</span>
                  <span className="text-text-muted">{percentage.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-bg-tertiary rounded-full h-2">
                  <div
                    className="bg-cyber-primary h-2 rounded-full transition-all duration-500"
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Network Alerts */}
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-4">Network Alerts</h3>
          <div className="space-y-3 max-h-80 overflow-y-auto">
            {networkAlerts.length === 0 ? (
              <div className="text-center py-8 text-text-muted">
                <Eye className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>No alerts detected</p>
              </div>
            ) : (
              networkAlerts.map((alert) => (
                <div key={alert.id} className={`p-3 rounded-lg border ${
                  alert.severity === 'high'
                    ? 'bg-red-500 bg-opacity-10 border-red-500 border-opacity-30'
                    : 'bg-yellow-500 bg-opacity-10 border-yellow-500 border-opacity-30'
                }`}>
                  <div className="flex items-start justify-between mb-2">
                    <AlertTriangle className={`w-4 h-4 mt-0.5 ${
                      alert.severity === 'high' ? 'text-red-400' : 'text-yellow-400'
                    }`} />
                    <span className="text-xs text-text-muted">{alert.timestamp}</span>
                  </div>
                  <p className="text-sm text-text-primary">{alert.message}</p>
                  <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium mt-2 ${
                    alert.severity === 'high'
                      ? 'bg-red-500 bg-opacity-20 text-red-400'
                      : 'bg-yellow-500 bg-opacity-20 text-yellow-400'
                  }`}>
                    {alert.severity.toUpperCase()}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Blocked IPs */}
      {blockedIPs.length > 0 && (
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-4">Recently Blocked IPs</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {blockedIPs.map((blockedIP, index) => (
              <div key={index} className="bg-red-500 bg-opacity-10 border border-red-500 border-opacity-30 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Lock className="w-4 h-4 text-red-400" />
                  <span className="font-mono text-sm text-text-primary">{blockedIP.ip}</span>
                </div>
                <p className="text-xs text-text-muted mb-1">{blockedIP.reason}</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-red-400">BLOCKED</span>
                  <span className="text-xs text-text-muted">{blockedIP.timestamp}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default NetworkMonitor;
