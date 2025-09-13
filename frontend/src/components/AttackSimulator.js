import React, { useState, useEffect } from 'react';
import { Zap, Target, Play, CheckCircle, Clock, Users, Database, Lock, Activity, Wifi, Server, Eye } from 'lucide-react';

const AttackSimulator = ({ onSimulateAttack, simulationResult }) => {
  const [selectedAttack, setSelectedAttack] = useState('');
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationProgress, setSimulationProgress] = useState(0);
  const [currentPhase, setCurrentPhase] = useState('');
  const [liveEvents, setLiveEvents] = useState([]);
  const [networkActivity, setNetworkActivity] = useState(0);

  const attackTypes = [
    {
      id: 'ddos',
      name: 'DDoS Attack',
      description: 'Coordinated botnet flooding network resources',
      detailsDescription: 'A coordinated Distributed Denial of Service attack where multiple compromised systems flood our network infrastructure with high-volume traffic, causing service disruption and potential system overload.',
      icon: <Zap className="w-6 h-6 text-red-500" />,
      severity: 'critical',
      color: 'red',
      targets: ['Web Servers', 'Load Balancers', 'Network Infrastructure'],
      attackVectors: ['HTTP Flood', 'SYN Flood', 'UDP Flood'],
      timeline: '2-5 minutes',
      impact: 'Service Unavailability',
      expectedLogs: 3,
      realWorldExample: 'Similar to the 2016 Dyn cyberattack that disrupted major services',
      attackPhases: ['Reconnaissance', 'Botnet Coordination', 'Traffic Amplification', 'Service Disruption'],
      liveEvents: [
        'Abnormal traffic spike detected from 157.240.12.45',
        'DDoS traffic pattern identified - HTTP floods targeting /login endpoint',
        'Server response time degraded to 8.5 seconds',
        'Load balancer failover triggered',
        'Emergency rate limiting activated'
      ]
    },
    {
      id: 'phishing',
      name: 'Phishing Campaign', 
      description: 'Targeted social engineering against personnel',
      detailsDescription: 'A sophisticated spear-phishing campaign targeting military personnel with tailored emails containing malicious attachments or credential harvesting links designed to compromise user accounts.',
      icon: <Target className="w-6 h-6 text-orange-500" />,
      severity: 'high',
      color: 'orange',
      targets: ['Email Users', 'Credentials', 'Personal Information'],
      attackVectors: ['Malicious Email', 'Credential Harvesting', 'Social Engineering'],
      timeline: '1-3 minutes',
      impact: 'Account Compromise',
      expectedLogs: 3,
      realWorldExample: 'Similar to advanced phishing campaigns against defense contractors',
      attackPhases: ['Target Research', 'Email Crafting', 'Delivery', 'Credential Theft'],
      liveEvents: [
        'Suspicious email from colonel_smith@def-mail.com to 15 recipients',
        'Malicious attachment (invoice.pdf.exe) detected in quarantine',
        'User clicked phishing link - credentials intercepted',
        'Unauthorized login attempt from 95.142.78.201',
        'Password reset request triggered from compromised account'
      ]
    },
    {
      id: 'insider_threat',
      name: 'Insider Threat',
      description: 'Malicious activity from privileged internal user',
      detailsDescription: 'A trusted employee or contractor with legitimate access abusing their privileges to steal sensitive data, access unauthorized systems, or sabotage operations from within the organization.',
      icon: <Users className="w-6 h-6 text-red-600" />,
      severity: 'critical',
      color: 'red',
      targets: ['Classified Data', 'Personnel Records', 'Internal Systems'],
      attackVectors: ['Privilege Abuse', 'Data Exfiltration', 'Unauthorized Access'],
      timeline: '3-7 minutes',
      impact: 'Data Breach',
      expectedLogs: 3,
      realWorldExample: 'Similar to the Edward Snowden or Chelsea Manning cases',
      attackPhases: ['Access Expansion', 'Data Collection', 'Exfiltration', 'Cover-up Attempts'],
      liveEvents: [
        'Elevated privilege usage detected for user: thompson_m',
        'Unusual file access pattern - 847 classified documents accessed',
        'Large data transfer to external USB device detected',
        'After-hours database query activity from admin account',
        'Attempted deletion of audit logs by privileged user'
      ]
    },
    {
      id: 'ransomware',
      name: 'Ransomware Attack',
      description: 'File encryption with ransom demand',
      detailsDescription: 'Advanced ransomware deployment that encrypts critical files and systems across the network, demanding payment for decryption keys while potentially exfiltrating data for double extortion.',
      icon: <Lock className="w-6 h-6 text-purple-500" />,
      severity: 'critical',
      color: 'purple',
      targets: ['File Systems', 'Databases', 'Backup Systems'],
      attackVectors: ['File Encryption', 'Lateral Movement', 'Backup Destruction'],
      timeline: '4-8 minutes',
      impact: 'System Lockdown',
      expectedLogs: 3,
      realWorldExample: 'Similar to WannaCry or Colonial Pipeline attacks',
      attackPhases: ['Initial Access', 'Network Mapping', 'Encryption Deployment', 'Ransom Demand'],
      liveEvents: [
        'Malicious process launched: cryptolock.exe',
        'Mass file encryption started in /documents directory',
        'Backup system access attempt detected',
        'Network share enumeration from infected workstation',
        'Ransom note deployed: YOUR_FILES_ARE_ENCRYPTED.txt'
      ]
    }
  ];

  // Simulate live attack progression
  const simulateAttackProgression = async (attackType) => {
    const selectedAttackData = attackTypes.find(a => a.id === attackType);
    setLiveEvents([]);
    setSimulationProgress(0);
    setNetworkActivity(0);
    
    const totalPhases = selectedAttackData.attackPhases.length;
    const eventInterval = 800; // 800ms between events
    
    for (let i = 0; i < totalPhases; i++) {
      const phase = selectedAttackData.attackPhases[i];
      setCurrentPhase(phase);
      
      // Simulate network activity spike for different attack types
      const activityMultiplier = attackType === 'ddos' ? 8 : attackType === 'ransomware' ? 4 : 2;
      setNetworkActivity(Math.min(100, (i + 1) * 20 * activityMultiplier));
      
      // Add corresponding live event
      if (selectedAttackData.liveEvents[i]) {
        setLiveEvents(prev => [...prev, {
          id: Date.now() + i,
          message: selectedAttackData.liveEvents[i],
          timestamp: new Date().toLocaleTimeString(),
          severity: i === totalPhases - 1 ? 'critical' : i > totalPhases / 2 ? 'high' : 'medium'
        }]);
      }
      
      setSimulationProgress(((i + 1) / totalPhases) * 100);
      await new Promise(resolve => setTimeout(resolve, eventInterval));
    }
    
    // Simulate cooldown
    await new Promise(resolve => setTimeout(resolve, 1000));
    setCurrentPhase('Attack simulation completed');
  };

  const handleSimulate = async (attackType) => {
    setSelectedAttack(attackType);
    setIsSimulating(true);
    
    try {
      // Run live simulation alongside API call
      const simulationPromise = simulateAttackProgression(attackType);
      const apiPromise = onSimulateAttack(attackType);
      
      await Promise.all([simulationPromise, apiPromise]);
    } catch (error) {
      console.error('Simulation failed:', error);
    }
    
    setIsSimulating(false);
  };

  // Network activity animation effect
  useEffect(() => {
    if (!isSimulating) return;
    
    const interval = setInterval(() => {
      setNetworkActivity(prev => {
        const variation = (Math.random() - 0.5) * 10;
        return Math.max(0, Math.min(100, prev + variation));
      });
    }, 200);
    
    return () => clearInterval(interval);
  }, [isSimulating]);

  return (
    <div className="bg-bg-secondary border border-border-primary rounded-lg shadow-lg p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-cyber-danger bg-opacity-20 rounded-lg">
          <Zap className="w-6 h-6 text-cyber-danger" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-text-primary">Live Attack Simulation</h3>
          <p className="text-sm text-text-muted">Simulate realistic cyber attack scenarios to test SOC response</p>
        </div>
      </div>

      {/* Attack Selection Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {attackTypes.map((attack) => (
          <div
            key={attack.id}
            className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
              selectedAttack === attack.id
                ? 'border-cyber-danger bg-cyber-danger bg-opacity-20'
                : 'border-border-primary hover:border-border-secondary hover:bg-bg-tertiary'
            }`}
            onClick={() => setSelectedAttack(attack.id)}
          >
            <div className="flex items-start gap-3">
              {attack.icon}
              <div className="flex-1">
                <h4 className="font-medium text-text-primary mb-1">{attack.name}</h4>
                <p className="text-sm text-text-secondary mb-2">{attack.description}</p>
                
                {/* Attack Severity Badge */}
                <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                  attack.severity === 'critical' 
                    ? 'bg-cyber-danger bg-opacity-20 text-cyber-danger border border-cyber-danger border-opacity-30'
                    : 'bg-cyber-warning bg-opacity-20 text-cyber-warning border border-cyber-warning border-opacity-30'
                }`}>
                  {attack.severity.toUpperCase()}
                </span>

                {/* Quick Stats */}
                <div className="mt-2 flex items-center gap-4 text-xs text-text-muted">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {attack.timeline}
                  </span>
                  <span className="flex items-center gap-1">
                    <Database className="w-3 h-3" />
                    {attack.expectedLogs} events
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Selected Attack Details */}
      {selectedAttack && (
        <div className="mb-6 p-4 bg-bg-tertiary border border-border-secondary rounded-lg">
          {(() => {
            const selected = attackTypes.find(a => a.id === selectedAttack);
            return (
              <div>
                <h4 className="text-lg font-semibold text-text-primary mb-2 flex items-center gap-2">
                  {selected.icon}
                  {selected.name} - Detailed Overview
                </h4>
                
                <p className="text-sm text-text-secondary mb-4">{selected.detailsDescription}</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h5 className="text-sm font-medium text-text-primary mb-2">🎯 Primary Targets</h5>
                    <ul className="text-xs text-text-muted space-y-1">
                      {selected.targets.map((target, i) => (
                        <li key={i} className="flex items-center gap-1">
                          <span className="w-1 h-1 bg-cyber-danger rounded-full"></span>
                          {target}
                        </li>
                      ))}
                    </ul>
                  </div>
                  
                  <div>
                    <h5 className="text-sm font-medium text-text-primary mb-2">⚔️ Attack Vectors</h5>
                    <ul className="text-xs text-text-muted space-y-1">
                      {selected.attackVectors.map((vector, i) => (
                        <li key={i} className="flex items-center gap-1">
                          <span className="w-1 h-1 bg-cyber-warning rounded-full"></span>
                          {vector}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Attack Timeline */}
                <div className="mt-4">
                  <h5 className="text-sm font-medium text-text-primary mb-2">🔄 Attack Phases</h5>
                  <div className="flex flex-wrap gap-2">
                    {selected.attackPhases.map((phase, i) => (
                      <span key={i} className="px-2 py-1 bg-cyber-accent bg-opacity-20 text-cyber-accent text-xs rounded border border-cyber-accent border-opacity-30">
                        {i + 1}. {phase}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Real-world Context */}
                <div className="mt-4 p-3 bg-cyber-warning bg-opacity-10 border border-cyber-warning border-opacity-20 rounded">
                  <h5 className="text-sm font-medium text-cyber-warning mb-1">🌍 Real-world Context</h5>
                  <p className="text-xs text-text-muted">{selected.realWorldExample}</p>
                </div>

                {/* Expected Impact */}
                <div className="mt-3 flex items-center justify-between text-xs">
                  <span className="text-text-muted">Expected Impact:</span>
                  <span className={`font-medium ${
                    selected.severity === 'critical' ? 'text-cyber-danger' : 'text-cyber-warning'
                  }`}>
                    {selected.impact}
                  </span>
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* Live Attack Visualization */}
      {isSimulating && (
        <div className="mb-6 p-4 bg-cyber-danger bg-opacity-10 border-2 border-cyber-danger border-opacity-30 rounded-lg">
          <div className="flex items-center gap-3 mb-4">
            <div className="relative">
              <Activity className="w-6 h-6 text-cyber-danger animate-pulse" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-cyber-danger rounded-full animate-ping"></div>
            </div>
            <div>
              <h4 className="font-semibold text-cyber-danger">🚨 LIVE ATTACK IN PROGRESS</h4>
              <p className="text-sm text-text-muted">Real-time monitoring of attack progression</p>
            </div>
          </div>

          {/* Attack Progress Bar */}
          <div className="mb-4">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-text-primary font-medium">Attack Progress</span>
              <span className="text-cyber-danger font-mono">{Math.round(simulationProgress)}%</span>
            </div>
            <div className="w-full bg-bg-tertiary rounded-full h-2 border border-border-primary">
              <div 
                className="bg-gradient-to-r from-cyber-warning to-cyber-danger h-2 rounded-full transition-all duration-300 ease-out"
                style={{ width: `${simulationProgress}%` }}
              ></div>
            </div>
            {currentPhase && (
              <p className="text-xs text-cyber-danger mt-1 font-mono">🔄 {currentPhase}</p>
            )}
          </div>

          {/* Network Activity Monitor */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div className="p-3 bg-bg-secondary border border-border-primary rounded">
              <div className="flex items-center gap-2 mb-2">
                <Wifi className="w-4 h-4 text-cyber-accent" />
                <span className="text-sm font-medium text-text-primary">Network Activity</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex-1 bg-bg-tertiary rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-200 ${
                      networkActivity > 70 ? 'bg-cyber-danger' : 
                      networkActivity > 40 ? 'bg-cyber-warning' : 'bg-cyber-success'
                    }`}
                    style={{ width: `${networkActivity}%` }}
                  ></div>
                </div>
                <span className="text-xs font-mono text-text-muted w-10">{Math.round(networkActivity)}%</span>
              </div>
            </div>

            <div className="p-3 bg-bg-secondary border border-border-primary rounded">
              <div className="flex items-center gap-2 mb-2">
                <Server className="w-4 h-4 text-cyber-warning" />
                <span className="text-sm font-medium text-text-primary">System Status</span>
              </div>
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full animate-pulse ${
                  simulationProgress > 80 ? 'bg-cyber-danger' : 
                  simulationProgress > 50 ? 'bg-cyber-warning' : 'bg-cyber-success'
                }`}></div>
                <span className="text-xs text-text-muted">
                  {simulationProgress > 80 ? 'CRITICAL' : 
                   simulationProgress > 50 ? 'DEGRADED' : 'OPERATIONAL'}
                </span>
              </div>
            </div>
          </div>

          {/* Live Event Feed */}
          <div className="bg-bg-primary border border-border-primary rounded p-3">
            <div className="flex items-center gap-2 mb-2">
              <Eye className="w-4 h-4 text-cyber-accent" />
              <span className="text-sm font-medium text-text-primary">Live Security Events</span>
            </div>
            <div className="space-y-2 max-h-32 overflow-y-auto">
              {liveEvents.length === 0 ? (
                <p className="text-xs text-text-muted italic">Monitoring for attack indicators...</p>
              ) : (
                liveEvents.slice(-5).reverse().map((event) => (
                  <div key={event.id} className="flex items-start gap-2 text-xs">
                    <span className="text-text-muted font-mono whitespace-nowrap">{event.timestamp}</span>
                    <div className={`w-2 h-2 rounded-full mt-1 flex-shrink-0 ${
                      event.severity === 'critical' ? 'bg-cyber-danger animate-pulse' : 
                      event.severity === 'high' ? 'bg-cyber-warning' : 'bg-cyber-accent'
                    }`}></div>
                    <span className={`flex-1 ${
                      event.severity === 'critical' ? 'text-cyber-danger' : 
                      event.severity === 'high' ? 'text-cyber-warning' : 'text-text-secondary'
                    }`}>
                      {event.message}
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
      <div className="flex gap-3">
        <button
          onClick={() => handleSimulate(selectedAttack)}
          disabled={!selectedAttack || isSimulating}
          className="flex-1 flex items-center justify-center gap-2 bg-cyber-danger text-white px-4 py-3 rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Play className="w-4 h-4" />
          {isSimulating ? 'Executing Attack Simulation...' : 'Execute Attack Simulation'}
          {isSimulating && (
            <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent ml-1"></div>
          )}
        </button>
      </div>

      {/* Simulation Result Display */}
      {simulationResult && (
        <div className="mt-6">
          <div className="p-4 bg-cyber-success bg-opacity-20 border border-cyber-success border-opacity-30 rounded-lg mb-4">
            <div className="flex items-center gap-2 mb-3">
              <CheckCircle className="w-5 h-5 text-cyber-success" />
              <h4 className="font-medium text-cyber-success">Attack Simulation Executed Successfully</h4>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
              <div className="text-center p-3 bg-bg-tertiary rounded">
                <div className="text-lg font-bold text-cyber-success">{simulationResult.logs_created}</div>
                <div className="text-xs text-text-muted">Security Events</div>
              </div>
              <div className="text-center p-3 bg-bg-tertiary rounded">
                <div className="text-lg font-bold text-cyber-warning">{simulationResult.attack_type}</div>
                <div className="text-xs text-text-muted">Attack Type</div>
              </div>
              <div className="text-center p-3 bg-bg-tertiary rounded">
                <div className="text-lg font-bold text-cyber-accent">ACTIVE</div>
                <div className="text-xs text-text-muted">Simulation Status</div>
              </div>
            </div>

            <div className="bg-bg-primary p-3 rounded border border-border-primary">
              <h5 className="text-sm font-medium text-text-primary mb-2">🚨 Attack Simulation Summary</h5>
              <p className="text-sm text-text-secondary mb-2">{simulationResult.message}</p>
              
              <div className="text-xs text-text-muted space-y-1">
                <div className="flex justify-between">
                  <span>Simulation Mode:</span>
                  <span className="text-cyber-warning font-mono">[DEMO MODE]</span>
                </div>
                <div className="flex justify-between">
                  <span>SOC Impact:</span>
                  <span className="text-cyber-success">Real-time log analysis activated</span>
                </div>
                <div className="flex justify-between">
                  <span>Recommended Action:</span>
                  <span className="text-cyber-accent">Monitor AI Analysis panel for threat assessment</span>
                </div>
              </div>
            </div>
          </div>

          {/* Post-simulation Guidance */}
          <div className="p-3 bg-cyber-accent bg-opacity-10 border border-cyber-accent border-opacity-20 rounded">
            <h5 className="text-sm font-medium text-cyber-accent mb-2">📋 Next Steps for SOC Analysis</h5>
            <ul className="text-xs text-text-muted space-y-1">
              <li className="flex items-center gap-2">
                <span className="w-1 h-1 bg-cyber-accent rounded-full"></span>
                Check the <strong>AI Analysis</strong> section for threat intelligence
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1 h-1 bg-cyber-accent rounded-full"></span>
                Review the <strong>Security Logs</strong> for attack progression
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1 h-1 bg-cyber-accent rounded-full"></span>
                Use the <strong>AI Chat</strong> to ask specific questions about the attack
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1 h-1 bg-cyber-accent rounded-full"></span>
                Execute recommended <strong>Security Actions</strong> if needed
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default AttackSimulator;
