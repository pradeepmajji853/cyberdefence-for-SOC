# 🛡️ AI-Powered Cyber Defense Assistant for SOC

A comprehensive Military Security Operations Center (SOC) dashboard with AI-powered log analysis, threat detection, and intelligent chatbot capabilities using Google Gemini AI.

## 🚀 Features

### 🔍 **Comprehensive Security Analysis**
- **Real-time log analysis** with AI-powered threat detection
- **169+ persistent security logs** with demo data for testing
- **Gemini AI integration** for intelligent threat assessment
- **Severity classification** (Critical, High, Medium, Low)
- **Automated threat identification** and recommendations

### 🤖 **Intelligent AI Assistant**
- **Smart question detection** for IP blocking, threats, and recommendations
- **Specific data-driven responses** with actual IP addresses and threat details
- **Professional SOC-grade analysis** with actionable intelligence
- **Context-aware responses** based on actual log data

### 📊 **Professional Dashboard**
- **Military-grade UI/UX** with dark theme and professional styling
- **Interactive charts and visualizations** for threat distribution
- **Real-time monitoring** with auto-refresh capabilities
- **Comprehensive statistics** and trend analysis

### 🎯 **Action-Oriented Interface**
- **In-section response display** for analysis actions
- **Specific IP blocking recommendations** with threat levels
- **Host isolation guidance** for compromised systems
- **Incident escalation workflows** with detailed threat analysis

## 🏗️ Architecture

```
📦 Cyber Defense Assistant
├── 🔧 Backend (FastAPI + SQLite)
│   ├── main.py - API server with endpoints
│   ├── ai_analyzer.py - Gemini AI integration
│   ├── database.py - SQLite database models
│   └── models.py - Pydantic data models
├── 🎨 Frontend (React + TailwindCSS)
│   ├── src/App.js - Main application component
│   ├── src/api.js - API client functions
│   └── src/index.css - Professional styling
└── 📊 Database
    └── cyber_defense.db - SQLite with persistent logs
```

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 14+**
- **npm or yarn**
- **Google Gemini AI API Key**

## ⚡ Quick Start

### 1. **Backend Setup**

```bash
# Clone the repository
git clone https://github.com/pradeepmajji853/cyberdefence-for-SOC.git
cd cyberdefence-for-SOC

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Initialize database with demo data
python init_database.py

# Start the backend server
python main.py
```

The backend will be available at `http://localhost:8000`

### 2. **Frontend Setup**

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 🔐 Environment Configuration

Create a `.env` file in the root directory:

```env
# Google Gemini AI API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# CORS Origins (Optional)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002

# Database URL (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///./cyber_defense.db
```

## 📡 API Endpoints

### **Core Endpoints**
- `GET /` - Health check and API status
- `GET /logs` - Retrieve security logs with filtering
- `POST /logs` - Create new security log entries
- `GET /analysis` - AI-powered threat analysis
- `POST /chat` - Intelligent chat interface
- `GET /stats` - System statistics and metrics

### **Analysis Features**
- **Comprehensive Analysis**: Processes up to 200 logs over 7-day timeframe
- **Smart Sampling**: Prioritizes critical and high-severity events
- **Statistical Analysis**: IP frequency tracking and event categorization
- **Actionable Intelligence**: Specific recommendations with implementation steps

## 🤖 AI Capabilities

### **Specialized Chat Intelligence**
1. **IP Blocking Queries**: "What IPs should be blocked?" → Returns specific malicious IPs
2. **Threat Analysis**: "What are the critical threats?" → Detailed threat breakdown
3. **Recommendations**: "What actions should we take?" → Specific SOC recommendations
4. **General Analysis**: Context-aware responses with log citations

### **Analysis Features**
- **Pattern Recognition**: Identifies brute force, malware, intrusions, and anomalies
- **Risk Assessment**: Automated severity classification and priority ranking
- **Threat Intelligence**: Correlates events to identify coordinated attacks
- **Actionable Output**: Specific IPs, timestamps, and mitigation steps

## 🎯 Usage Examples

