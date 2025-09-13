import os
import json
import requests
from typing import List, Dict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "AIzaSyBhojJ0wFVlbgnjkNeTU7aMqnETp63rRLI")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    def analyze_logs(self, logs: List[Dict]) -> Dict:
        """
        Analyze security logs using Google Gemini AI to provide threat summary,
        severity classification, and recommendations.
        """
        if not logs:
            return {
                "summary": "No logs available for analysis",
                "threats_identified": [],
                "severity_classification": "low",
                "recommendations": [],
                "total_logs_analyzed": 0
            }
        
        # Prepare logs for AI analysis with intelligent sampling
        log_text = self._format_logs_for_ai(logs, limit=30)  # Use more logs for better analysis
        
        # Get log statistics for better context
        stats = self._get_log_statistics(logs)
        
        prompt = f"""You are an expert SOC (Security Operations Center) cyber defense analyst analyzing military network security logs.

DATASET OVERVIEW:
Total Logs: {len(logs)}
Critical Events: {stats['critical']}
High Severity: {stats['high']}
Medium Severity: {stats['medium']}
Low Severity: {stats['low']}
Unique Event Types: {len(stats['event_types'])}
Top Event Types: {', '.join(list(stats['event_types'].keys())[:5])}

RECENT SECURITY EVENTS (Sample):
{log_text}

ANALYSIS REQUIREMENTS:
Provide a comprehensive threat assessment in this EXACT JSON format:
{{
  "summary": "Detailed 2-3 sentence overview of the security landscape and key threats",
  "threats_identified": ["specific_threat_1", "specific_threat_2", "specific_threat_3", "specific_threat_4"],
  "severity_classification": "low/medium/high/critical",
  "recommendations": ["actionable_recommendation_1", "actionable_recommendation_2", "actionable_recommendation_3", "actionable_recommendation_4"],
  "total_logs_analyzed": {len(logs)}
}}

ANALYSIS FOCUS:
- Network intrusions and lateral movement
- Brute force attacks and credential stuffing
- Malware communications and C2 traffic
- Privilege escalation and system compromise
- Reconnaissance and vulnerability scanning
- Anomalous authentication patterns
- Data exfiltration attempts

Provide specific, actionable intelligence for SOC teams. Return ONLY the JSON object with no additional text."""
        
        try:
            response = self._call_gemini_api(prompt)
            return self._parse_gemini_response(response, len(logs))
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_analysis(logs)
    
    def chat_response(self, question: str, logs_context: List[Dict] = None) -> str:
        """
        Generate a conversational response to analyst questions based on logs context.
        """
        if not logs_context:
            return self._fallback_chat_response(question)
        
        # Analyze the question type to provide specific data
        question_lower = question.lower()
        
        # For IP blocking questions, analyze the logs for malicious IPs
        if any(keyword in question_lower for keyword in ['ip', 'block', 'address', 'source']):
            return self._analyze_ips_for_blocking(logs_context, question)
        
        # For threat questions, focus on specific threats
        elif any(keyword in question_lower for keyword in ['threat', 'attack', 'critical', 'dangerous']):
            return self._analyze_critical_threats(logs_context, question)
        
        # For recommendation questions, provide specific actions
        elif any(keyword in question_lower for keyword in ['recommend', 'action', 'do', 'should']):
            return self._provide_specific_recommendations(logs_context, question)
        
        # General analysis with more context
        else:
            context = f"\nSECURITY CONTEXT - Analyzing {len(logs_context)} recent events:\n{self._format_logs_for_ai(logs_context[:20])}\n"
            
            prompt = f"""You are an expert SOC cyber defense analyst. Provide specific, data-driven responses based on actual log analysis.

{context}

ANALYST QUESTION: {question}

INSTRUCTIONS:
- Reference specific IPs, timestamps, and event details from the logs
- Provide concrete, actionable information
- Use technical SOC terminology
- Be specific rather than generic
- If data exists in logs, cite it directly
- Keep response focused and under 300 words

Respond as a professional SOC analyst would."""
        
        try:
            response = self._call_gemini_api(prompt)
            return self._extract_text_from_gemini(response)
        except Exception as e:
            print(f"Gemini chat error: {e}")
            return self._fallback_chat_response(question, logs_context)
    
    def _call_gemini_api(self, prompt: str) -> Dict:
        """Make a request to Gemini API"""
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "topP": 0.8,
                "topK": 40,
                "maxOutputTokens": 1024
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Gemini API error: {response.status_code} - {response.text}")
    
    def _extract_text_from_gemini(self, response: Dict) -> str:
        """Extract text content from Gemini API response"""
        try:
            return response['candidates'][0]['content']['parts'][0]['text'].strip()
        except (KeyError, IndexError):
            return "I apologize, but I'm having trouble processing your request right now."
    
    def _parse_gemini_response(self, response: Dict, log_count: int) -> Dict:
        """Parse Gemini response for log analysis"""
        try:
            text_content = self._extract_text_from_gemini(response)
            
            # Try to parse as JSON
            if text_content.startswith('{') and text_content.endswith('}'):
                parsed = json.loads(text_content)
                # Validate required fields
                if all(key in parsed for key in ['summary', 'threats_identified', 'severity_classification', 'recommendations']):
                    parsed['total_logs_analyzed'] = log_count
                    return parsed
            
            # If JSON parsing fails, extract information manually
            return self._extract_analysis_from_text(text_content, log_count)
            
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return self._fallback_analysis_with_count(log_count)
    
    def _extract_analysis_from_text(self, text: str, log_count: int) -> Dict:
        """Extract analysis components from plain text response"""
        lines = text.split('\n')
        
        summary = "Multiple security events detected across the network."
        threats = ["Network reconnaissance", "Authentication failures", "Suspicious traffic patterns"]
        severity = "medium"
        recommendations = ["Monitor failed login attempts", "Review firewall rules", "Investigate suspicious IPs"]
        
        # Try to extract actual content
        for line in lines:
            if "summary" in line.lower() and ":" in line:
                summary = line.split(":", 1)[1].strip().strip('"')
            elif "critical" in line.lower():
                severity = "critical"
            elif "high" in line.lower() and severity not in ["critical"]:
                severity = "high"
        
        return {
            "summary": summary,
            "threats_identified": threats,
            "severity_classification": severity,
            "recommendations": recommendations,
            "total_logs_analyzed": log_count
        }
    
    def _format_logs_for_ai(self, logs: List[Dict], limit: int = 30) -> str:
        """Format logs for AI analysis with better structure"""
        formatted_logs = []
        
        # Sort logs by severity (critical first) and timestamp
        sorted_logs = sorted(logs[:limit], 
                           key=lambda x: (x.get('severity', 'low') == 'critical', 
                                        x.get('severity', 'low') == 'high',
                                        x.get('timestamp', '')), 
                           reverse=True)
        
        for i, log in enumerate(sorted_logs, 1):
            timestamp = log.get('timestamp', 'Unknown')
            if isinstance(timestamp, str) and len(timestamp) > 19:
                timestamp = timestamp[:19]  # Truncate to YYYY-MM-DD HH:MM:SS
            
            event_type = log.get('event_type', 'Unknown')
            severity = log.get('severity', 'Unknown').upper()
            source_ip = log.get('source_ip', 'Unknown')
            dest_ip = log.get('dest_ip', 'Unknown')
            message = log.get('message', 'No message')
            
            # Truncate long messages for readability
            if len(message) > 150:
                message = message[:147] + "..."
            
            formatted_logs.append(
                f"{i:2d}. [{timestamp}] {severity:8s} | {event_type:25s} | {source_ip:15s} → {dest_ip:15s} | {message}"
            )
        
        return '\n'.join(formatted_logs)

    def _get_log_statistics(self, logs: List[Dict]) -> Dict:
        """Get comprehensive statistics about the log dataset"""
        stats = {
            'total': len(logs),
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'event_types': {},
            'source_ips': {},
            'dest_ips': {}
        }
        
        for log in logs:
            # Severity counts
            severity = log.get('severity', 'low').lower()
            if severity in ['critical', 'high', 'medium', 'low']:
                stats[severity] += 1
            
            # Event type counts
            event_type = log.get('event_type', 'unknown')
            stats['event_types'][event_type] = stats['event_types'].get(event_type, 0) + 1
            
            # IP address counts
            source_ip = log.get('source_ip', 'unknown')
            dest_ip = log.get('dest_ip', 'unknown')
            stats['source_ips'][source_ip] = stats['source_ips'].get(source_ip, 0) + 1
            stats['dest_ips'][dest_ip] = stats['dest_ips'].get(dest_ip, 0) + 1
        
        # Sort by frequency
        stats['event_types'] = dict(sorted(stats['event_types'].items(), 
                                         key=lambda x: x[1], reverse=True))
        stats['source_ips'] = dict(sorted(stats['source_ips'].items(), 
                                        key=lambda x: x[1], reverse=True))
        stats['dest_ips'] = dict(sorted(stats['dest_ips'].items(), 
                                      key=lambda x: x[1], reverse=True))
        
        return stats
    
    def _fallback_analysis(self, logs: List[Dict]) -> Dict:
        """Enhanced fallback analysis when Gemini API is not available"""
        if not logs:
            return self._fallback_analysis_with_count(0)
            
        stats = self._get_log_statistics(logs)
        
        # Determine overall severity based on distribution
        if stats['critical'] > 0:
            overall_severity = "critical"
        elif stats['high'] > 3 or (stats['high'] > 0 and stats['critical'] > 0):
            overall_severity = "high"
        elif stats['medium'] > 10 or stats['high'] > 0:
            overall_severity = "medium"
        else:
            overall_severity = "low"
        
        # Generate detailed threats based on event types
        threats = []
        recommendations = []
        
        for event_type, count in list(stats['event_types'].items())[:10]:
            if any(keyword in event_type.lower() for keyword in ['brute_force', 'brute', 'force']):
                threats.append(f"SSH/RDP brute force attacks detected ({count} events)")
                recommendations.append("Implement account lockout policies and IP blocking for repeated failures")
                
            elif any(keyword in event_type.lower() for keyword in ['malware', 'virus', 'trojan', 'ransomware']):
                threats.append(f"Malware activity identified ({count} events)")
                recommendations.append("Quarantine affected systems and update antivirus signatures")
                
            elif any(keyword in event_type.lower() for keyword in ['intrusion', 'breach', 'compromise']):
                threats.append(f"Network intrusion attempts ({count} events)")
                recommendations.append("Review firewall rules and implement network segmentation")
                
            elif any(keyword in event_type.lower() for keyword in ['injection', 'sql', 'xss']):
                threats.append(f"Web application attacks detected ({count} events)")
                recommendations.append("Update WAF rules and patch web applications")
                
            elif any(keyword in event_type.lower() for keyword in ['scan', 'reconnaissance', 'probe']):
                threats.append(f"Network reconnaissance activities ({count} events)")
                recommendations.append("Monitor and block scanning source IPs")
                
            elif any(keyword in event_type.lower() for keyword in ['login', 'auth', 'credential']):
                threats.append(f"Authentication anomalies ({count} events)")
                recommendations.append("Review user accounts and enable multi-factor authentication")
                
            elif any(keyword in event_type.lower() for keyword in ['ddos', 'dos', 'flood']):
                threats.append(f"Denial of service attacks ({count} events)")
                recommendations.append("Implement rate limiting and DDoS protection")
                
            elif any(keyword in event_type.lower() for keyword in ['privilege', 'escalation', 'elevation']):
                threats.append(f"Privilege escalation attempts ({count} events)")
                recommendations.append("Review user privileges and implement least-privilege principle")
        
        # Add IP-based analysis
        top_sources = list(stats['source_ips'].items())[:3]
        for ip, count in top_sources:
            if count > 5 and ip not in ['localhost', '127.0.0.1', 'unknown']:
                threats.append(f"High-volume traffic from {ip} ({count} events)")
                recommendations.append(f"Investigate and potentially block suspicious IP {ip}")
        
        # Ensure we have sufficient content
        if len(threats) < 3:
            threats.extend([
                "Multiple security events require investigation",
                "Potential coordinated attack patterns detected",
                "Anomalous network behavior identified"
            ])
        
        if len(recommendations) < 3:
            recommendations.extend([
                "Increase monitoring and alerting sensitivity",
                "Conduct thorough security audit",
                "Review and update security policies"
            ])
        
        # Create comprehensive summary
        event_diversity = len(stats['event_types'])
        severity_summary = f"{stats['critical']} critical, {stats['high']} high, {stats['medium']} medium severity"
        
        summary = f"Comprehensive analysis of {len(logs)} security events revealed {event_diversity} distinct threat types with {severity_summary} incidents. Key concerns include {list(stats['event_types'].keys())[0] if stats['event_types'] else 'various security events'} and multiple attack vectors targeting network infrastructure."
        
        return {
            "summary": summary,
            "threats_identified": threats[:6],  # Top 6 threats
            "severity_classification": overall_severity,
            "recommendations": recommendations[:6],  # Top 6 recommendations
            "total_logs_analyzed": len(logs)
        }
    
    def _fallback_analysis_with_count(self, log_count: int) -> Dict:
        """Fallback analysis with log count"""
        return {
            "summary": f"Processed {log_count} security events. Multiple threat vectors identified requiring immediate attention.",
            "threats_identified": [
                "Network intrusion attempts detected",
                "Brute force authentication attacks",
                "Suspicious outbound connections",
                "Potential malware communications"
            ],
            "severity_classification": "high",
            "recommendations": [
                "Implement immediate IP blocking for suspicious sources",
                "Review and update firewall rules",
                "Conduct thorough network scan for compromised systems",
                "Enable enhanced monitoring on critical assets"
            ],
            "total_logs_analyzed": log_count
        }
    
    def _fallback_chat_response(self, question: str, logs_context: List[Dict] = None) -> str:
        """Enhanced fallback chat response when Gemini API is not available"""
        question_lower = question.lower()
        
        if logs_context:
            # Try to provide more intelligent responses based on actual log data
            stats = self._get_log_statistics(logs_context)
            
            if any(word in question_lower for word in ['ip', 'address', 'source']):
                top_ips = list(stats['source_ips'].items())[:3]
                response = "**IP Analysis (Local Analysis):**\n"
                response += f"Analyzing {len(logs_context)} security events:\n\n"
                for ip, count in top_ips:
                    if ip not in ['unknown', '127.0.0.1', 'localhost']:
                        response += f"• {ip}: {count} events detected\n"
                return response
                
            elif any(word in question_lower for word in ['attack', 'threat', 'malware', 'status', 'security', 'situation', 'environment', 'current', 'understand', 'help']):
                response = "**Security Status (Local Analysis):**\n"
                response += f"Current threat landscape from {len(logs_context)} recent events:\n\n"
                response += f"• Critical: {stats['critical']} events\n"
                response += f"• High: {stats['high']} events\n"
                response += f"• Medium: {stats['medium']} events\n"
                response += f"• Low: {stats['low']} events\n\n"
                
                top_threats = list(stats['event_types'].items())[:3]
                response += "Top threats:\n"
                for threat_type, count in top_threats:
                    response += f"• {threat_type}: {count} occurrences\n"
                    
                # Add some analysis
                if stats['critical'] > 0:
                    response += f"\n⚠️ **URGENT**: {stats['critical']} critical events require immediate attention"
                if stats['high'] >= 10:
                    response += f"\n⚡ **HIGH PRIORITY**: {stats['high']} high-severity events need review"
                    
                return response
                
            elif any(word in question_lower for word in ['recommend', 'action', 'do']):
                response = "**Recommendations (Local Analysis):**\n"
                response += "Based on current security events:\n\n"
                if stats['critical'] > 0:
                    response += f"🚨 URGENT: {stats['critical']} critical events require immediate attention\n"
                if stats['high'] >= 5:
                    response += f"⚠️ HIGH: {stats['high']} high-severity events need review\n"
                    
                # Add specific recommendations based on top event types
                top_events = list(stats['event_types'].items())[:2]
                for event_type, count in top_events:
                    if 'brute_force' in event_type.lower():
                        response += f"• Implement SSH rate limiting ({count} brute force attempts)\n"
                    elif 'malware' in event_type.lower():
                        response += f"• Quarantine affected systems ({count} malware detections)\n"
                return response
        
        # Generic responses when no log context available
        if any(word in question_lower for word in ['ip', 'address', 'source']):
            return "I can help analyze IP addresses and network traffic patterns. Please check the security logs for detailed information about specific IP activities."
        elif any(word in question_lower for word in ['attack', 'threat', 'malware']):
            return "Based on current security events, I recommend monitoring brute force attempts, malware communications, and network intrusions. Review the threat analysis panel for detailed insights."
        elif any(word in question_lower for word in ['recommend', 'action', 'do']):
            return "Key recommendations: 1) Block suspicious IPs, 2) Update security rules, 3) Monitor critical systems, 4) Review authentication logs."
        else:
            return "I'm a SOC cyber defense assistant. Ask me about security threats, IP addresses, attack patterns, or recommended actions based on the current security events."
    
    def _analyze_ips_for_blocking(self, logs_context: List[Dict], question: str) -> str:
        """Analyze logs to identify specific IPs that should be blocked"""
        if not logs_context:
            return "No log data available for IP analysis."
        
        # Collect IP statistics
        malicious_ips = {}
        critical_ips = {}
        
        for log in logs_context:
            source_ip = log.get('source_ip', 'unknown')
            severity = log.get('severity', 'low').lower()
            event_type = log.get('event_type', '').lower()
            message = log.get('message', '').lower()
            
            if source_ip == 'unknown' or source_ip in ['127.0.0.1', 'localhost']:
                continue
                
            # Count occurrences and severity
            if source_ip not in malicious_ips:
                malicious_ips[source_ip] = {'count': 0, 'critical': 0, 'high': 0, 'events': []}
            
            malicious_ips[source_ip]['count'] += 1
            malicious_ips[source_ip]['events'].append(event_type)
            
            if severity == 'critical':
                malicious_ips[source_ip]['critical'] += 1
                critical_ips[source_ip] = malicious_ips[source_ip]
            elif severity == 'high':
                malicious_ips[source_ip]['high'] += 1
        
        # Identify IPs to block based on criteria
        block_recommendations = []
        
        for ip, stats in malicious_ips.items():
            # Block criteria: multiple events, high/critical severity, or malicious patterns
            if (stats['count'] >= 3 or 
                stats['critical'] >= 1 or 
                stats['high'] >= 2 or
                any(malicious in ' '.join(stats['events']) for malicious in ['brute_force', 'malware', 'intrusion', 'attack'])):
                
                threat_level = "CRITICAL" if stats['critical'] > 0 else "HIGH" if stats['high'] > 0 else "MEDIUM"
                event_types = list(set(stats['events']))[:3]
                
                block_recommendations.append({
                    'ip': ip,
                    'threat_level': threat_level,
                    'event_count': stats['count'],
                    'critical_events': stats['critical'],
                    'high_events': stats['high'],
                    'attack_types': event_types
                })
        
        # Sort by threat level and event count
        block_recommendations.sort(key=lambda x: (x['critical_events'], x['high_events'], x['event_count']), reverse=True)
        
        if not block_recommendations:
            return "Based on current log analysis, no IPs meet the immediate blocking criteria. Continue monitoring for patterns."
        
        # Format response
        response = f"🚨 IMMEDIATE IP BLOCKING RECOMMENDATIONS:\n\n"
        response += f"Analyzed {len(logs_context)} security events. Found {len(block_recommendations)} IPs requiring blocking:\n\n"
        
        for i, rec in enumerate(block_recommendations[:10], 1):  # Top 10
            response += f"{i}. {rec['ip']} ({rec['threat_level']} RISK)\n"
            response += f"   - Events: {rec['event_count']} total ({rec['critical_events']} critical, {rec['high_events']} high)\n"
            response += f"   - Attacks: {', '.join(rec['attack_types'])}\n"
            response += f"   - Action: BLOCK IMMEDIATELY\n\n"
        
        response += "BLOCKING RATIONALE: These IPs show patterns of malicious activity including multiple attack attempts, high-severity events, or known attack signatures."
        
        return response
    
    def _analyze_critical_threats(self, logs_context: List[Dict], question: str) -> str:
        """Analyze logs for critical threats and specific attack details"""
        if not logs_context:
            return "No log data available for threat analysis."
        
        # Categorize threats by severity and type
        critical_threats = []
        high_threats = []
        threat_summary = {}
        
        for log in logs_context:
            severity = log.get('severity', 'low').lower()
            event_type = log.get('event_type', 'unknown')
            source_ip = log.get('source_ip', 'unknown')
            message = log.get('message', '')
            timestamp = log.get('timestamp', 'unknown')
            
            threat_entry = {
                'severity': severity,
                'event_type': event_type,
                'source_ip': source_ip,
                'message': message,
                'timestamp': timestamp
            }
            
            if severity == 'critical':
                critical_threats.append(threat_entry)
            elif severity == 'high':
                high_threats.append(threat_entry)
            
            # Count by event type
            threat_summary[event_type] = threat_summary.get(event_type, 0) + 1
        
        if not critical_threats and not high_threats:
            return "No critical or high-severity threats identified in recent logs. Current threat level: LOW."
        
        # Format detailed response
        response = f"🚨 CRITICAL THREAT ANALYSIS:\n\n"
        response += f"Analysis of {len(logs_context)} events:\n"
        response += f"- CRITICAL threats: {len(critical_threats)}\n"
        response += f"- HIGH severity threats: {len(high_threats)}\n\n"
        
        if critical_threats:
            response += "CRITICAL THREATS REQUIRING IMMEDIATE ACTION:\n"
            for i, threat in enumerate(critical_threats[:5], 1):
                response += f"{i}. {threat['event_type']} from {threat['source_ip']}\n"
                response += f"   Time: {threat['timestamp']}\n"
                response += f"   Details: {threat['message'][:100]}...\n"
                response += f"   IMMEDIATE ACTION REQUIRED\n\n"
        
        if high_threats:
            response += f"HIGH SEVERITY THREATS ({len(high_threats)} total):\n"
            for threat in high_threats[:3]:
                response += f"- {threat['event_type']} from {threat['source_ip']}\n"
        
        # Top threat types
        top_threats = sorted(threat_summary.items(), key=lambda x: x[1], reverse=True)[:5]
        response += f"\nTOP ATTACK VECTORS:\n"
        for threat_type, count in top_threats:
            response += f"- {threat_type}: {count} events\n"
        
        return response
    
    def _provide_specific_recommendations(self, logs_context: List[Dict], question: str) -> str:
        """Provide specific, actionable recommendations based on log analysis"""
        if not logs_context:
            return "No log data available for recommendations."
        
        # Analyze patterns for specific recommendations
        stats = self._get_log_statistics(logs_context)
        recommendations = []
        
        # IP-based recommendations
        high_volume_ips = [(ip, count) for ip, count in stats['source_ips'].items() 
                          if count >= 5 and ip not in ['unknown', '127.0.0.1', 'localhost']]
        
        if high_volume_ips:
            top_ip, count = high_volume_ips[0]
            recommendations.append(f"🚫 BLOCK IP {top_ip} immediately ({count} malicious events)")
        
        # Event-type based recommendations
        for event_type, count in list(stats['event_types'].items())[:5]:
            if 'brute_force' in event_type.lower() and count >= 3:
                recommendations.append(f"🔒 Implement rate limiting for SSH/RDP services ({count} brute force attempts)")
            elif 'malware' in event_type.lower() and count >= 2:
                recommendations.append(f"🦠 Quarantine affected systems and update antivirus signatures ({count} malware detections)")
            elif 'intrusion' in event_type.lower() and count >= 2:
                recommendations.append(f"🛡️ Review firewall rules and enable network segmentation ({count} intrusion attempts)")
        
        # Severity-based recommendations
        if stats['critical'] >= 3:
            recommendations.append(f"⚠️ URGENT: Escalate to incident response team ({stats['critical']} critical events)")
        if stats['high'] >= 10:
            recommendations.append(f"📊 Enable enhanced monitoring ({stats['high']} high-severity events)")
        
        # General recommendations based on volume
        if stats['total'] >= 100:
            recommendations.append("📈 Consider increasing log retention and analysis frequency")
        
        if not recommendations:
            recommendations = [
                "Continue current monitoring practices",
                "Review security policies and update as needed",
                "Maintain vigilance for emerging threats"
            ]
        
        response = f"🎯 SPECIFIC SOC RECOMMENDATIONS:\n\n"
        response += f"Based on analysis of {len(logs_context)} security events:\n\n"
        
        for i, rec in enumerate(recommendations[:8], 1):
            response += f"{i}. {rec}\n"
        
        response += f"\nPRIORITY: Focus on the first 3-4 recommendations for immediate impact."
        
        return response
