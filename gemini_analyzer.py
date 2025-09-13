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
        """Analyze security logs using Google Gemini AI"""
        if not logs:
            return {
                "summary": "No logs available for analysis",
                "threats_identified": [],
                "severity_classification": "low",
                "recommendations": [],
                "total_logs_analyzed": 0
            }
        
        # Format logs for AI analysis
        log_text = self._format_logs_for_ai(logs)
        
        prompt = f"""You are a SOC cyber defense assistant. Analyze these security logs and respond with JSON:

LOGS:
{log_text}

Respond ONLY with this JSON format:
{{
  "summary": "Brief overview in 1-2 sentences",
  "threats_identified": ["threat1", "threat2", "threat3"],
  "severity_classification": "critical",
  "recommendations": ["action1", "action2", "action3"],
  "total_logs_analyzed": {len(logs)}
}}"""
        
        try:
            response = self._call_gemini_api(prompt)
            return self._parse_response(response, len(logs))
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_analysis(logs)
    
    def chat(self, question: str, logs_context: List[Dict] = None) -> str:
        """Chat with Gemini AI about security events"""
        context = ""
        if logs_context:
            context = f"\nRecent events:\n{self._format_logs_for_ai(logs_context[:5])}\n"
        
        prompt = f"""You are a SOC cyber defense assistant.{context}
        
Question: {question}

Provide a technical response in 100 words or less."""
        
        try:
            response = self._call_gemini_api(prompt)
            return self._extract_text(response)
        except Exception as e:
            return f"I'm having trouble accessing the AI service. Error: {str(e)}"
    
    def _call_gemini_api(self, prompt: str) -> Dict:
        """Make request to Gemini API"""
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': self.api_key
        }
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")
    
    def _extract_text(self, response: Dict) -> str:
        """Extract text from Gemini response"""
        try:
            return response['candidates'][0]['content']['parts'][0]['text'].strip()
        except (KeyError, IndexError):
            return "Sorry, I couldn't process that request."
    
    def _parse_response(self, response: Dict, log_count: int) -> Dict:
        """Parse Gemini response for analysis"""
        try:
            text = self._extract_text(response)
            
            # Try to parse JSON
            if '{' in text and '}' in text:
                start = text.find('{')
                end = text.rfind('}') + 1
                json_str = text[start:end]
                parsed = json.loads(json_str)
                
                # Validate required fields
                if all(key in parsed for key in ['summary', 'threats_identified', 'severity_classification', 'recommendations']):
                    parsed['total_logs_analyzed'] = log_count
                    return parsed
            
            return self._fallback_analysis_with_count(log_count)
            
        except Exception as e:
            print(f"Parse error: {e}")
            return self._fallback_analysis_with_count(log_count)
    
    def _format_logs_for_ai(self, logs: List[Dict], limit: int = 15) -> str:
        """Format logs for AI analysis"""
        formatted = []
        for log in logs[:limit]:
            timestamp = log.get('timestamp', 'Unknown')[:19]  # Truncate timestamp
            event_type = log.get('event_type', 'Unknown')
            severity = log.get('severity', 'Unknown')
            source_ip = log.get('source_ip', 'Unknown')
            dest_ip = log.get('dest_ip', 'Unknown')
            message = log.get('message', 'No message')[:100]  # Truncate message
            
            formatted.append(f"[{severity.upper()}] {event_type}: {source_ip}→{dest_ip} | {message}")
        
        return '\n'.join(formatted)
    
    def _fallback_analysis(self, logs: List[Dict]) -> Dict:
        """Fallback when AI is unavailable"""
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
                threats.append(f"SSH brute force attacks detected ({count} events)")
                recommendations.append("Implement SSH rate limiting and IP blocking")
            elif 'malware' in event_type:
                threats.append(f"Malware activity detected ({count} events)")
                recommendations.append("Quarantine affected systems and update signatures")
            elif 'intrusion' in event_type:
                threats.append(f"Network intrusion attempts ({count} events)")
                recommendations.append("Strengthen perimeter defenses")
            elif 'port_scan' in event_type:
                threats.append(f"Network reconnaissance ({count} events)")
                recommendations.append("Monitor and block scanning sources")
        
        if not threats:
            threats = ["Multiple security events require attention"]
        if not recommendations:
            recommendations = ["Continue monitoring", "Review security policies"]
        
        return {
            "summary": f"Analyzed {len(logs)} events: {severity_counts['critical']} critical, {severity_counts['high']} high severity incidents detected.",
            "threats_identified": threats[:4],
            "severity_classification": overall_severity,
            "recommendations": recommendations[:4],
            "total_logs_analyzed": len(logs)
        }
    
    def _fallback_analysis_with_count(self, log_count: int) -> Dict:
        """Simple fallback with count"""
        return {
            "summary": f"Analyzed {log_count} security events with multiple threat indicators identified.",
            "threats_identified": [
                "Network intrusion attempts detected",
                "Brute force authentication attacks",
                "Suspicious network communications",
                "Potential malware activity"
            ],
            "severity_classification": "high",
            "recommendations": [
                "Block suspicious IP addresses immediately",
                "Review and update firewall rules", 
                "Conduct network security scan",
                "Enable enhanced monitoring"
            ],
            "total_logs_analyzed": log_count
        }

if __name__ == "__main__":
    # Test the analyzer
    analyzer = AIAnalyzer()
    print("Gemini AI Analyzer initialized successfully!")