### **Query the AI Assistant**
```
User: "WHAT ARE THE IPS THAT ARE NEEDED TO BE BLOCKED"
AI: 🚨 IMMEDIATE IP BLOCKING RECOMMENDATIONS:

1. 203.0.113.45 (CRITICAL RISK)
   - Events: 15 total (12 critical, 3 high)
   - Attacks: brute_force_ssh, malware_detection
   - Action: BLOCK IMMEDIATELY

2. 192.168.1.75 (HIGH RISK)
   - Events: 8 total (0 critical, 8 high)
   - Attacks: intrusion_attempt
   - Action: BLOCK IMMEDIATELY
```

### **Analysis Actions**
- **Block All IPs**: Returns specific malicious IP addresses with threat levels
- **Isolate Hosts**: Identifies compromised systems requiring isolation
- **Escalate Incident**: Lists critical events needing immediate attention
- **Enhanced Monitor**: Recommends monitoring strategies for threat indicators

## 🛠️ Development

### **Adding New Features**
1. **Backend**: Add endpoints in `main.py`, enhance AI logic in `ai_analyzer.py`
2. **Frontend**: Modify `App.js` for UI changes, update `api.js` for new endpoints
3. **Database**: Update models in `database.py` and `models.py`

### **Testing**
```bash
# Test the backend API
python verify_system.py

# Test AI functionality
python test_perfect_analysis.py

# Test Gemini AI integration
python verify_gemini_integration.py
```

## 📊 Demo Data

The system includes 169+ persistent security logs with various threat types:
- **Critical Events**: Advanced persistent threats, zero-day exploits, nation-state actors
- **High Severity**: Brute force attacks, malware detections, intrusion attempts
- **Medium/Low**: Reconnaissance, failed authentications, routine scans

## 🔒 Security Features

- **Input Validation**: Comprehensive request validation and sanitization
- **Error Handling**: Graceful error management with proper logging
- **Rate Limiting**: Protection against abuse and DoS attempts
- **Secure Headers**: CORS configuration and security headers
- **Environment Variables**: Secure API key and configuration management

## 🎨 UI/UX Features

### **Professional Military Interface**
- **Dark theme** with cyber security aesthetics
- **Real-time indicators** for system status and threat levels
- **Interactive visualizations** with threat distribution charts
- **Responsive design** for desktop and tablet usage

### **Enhanced User Experience**
- **Loading states** with professional animations
- **Error handling** with clear user feedback
- **Auto-refresh** capabilities for real-time monitoring
- **Action feedback** with in-section response display

## 🚀 Deployment

### **Production Deployment**
1. **Backend**: Deploy FastAPI with Uvicorn/Gunicorn on cloud platforms
2. **Frontend**: Build and serve React app with nginx or CDN
3. **Database**: Use PostgreSQL or cloud database for production
4. **Environment**: Set production environment variables and security configurations

### **Docker Support** (Coming Soon)
```bash
# Build and run with Docker
docker-compose up --build
```

## 📈 Roadmap

- [ ] **Docker containerization** for easy deployment
- [ ] **PostgreSQL support** for production environments
- [ ] **User authentication** and role-based access control
- [ ] **Advanced threat intelligence** integration
- [ ] **Email/SMS alerting** for critical events
- [ ] **Export functionality** for reports and logs
- [ ] **Multi-tenant support** for enterprise deployments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Pradeep Kumar Majji**
- GitHub: [@pradeepmajji853](https://github.com/pradeepmajji853)
- Email: pradeepmajji853@gmail.com

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent threat analysis
- **FastAPI** for the robust backend framework
- **React & TailwindCSS** for the professional frontend
- **SQLAlchemy** for database management
- **Lucide React** for beautiful icons

---

## 🔥 **Key Highlights**

- ✅ **169+ Persistent Security Logs** with realistic threat data
- ✅ **Google Gemini AI Integration** for intelligent analysis
- ✅ **Professional SOC Interface** with military-grade styling
- ✅ **Specific Intelligence Responses** with actual IP addresses and threat details
- ✅ **Real-time Analysis** with comprehensive threat assessment
- ✅ **Action-oriented Interface** with in-section response display

**🛡️ Perfect for Security Operations Centers, Cyber Defense Teams, and Security Analysts!**
