import React, { useState, useEffect } from 'react';
import { AlertTriangle, Clock, Users, CheckCircle, XCircle, Play, Pause, Shield, Target, Zap, FileText, Phone, Mail } from 'lucide-react';

const IncidentResponse = ({ logs, analysis }) => {
  const [incidents, setIncidents] = useState([]);
  const [activePlaybook, setActivePlaybook] = useState(null);
  const [responseTeams, setResponseTeams] = useState([]);
  const [escalationMatrix, setEscalationMatrix] = useState([]);
  const [automatedActions, setAutomatedActions] = useState([]);
  const [responseMetrics, setResponseMetrics] = useState({});

  // Initialize incident response system
  useEffect(() => {
    generateIncidents();
    initializeResponseTeams();
    setupEscalationMatrix();
    loadAutomatedActions();
    calculateMetrics();
  }, [logs, analysis]);

  const generateIncidents = () => {
    if (!logs || logs.length === 0) return;

    // Group logs into potential incidents
    const criticalLogs = logs.filter(log => log.severity === 'critical');
    const incidentGroups = {};

    criticalLogs.forEach(log => {
      const key = `${log.event_type}-${log.source_ip}`;
      if (!incidentGroups[key]) {
        incidentGroups[key] = {
          id: `INC-${Date.now()}-${Math.random().toString(36).substr(2, 4).toUpperCase()}`,
          title: `${log.event_type} from ${log.source_ip}`,
          type: log.event_type,
          severity: determineSeverity(log),
          status: 'open',
          source_ip: log.source_ip,
          first_detected: log.timestamp,
          last_activity: log.timestamp,
          events_count: 1,
          affected_systems: [log.dest_ip || 'Unknown'],
          assigned_team: assignTeam(log.event_type),
          playbook: getPlaybook(log.event_type),
          timeline: [{
            timestamp: log.timestamp,
            action: 'Incident Created',
            user: 'System',
            details: `Automated detection of ${log.event_type}`
          }],
          artifacts: [
            { type: 'log', data: log.message, source: 'SIEM' },
            { type: 'ip', data: log.source_ip, source: 'Network' }
          ],
          impact: assessImpact(log),
          containment_status: 'not_started',
          eradication_status: 'not_started',
          recovery_status: 'not_started'
        };
      } else {
        incidentGroups[key].events_count++;
        incidentGroups[key].last_activity = log.timestamp;
        incidentGroups[key].timeline.push({
          timestamp: log.timestamp,
          action: 'Additional Event',
          user: 'System',
          details: log.message
        });
      }
    });

    // Add some simulated ongoing incidents
    const simulatedIncidents = [
      {
        id: 'INC-2025-RANSOMWARE-001',
        title: 'Ransomware Outbreak - Finance Department',
        type: 'Ransomware',
        severity: 'critical',
        status: 'in_progress',
        source_ip: '192.168.50.42',
        first_detected: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        last_activity: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        events_count: 23,
        affected_systems: ['WIN-FINANCE-01', 'WIN-FINANCE-02', 'FILE-SERVER-03'],
        assigned_team: 'Cyber Incident Response Team',
        playbook: 'Ransomware Response Playbook v2.1',
        timeline: [
          {
            timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
            action: 'Incident Created',
            user: 'System',
            details: 'Automated ransomware detection triggered'
          },
          {
            timestamp: new Date(Date.now() - 1.8 * 60 * 60 * 1000).toISOString(),
            action: 'Team Notified',
            user: 'System',
            details: 'CIRT team automatically notified via Slack and email'
          },
          {
            timestamp: new Date(Date.now() - 1.5 * 60 * 60 * 1000).toISOString(),
            action: 'Containment Started',
            user: 'Sarah Chen',
            details: 'Network segments isolated, affected systems quarantined'
          },
          {
            timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
            action: 'Forensics Initiated',
            user: 'Mike Rodriguez',
            details: 'Memory dumps collected, disk images created'
          },
          {
            timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
            action: 'External Communication',
            user: 'Lisa Wong',
            details: 'Legal and PR teams briefed on potential data exposure'
          }
        ],
        artifacts: [
          { type: 'hash', data: 'a1b2c3d4e5f6...', source: 'Malware Analysis' },
          { type: 'registry', data: 'HKLM\\SOFTWARE\\...', source: 'Host Forensics' },
          { type: 'network', data: 'C2: 185.220.101.42:443', source: 'Traffic Analysis' }
        ],
        impact: 'high',
        containment_status: 'in_progress',
        eradication_status: 'not_started',
        recovery_status: 'not_started'
      }
    ];

    setIncidents([...Object.values(incidentGroups), ...simulatedIncidents]);
  };

  const determineSeverity = (log) => {
    const severityMap = {
      'critical': 'critical',
      'high': 'high',
      'medium': 'medium',
      'low': 'low'
    };
    return severityMap[log.severity] || 'medium';
  };

  const assignTeam = (eventType) => {
    const teamAssignments = {
      'Ransomware': 'Cyber Incident Response Team',
      'DDoS Attack': 'Network Security Team',
      'Malware Attack': 'Malware Analysis Team',
      'Data Breach': 'Data Protection Team',
      'Insider Threat': 'Insider Threat Team',
      'Phishing Attempt': 'Email Security Team'
    };
    return teamAssignments[eventType] || 'General Security Team';
  };

  const getPlaybook = (eventType) => {
    const playbookMap = {
      'Ransomware': 'Ransomware Response Playbook v2.1',
      'DDoS Attack': 'DDoS Mitigation Playbook v1.5',
      'Malware Attack': 'Malware Incident Response v3.0',
      'Data Breach': 'Data Breach Response v2.0',
      'Insider Threat': 'Insider Threat Investigation v1.2',
      'Phishing Attempt': 'Phishing Response Playbook v1.8'
    };
    return playbookMap[eventType] || 'General Incident Response v4.0';
  };

  const assessImpact = (log) => {
    if (log.severity === 'critical') return 'high';
    if (log.severity === 'high') return 'medium';
    return 'low';
  };

  const initializeResponseTeams = () => {
    setResponseTeams([
      {
        name: 'Cyber Incident Response Team',
        members: [
          { name: 'Sarah Chen', role: 'Lead Analyst', status: 'available', expertise: ['Malware', 'Forensics'] },
          { name: 'Mike Rodriguez', role: 'Senior Analyst', status: 'on_incident', expertise: ['Network', 'APT'] },
          { name: 'Alex Kim', role: 'Junior Analyst', status: 'available', expertise: ['OSINT', 'Threat Hunting'] }
        ],
        on_call: 'Sarah Chen',
        availability: '24/7',
        response_time: '15 minutes'
      },
      {
        name: 'Network Security Team',
        members: [
          { name: 'David Park', role: 'Network Lead', status: 'available', expertise: ['Firewall', 'IDS/IPS'] },
          { name: 'Emma Wilson', role: 'Network Analyst', status: 'available', expertise: ['Traffic Analysis', 'DDoS'] }
        ],
        on_call: 'David Park',
        availability: '24/7',
        response_time: '10 minutes'
      },
      {
        name: 'Malware Analysis Team',
        members: [
          { name: 'Dr. James Liu', role: 'Malware Analyst', status: 'available', expertise: ['Reverse Engineering', 'Sandbox'] },
          { name: 'Nina Patel', role: 'Behavioral Analyst', status: 'off_duty', expertise: ['Dynamic Analysis', 'IOC'] }
        ],
        on_call: 'Dr. James Liu',
        availability: 'Business Hours',
        response_time: '30 minutes'
      }
    ]);
  };

  const setupEscalationMatrix = () => {
    setEscalationMatrix([
      { level: 1, timeframe: '15 minutes', role: 'SOC Analyst', action: 'Initial assessment and containment' },
      { level: 2, timeframe: '30 minutes', role: 'Senior Analyst', action: 'Advanced analysis and response coordination' },
      { level: 3, timeframe: '1 hour', role: 'Incident Manager', action: 'Resource coordination and stakeholder communication' },
      { level: 4, timeframe: '2 hours', role: 'CISO', action: 'Strategic decision making and external coordination' },
      { level: 5, timeframe: '4 hours', role: 'Executive Leadership', action: 'Business continuity and crisis management' }
    ]);
  };

  const loadAutomatedActions = () => {
    setAutomatedActions([
      {
        id: 'auto-001',
        name: 'Automated IP Blocking',
        trigger: 'Multiple failed login attempts',
        status: 'active',
        executed_count: 147,
        success_rate: 98.6
      },
      {
        id: 'auto-002',
        name: 'Email Quarantine',
        trigger: 'Malicious attachment detected',
        status: 'active',
        executed_count: 23,
        success_rate: 100
      },
      {
        id: 'auto-003',
        name: 'Host Isolation',
        trigger: 'Malware signature match',
        status: 'active',
        executed_count: 8,
        success_rate: 87.5
      },
      {
        id: 'auto-004',
        name: 'DNS Sinkholing',
        trigger: 'C2 communication detected',
        status: 'paused',
        executed_count: 5,
        success_rate: 80
      }
    ]);
  };

  const calculateMetrics = () => {
    const totalIncidents = incidents.length;
    const openIncidents = incidents.filter(i => i.status === 'open').length;
    const criticalIncidents = incidents.filter(i => i.severity === 'critical').length;
    const avgResponseTime = 18; // minutes
    const mttr = 4.2; // hours

    setResponseMetrics({
      totalIncidents,
      openIncidents,
      criticalIncidents,
      avgResponseTime,
      mttr,
      containmentRate: 94.2,
      falsePositiveRate: 3.1
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'open': return 'text-red-400';
      case 'in_progress': return 'text-yellow-400';
      case 'resolved': return 'text-green-400';
      case 'closed': return 'text-gray-400';
      default: return 'text-gray-400';
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  const IncidentCard = ({ incident }) => (
    <div className="bg-bg-tertiary border border-border-primary rounded-lg p-4 hover:border-border-accent transition-colors">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className={`w-3 h-3 rounded-full ${getSeverityColor(incident.severity)}`}></div>
          <div>
            <h4 className="font-semibold text-text-primary">{incident.title}</h4>
            <p className="text-sm text-text-muted">{incident.id}</p>
          </div>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(incident.status)} bg-opacity-20`}>
          {incident.status.replace('_', ' ').toUpperCase()}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-3 text-sm">
        <div>
          <span className="text-text-muted">Assigned Team:</span>
          <p className="text-text-primary font-medium">{incident.assigned_team}</p>
        </div>
        <div>
          <span className="text-text-muted">Events:</span>
          <p className="text-text-primary font-medium">{incident.events_count}</p>
        </div>
        <div>
          <span className="text-text-muted">First Detected:</span>
          <p className="text-text-primary font-medium">{new Date(incident.first_detected).toLocaleTimeString()}</p>
        </div>
        <div>
          <span className="text-text-muted">Last Activity:</span>
          <p className="text-text-primary font-medium">{new Date(incident.last_activity).toLocaleTimeString()}</p>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="text-xs text-text-muted">
          Playbook: {incident.playbook}
        </div>
        <button
          onClick={() => setActivePlaybook(incident)}
          className="px-3 py-1 bg-cyber-primary text-white rounded text-xs hover:bg-blue-600 transition-colors"
        >
          View Details
        </button>
      </div>
    </div>
  );

  const PlaybookModal = ({ incident, onClose }) => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-bg-secondary border border-border-primary rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div className="p-6 border-b border-border-primary">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-text-primary">{incident.title}</h2>
              <p className="text-text-muted">{incident.id} - {incident.playbook}</p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-bg-tertiary rounded-lg transition-colors"
            >
              <XCircle className="w-5 h-5 text-text-muted" />
            </button>
          </div>
        </div>

        <div className="p-6 overflow-y-auto max-h-[calc(90vh-100px)]">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Incident Overview */}
            <div className="lg:col-span-2 space-y-6">
              {/* Response Timeline */}
              <div>
                <h3 className="text-lg font-semibold text-text-primary mb-4">Response Timeline</h3>
                <div className="space-y-4">
                  {incident.timeline.map((event, index) => (
                    <div key={index} className="flex gap-4">
                      <div className="flex-shrink-0 w-2 h-2 bg-cyber-primary rounded-full mt-2"></div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-medium text-text-primary">{event.action}</span>
                          <span className="text-xs text-text-muted">
                            {new Date(event.timestamp).toLocaleString()}
                          </span>
                        </div>
                        <p className="text-sm text-text-muted">{event.details}</p>
                        <p className="text-xs text-cyber-primary">by {event.user}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Artifacts */}
              <div>
                <h3 className="text-lg font-semibold text-text-primary mb-4">Evidence & Artifacts</h3>
                <div className="space-y-3">
                  {incident.artifacts.map((artifact, index) => (
                    <div key={index} className="bg-bg-tertiary border border-border-primary rounded-lg p-3">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-text-primary capitalize">{artifact.type}</span>
                        <span className="text-xs text-text-muted">{artifact.source}</span>
                      </div>
                      <code className="text-xs text-cyber-primary font-mono">{artifact.data}</code>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Incident Details Sidebar */}
            <div className="space-y-6">
              {/* Status */}
              <div className="bg-bg-tertiary border border-border-primary rounded-lg p-4">
                <h4 className="font-semibold text-text-primary mb-3">Response Status</h4>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-text-muted">Containment</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                      incident.containment_status === 'complete' ? 'bg-green-500 text-white' :
                      incident.containment_status === 'in_progress' ? 'bg-yellow-500 text-white' :
                      'bg-gray-500 text-white'
                    }`}>
                      {incident.containment_status.replace('_', ' ')}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-text-muted">Eradication</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                      incident.eradication_status === 'complete' ? 'bg-green-500 text-white' :
                      incident.eradication_status === 'in_progress' ? 'bg-yellow-500 text-white' :
                      'bg-gray-500 text-white'
                    }`}>
                      {incident.eradication_status.replace('_', ' ')}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-text-muted">Recovery</span>
                    <span className={`px-2 py-1 rounded text-xs ${
                      incident.recovery_status === 'complete' ? 'bg-green-500 text-white' :
                      incident.recovery_status === 'in_progress' ? 'bg-yellow-500 text-white' :
                      'bg-gray-500 text-white'
                    }`}>
                      {incident.recovery_status.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              </div>

              {/* Affected Systems */}
              <div className="bg-bg-tertiary border border-border-primary rounded-lg p-4">
                <h4 className="font-semibold text-text-primary mb-3">Affected Systems</h4>
                <div className="space-y-2">
                  {incident.affected_systems.map((system, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <Target className="w-4 h-4 text-red-400" />
                      <span className="text-sm text-text-primary font-mono">{system}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="space-y-3">
                <button className="w-full flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors">
                  <Shield className="w-4 h-4" />
                  Emergency Containment
                </button>
                <button className="w-full flex items-center gap-2 px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors">
                  <Users className="w-4 h-4" />
                  Escalate Incident
                </button>
                <button className="w-full flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                  <FileText className="w-4 h-4" />
                  Generate Report
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Incident Response Dashboard Header */}
      <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-red-500 bg-opacity-20 rounded-lg">
              <AlertTriangle className="w-6 h-6 text-red-400" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-text-primary">Incident Response Center</h2>
              <p className="text-text-muted">Coordinated security incident management and response</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-2xl font-bold text-text-primary">{responseMetrics.mttr}h</div>
              <div className="text-xs text-text-muted">Avg MTTR</div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-green-400">{responseMetrics.containmentRate}%</div>
              <div className="text-xs text-text-muted">Containment Rate</div>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-bg-tertiary p-4 rounded-lg border border-border-primary text-center">
            <div className="text-xl font-bold text-text-primary">{responseMetrics.totalIncidents}</div>
            <div className="text-xs text-text-muted">Total Incidents</div>
          </div>
          <div className="bg-bg-tertiary p-4 rounded-lg border border-border-primary text-center">
            <div className="text-xl font-bold text-red-400">{responseMetrics.openIncidents}</div>
            <div className="text-xs text-text-muted">Open Incidents</div>
          </div>
          <div className="bg-bg-tertiary p-4 rounded-lg border border-border-primary text-center">
            <div className="text-xl font-bold text-orange-400">{responseMetrics.criticalIncidents}</div>
            <div className="text-xs text-text-muted">Critical</div>
          </div>
          <div className="bg-bg-tertiary p-4 rounded-lg border border-border-primary text-center">
            <div className="text-xl font-bold text-blue-400">{responseMetrics.avgResponseTime}m</div>
            <div className="text-xs text-text-muted">Avg Response</div>
          </div>
          <div className="bg-bg-tertiary p-4 rounded-lg border border-border-primary text-center">
            <div className="text-xl font-bold text-yellow-400">{responseMetrics.falsePositiveRate}%</div>
            <div className="text-xs text-text-muted">False Positives</div>
          </div>
        </div>
      </div>

      {/* Active Incidents */}
      <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
        <h3 className="text-lg font-semibold text-text-primary mb-4">Active Incidents</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {incidents.slice(0, 6).map((incident, index) => (
            <IncidentCard key={index} incident={incident} />
          ))}
        </div>
      </div>

      {/* Response Teams & Automation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Response Teams */}
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-4">Response Teams</h3>
          <div className="space-y-4">
            {responseTeams.map((team, index) => (
              <div key={index} className="bg-bg-tertiary border border-border-primary rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-medium text-text-primary">{team.name}</h4>
                  <div className="flex items-center gap-2 text-sm">
                    <Clock className="w-4 h-4 text-blue-400" />
                    <span className="text-text-muted">{team.response_time}</span>
                  </div>
                </div>
                <div className="space-y-2">
                  {team.members.map((member, memberIndex) => (
                    <div key={memberIndex} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${
                          member.status === 'available' ? 'bg-green-400' :
                          member.status === 'on_incident' ? 'bg-red-400' : 'bg-gray-400'
                        }`}></div>
                        <span className="text-sm text-text-primary">{member.name}</span>
                        <span className="text-xs text-text-muted">({member.role})</span>
                      </div>
                      <div className="text-xs text-text-muted">
                        {member.expertise.join(', ')}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Automated Actions */}
        <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
          <h3 className="text-lg font-semibold text-text-primary mb-4">Automated Response Actions</h3>
          <div className="space-y-4">
            {automatedActions.map((action, index) => (
              <div key={index} className="bg-bg-tertiary border border-border-primary rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-text-primary">{action.name}</h4>
                  <div className="flex items-center gap-2">
                    {action.status === 'active' ? 
                      <Play className="w-4 h-4 text-green-400" /> : 
                      <Pause className="w-4 h-4 text-yellow-400" />
                    }
                    <span className={`px-2 py-1 rounded text-xs ${
                      action.status === 'active' ? 'bg-green-500 text-white' : 'bg-yellow-500 text-white'
                    }`}>
                      {action.status}
                    </span>
                  </div>
                </div>
                <p className="text-sm text-text-muted mb-3">{action.trigger}</p>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-text-muted">Executed: {action.executed_count} times</span>
                  <span className="text-green-400">Success: {action.success_rate}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Escalation Matrix */}
      <div className="bg-bg-secondary border border-border-primary rounded-xl p-6">
        <h3 className="text-lg font-semibold text-text-primary mb-4">Escalation Matrix</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border-primary">
                <th className="text-left p-3 text-text-muted">Level</th>
                <th className="text-left p-3 text-text-muted">Timeframe</th>
                <th className="text-left p-3 text-text-muted">Role</th>
                <th className="text-left p-3 text-text-muted">Action</th>
              </tr>
            </thead>
            <tbody>
              {escalationMatrix.map((level, index) => (
                <tr key={index} className="border-b border-border-primary border-opacity-30">
                  <td className="p-3">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 bg-cyber-primary text-white rounded-full flex items-center justify-center text-sm font-bold">
                        {level.level}
                      </div>
                      <span className="text-text-primary">Level {level.level}</span>
                    </div>
                  </td>
                  <td className="p-3 text-text-muted">{level.timeframe}</td>
                  <td className="p-3 text-text-primary font-medium">{level.role}</td>
                  <td className="p-3 text-text-muted">{level.action}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Playbook Modal */}
      {activePlaybook && (
        <PlaybookModal incident={activePlaybook} onClose={() => setActivePlaybook(null)} />
      )}
    </div>
  );
};

export default IncidentResponse;
