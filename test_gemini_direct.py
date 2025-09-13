#!/usr/bin/env python3
"""
Direct Gemini API Test Script
Tests if Gemini API is responding or if we're hitting quota limits
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_direct():
    """Test Gemini API directly with a simple prompt"""
    api_key = os.getenv("GEMINI_API_KEY", "AIzaSyBhojJ0wFVlbgnjkNeTU7aMqnETp63rRLI")
    base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Test prompt: Analyze this security log: '2025-01-01 10:00:00 - Failed SSH login from 192.168.1.100'. Respond with JSON: {\"threat\": \"description\", \"severity\": \"level\"}"
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 512
        }
    }
    
    try:
        print("🔍 Testing Gemini API directly...")
        response = requests.post(base_url, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Gemini API is working!")
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Extract the text response
            try:
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                print(f"\n📝 AI Response Text:\n{text_response}")
                return True
            except (KeyError, IndexError) as e:
                print(f"⚠️ Response structure unexpected: {e}")
                return False
                
        elif response.status_code == 429:
            print("❌ Quota exceeded (429) - API limit reached")
            print("💡 This explains why we're seeing fallback responses")
            print(f"Response: {response.text}")
            return False
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_with_realistic_log():
    """Test with a realistic security log analysis prompt"""
    api_key = os.getenv("GEMINI_API_KEY", "AIzaSyBhojJ0wFVlbgnjkNeTU7aMqnETp63rRLI")
    base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }
    
    prompt = """Analyze these security logs:
2025-01-01 10:00:00 - SSH brute force attack from 203.0.113.45 (5 attempts)
2025-01-01 10:05:00 - Malware detected: Trojan.Win32.Agent
2025-01-01 10:10:00 - Unauthorized access attempt to admin portal

Provide analysis in JSON format:
{
  "summary": "brief overview",
  "threats_identified": ["threat1", "threat2"],
  "severity_classification": "critical",
  "recommendations": ["action1", "action2"]
}"""
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}
    }
    
    try:
        print("\n🔍 Testing with realistic security log analysis...")
        response = requests.post(base_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            print("✅ Realistic analysis test successful!")
            print(f"📝 AI Analysis Response:\n{text_response}")
            return True
        else:
            print(f"❌ Realistic test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Realistic test error: {e}")
        return False

if __name__ == "__main__":
    print("🤖 GEMINI API DIRECT TEST")
    print("=" * 40)
    
    # Test basic API connectivity
    basic_works = test_gemini_direct()
    
    if basic_works:
        # Test with realistic security analysis
        test_with_realistic_log()
    
    print("\n" + "=" * 40)
    print("📊 ANALYSIS:")
    if basic_works:
        print("✅ Gemini API is responding correctly")
        print("🔧 The system should be using real AI responses")
        print("💡 Check if fallback is being triggered unnecessarily")
    else:
        print("❌ Gemini API is not responding (likely quota exceeded)")
        print("🔄 System will use intelligent fallback analysis")
        print("💰 Consider upgrading to paid tier for unlimited API access")
