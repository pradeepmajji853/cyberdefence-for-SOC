# AI-Powered Cyber Defense Assistant 🛡️

A hackathon demo showcasing an AI-powered Security Operations Center (SOC) dashboard for military cyber defense.

## 🚀 Quick Start

1. **Setup Environment**:
   ```bash
   ./setup_demo.sh
   ```

2. **Add OpenAI API Key**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`

3. **Start Backend** (Terminal 1):
   ```bash
   python main.py
   ```

4. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm start
   ```

5. **Generate Demo Data** (Terminal 3):
   ```bash
   python fake_log_generator.py
   ```

6. **Open Dashboard**: http://localhost:3000

## 🎯 Demo Features

### Backend (FastAPI)
- **POST /logs** - Accept JSON security logs
- **GET /logs** - Retrieve recent logs with filtering
- **GET /analysis** - AI-powered threat analysis and recommendations
- **POST /chat** - Natural language SOC assistant
- **GET /stats** - Dashboard statistics

### AI Layer
- OpenAI GPT integration for threat analysis
- Automated severity classification
- Actionable security recommendations
- Conversational SOC assistant

### Frontend (React + Tailwind)
- **Live Log Stream** - Real-time security events
- **AI Threat Analysis** - Automated threat summarization
- **Interactive Dashboard** - Charts and statistics
- **SOC Assistant Chat** - Natural language queries
- **Quick Actions** - Simulated response buttons

## 🔧 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │   FastAPI Backend │    │   OpenAI API    │
│   (Port 3000)    │◄──►│   (Port 8000)     │◄──►│   (GPT Model)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   SQLite Database │
                       │   (security_logs) │
                       └──────────────────┘
```

## 🎭 Demo Scenarios

The fake log generator creates realistic scenarios:

- **Brute Force Attacks** - SSH login attempts
- **Port Scanning** - Network reconnaissance
- **Malware Detection** - C2 communications
- **DDoS Attacks** - Traffic flooding
- **Intrusion Attempts** - System compromise
- **Failed Logins** - Authentication failures

## 🎨 UI Features

- **Dark SOC Theme** - Military-style interface
- **Real-time Updates** - Auto-refreshing dashboard
- **Severity Classification** - Color-coded threat levels
- **Timeline Charts** - Activity visualization
- **Responsive Design** - Works on all screen sizes

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: React, Tailwind CSS, Recharts
- **AI**: OpenAI GPT-3.5/GPT-4
- **Icons**: Lucide React
- **Charts**: Recharts library

## 📊 API Endpoints

### Security Logs
- `POST /logs` - Create security log entry
- `GET /logs?limit=50&severity=high&hours_back=24` - Get filtered logs

### AI Analysis
- `GET /analysis?hours_back=2` - Get threat analysis
- `POST /chat` - Chat with SOC assistant

### Statistics
- `GET /stats` - Dashboard statistics
- `GET /health` - Health check

## 🎯 Hackathon Demo Flow

1. **Start Systems** - Launch backend, frontend, log generator
2. **Generate Historical Data** - Populate with 50+ fake logs
3. **Show Live Dashboard** - Real-time log stream and AI analysis
4. **Demonstrate AI Chat** - Ask questions about threats
5. **Simulate Incident** - Generate critical alerts
6. **Show Recommendations** - AI-generated response actions

## 🔒 Security Features

- CORS protection
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy
- Rate limiting ready (can be added)
- Environment variable configuration

## 🚀 Production Readiness

To make this production-ready, consider:
- Authentication and authorization
- Rate limiting and API quotas
- Database scaling (PostgreSQL)
- Logging and monitoring
- Docker containerization
- CI/CD pipeline
- Security scanning
- Load balancing

## 🤝 Team Demo Tips

1. **Presenter Setup**: Have all terminals ready
2. **Backup Plan**: Pre-populate database if API fails
3. **Story Flow**: Start with empty dashboard, add incidents
4. **Interactive Demo**: Let audience ask chatbot questions
5. **Technical Deep-dive**: Show code structure if requested

---

**Built for Military SOC Demo | FastAPI + React + AI**
