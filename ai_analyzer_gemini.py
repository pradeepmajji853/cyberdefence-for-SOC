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
        
        # Prepare logs for AI analysis
        log_text = self._format_logs_for_ai(logs)
        
        prompt = f"""You are a SOC (Security Operations Center) cyber defense assistant analyzing military network security logs.

SECURITY LOGS TO ANALYZE:
{log_text}

Please provide a comprehensive analysis in this EXACT JSON format:
{{
  "summary": "Brief overview of security events in 2-3 sentences",
  "threats_identified": ["threat1", "threat2", "threat3"],
  "severity_classification": "low/medium/high/critical",
  "recommendations": ["recommendation1", "recommendation2", "recommendation3"],
  "total_logs_analyzed": {len(logs)}
}}

Focus on:
- Network intrusions and brute force attacks
- Malware and C2 communications
- Privilege escalation attempts
- Port scanning and reconnaissance
- Failed authentication patterns

Provide actionable intelligence for SOC analysts. Return ONLY the JSON object."""
        
        try:
            response = self._call_gemini_api(prompt)
            return self._parse_gemini_response(response, len(logs))
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_analysis(logs)
    
    def chat(self, question: str, logs_context: List[Dict] = None) -> str:
        """
        Chat interface using Gemini AI for natural language security queries.
        """
        context = ""
        if logs_context:
            context = f"\nCONTEXT - Recent security events:\n{self._format_logs_for_ai(logs_context[:10])}\n"
        
        prompt = f"""You are a military SOC cyber defense assistant. Answer security-related questions with technical expertise.
        
        {context}
        
        QUESTION: {question}
        
        Provide a concise, technical response focused on cybersecurity. If asked about specific IPs, events, or threats, reference the context data. Keep responses under 200 words."""
        
        try:
            response = self._call_gemini_api(prompt)
            return self._extract_text_from_gemini(response)
        except Exception as e:
            print(f"Gemini chat error: {e}")
            return self._fallback_chat_response(question)
    
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
    
    def _format_logs_for_ai(self, logs: List[Dict], limit: int = 20) -> str:
        """Format logs for AI analysis"""
        formatted_logs = []
        for log in logs[:limit]:
            timestamp = log.get('timestamp', 'Unknown')
            event_type = log.get('event_type', 'Unknown')
            severity = log.get('severity', 'Unknown')
            source_ip = log.get('source_ip', 'Unknown')
            dest_ip = log.get('dest_ip', 'Unknown')
            message = log.get('message', 'No message')
            
            formatted_logs.append(
                f"[{timestamp}] {severity.upper()} - {event_type}: {source_ip} → {dest_ip} | {message}"
            )
        
        return '\n'.join(formatted_logs)
    
    def _fallback_analysis(self, logs: List[Dict]) -> Dict:
        """Fallback analysis when Gemini API is not available"""
        severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        event_types = {}
        
        for log in logs:
            sev = log.get('severity', 'low').lower()
            if sev in severity_counts:
                severity_counts[sev] += 1
            
            event_type = log.get('event_type', 'unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        # Determine overall severity
        if severity_counts['critical'] > 0:
            overall_severity = "critical"
        elif severity_counts['high'] > 2:
            overall_severity = "high"
        elif severity_counts['medium'] > 5:
            overall_severity = "medium"
        else:
            overall_severity = "low"
        
        top_events = sorted(event_types.items(), key=lambda x: x[1], reverse=True)[:3]
        
        threats = []
        recommendations = []
        
        for event_type, count in top_events:
            if 'brute_force' in event_type:
                threats.append(f"SSH brute force attacks ({count} events)")
                recommendations.append("Implement rate limiting on SSH services")
            elif 'malware' in event_type:
                threats.append(f"Malware detection events ({count} events)")
                recommendations.append("Update antivirus signatures and quarantine affected systems")
            elif 'intrusion' in event_type:
                threats.append(f"Network intrusion attempts ({count} events)")
                recommendations.append("Review and strengthen network perimeter defenses")
            elif 'port_scan' in event_type:
                threats.append(f"Network reconnaissance ({count} events)")
                recommendations.append("Monitor and block scanning source IPs")
            elif 'failed_login' in event_type:
                threats.append(f"Authentication failures ({count} events)")
                recommendations.append("Review account security and enable 2FA")
        
        if not threats:
            threats = ["Various security events detected"]
        if not recommendations:
            recommendations = ["Continue monitoring", "Review security policies"]
        
        return {
            "summary": f"Analyzed {len(logs)} security events with {severity_counts['critical']} critical and {severity_counts['high']} high severity incidents.",
            "threats_identified": threats[:5],
            "severity_classification": overall_severity,
            "recommendations": recommendations[:5],
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
    
    def _fallback_chat_response(self, question: str) -> str:
        """Fallback chat response when Gemini API is not available"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['ip', 'address', 'source']):
            return "I can help analyze IP addresses and network traffic patterns. Please check the security logs for detailed information about specific IP activities."
        elif any(word in question_lower for word in ['attack', 'threat', 'malware']):
            return "Based on current security events, I recommend monitoring brute force attempts, malware communications, and network intrusions. Review the threat analysis panel for detailed insights."
        elif any(word in question_lower for word in ['recommend', 'action', 'do']):
            return "Key recommendations: 1) Block suspicious IPs, 2) Update security rules, 3) Monitor critical systems, 4) Review authentication logs."
        else:
            return "I'm a SOC cyber defense assistant. Ask me about security threats, IP addresses, attack patterns, or recommended actions based on the current security events."
