import os
from typing import List, Dict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        
    def analyze_logs(self, logs: List[Dict]) -> Dict:
        """
        Analyze security logs using OpenAI GPT to provide threat summary,
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
        
        prompt = f"""You are a SOC (Security Operations Center) cyber defense assistant. 
        Given these security logs: {log_text}
        
        Please provide a comprehensive analysis in the following format:
        1. SUMMARY: Brief overview of security events
        2. THREATS: List key threats identified
        3. SEVERITY: Overall severity classification (low/medium/high/critical)
        4. RECOMMENDATIONS: Specific actionable recommendations
        
        Be concise, technical, and focus on actionable intelligence for SOC analysts."""
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-4" if os.getenv("OPENAI_MODEL", "gpt-3.5-turbo") == "gpt-4" else "gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert cybersecurity analyst in a military SOC."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            return self._parse_ai_response(analysis_text, len(logs))
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_analysis(logs)
    
    def chat_response(self, question: str, logs: List[Dict]) -> str:
        """
        Generate a conversational response to analyst questions based on logs context.
        """
        log_context = self._format_logs_for_ai(logs[-50:])  # Use recent 50 logs for context
        
        prompt = f"""You are a SOC assistant. Answer the analyst's query based on these recent logs: {log_context}
        
        Analyst Question: {question}
        
        Provide a clear, concise SOC-style response. Include specific IP addresses, timestamps, and actionable recommendations when relevant."""
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful SOC assistant. Be concise and technical."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.4
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return f"I'm currently unable to access the AI analysis system. However, I can see we have {len(logs)} recent log entries. Please check the logs manually or try again later."
    
    def _format_logs_for_ai(self, logs: List[Dict]) -> str:
        """Format logs into a readable text for AI analysis."""
        formatted_logs = []
        for log in logs[-20:]:  # Use most recent 20 logs to avoid token limits
            formatted_logs.append(
                f"[{log.get('timestamp', 'Unknown')}] "
                f"{log.get('severity', 'unknown').upper()} - "
                f"{log.get('event_type', 'Unknown Event')} - "
                f"Source: {log.get('source_ip', 'Unknown')} -> "
                f"Dest: {log.get('dest_ip', 'Unknown')} - "
                f"Message: {log.get('message', 'No message')}"
            )
        return "\n".join(formatted_logs)
    
    def _parse_ai_response(self, ai_text: str, total_logs: int) -> Dict:
        """Parse AI response into structured format."""
        lines = ai_text.split('\n')
        
        summary = ""
        threats = []
        severity = "medium"
        recommendations = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.upper().startswith("1. SUMMARY") or line.upper().startswith("SUMMARY"):
                current_section = "summary"
                summary = line.split(":", 1)[-1].strip()
            elif line.upper().startswith("2. THREATS") or line.upper().startswith("THREATS"):
                current_section = "threats"
            elif line.upper().startswith("3. SEVERITY") or line.upper().startswith("SEVERITY"):
                current_section = "severity"
                severity_text = line.split(":", 1)[-1].strip().lower()
                if any(word in severity_text for word in ["critical", "high"]):
                    severity = "critical" if "critical" in severity_text else "high"
                elif "medium" in severity_text:
                    severity = "medium"
                else:
                    severity = "low"
            elif line.upper().startswith("4. RECOMMENDATIONS") or line.upper().startswith("RECOMMENDATIONS"):
                current_section = "recommendations"
            elif current_section == "threats" and (line.startswith("-") or line.startswith("•")):
                threats.append(line[1:].strip())
            elif current_section == "recommendations" and (line.startswith("-") or line.startswith("•")):
                recommendations.append(line[1:].strip())
            elif current_section == "summary" and summary == "":
                summary = line
        
        return {
            "summary": summary or "Analysis completed for recent security events",
            "threats_identified": threats or ["No specific threats identified"],
            "severity_classification": severity,
            "recommendations": recommendations or ["Continue monitoring", "Review logs for patterns"],
            "total_logs_analyzed": total_logs
        }
    
    def _fallback_analysis(self, logs: List[Dict]) -> Dict:
        """Fallback analysis when AI is unavailable."""
        severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        event_types = {}
        
        for log in logs:
            sev = log.get("severity", "low").lower()
            if sev in severity_counts:
                severity_counts[sev] += 1
            
            event_type = log.get("event_type", "unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        # Determine overall severity
        if severity_counts["critical"] > 0:
            overall_severity = "critical"
        elif severity_counts["high"] > 0:
            overall_severity = "high"
        elif severity_counts["medium"] > 0:
            overall_severity = "medium"
        else:
            overall_severity = "low"
        
        return {
            "summary": f"Analyzed {len(logs)} security events. Most common: {max(event_types.items(), key=lambda x: x[1])[0] if event_types else 'N/A'}",
            "threats_identified": list(event_types.keys())[:5],
            "severity_classification": overall_severity,
            "recommendations": [
                "Monitor high-priority events",
                "Review source IPs for patterns",
                "Check for repeated event types"
            ],
            "total_logs_analyzed": len(logs)
        }
