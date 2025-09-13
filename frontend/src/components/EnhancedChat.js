import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, Send, Bot, User, Zap, Shield, Activity, Search } from 'lucide-react';

const EnhancedChat = ({ onSendMessage, chatHistory, loading }) => {
  const [currentMessage, setCurrentMessage] = useState('');
  const chatContainerRef = useRef(null);

  const suggestedQueries = [
    "Show me last 10 critical security breaches",
    "What's the biggest risk right now?",
    "Recommend mitigation steps for Zero-Day Exploit",
    "Which IPs should be blocked immediately?",
    "Analyze the current threat landscape",
    "Show anomalies from the last 24 hours",
    "What systems need immediate attention?",
    "Generate incident response plan"
  ];

  const quickActions = [
    { icon: <Shield className="w-4 h-4" />, text: "Security Status", query: "Give me a complete security status overview" },
    { icon: <Activity className="w-4 h-4" />, text: "Threat Analysis", query: "Analyze current threats and provide recommendations" },
    { icon: <Zap className="w-4 h-4" />, text: "Critical Incidents", query: "Show me all critical security incidents from today" },
    { icon: <Search className="w-4 h-4" />, text: "Anomaly Report", query: "Generate a detailed anomaly detection report" }
  ];

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleSendMessage = () => {
    if (!currentMessage.trim()) return;
    onSendMessage(currentMessage);
    setCurrentMessage('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleQuickAction = (query) => {
    onSendMessage(query);
  };

  const handleSuggestedQuery = (query) => {
    setCurrentMessage(query);
  };

  const formatMessage = (content) => {
    // Simple formatting for better readability
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br />')
      .replace(/- (.*?)(\n|$)/g, '• $1<br />');
  };

  return (
    <div className="bg-bg-secondary border border-border-primary rounded-lg shadow-lg flex flex-col h-[600px]">
      {/* Header */}
      <div className="flex items-center gap-3 p-6 border-b border-border-primary bg-bg-tertiary rounded-t-lg">
        <div className="p-2 bg-cyber-primary bg-opacity-20 rounded-lg">
          <MessageSquare className="w-6 h-6 text-cyber-primary" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-text-primary">AI Security Assistant</h3>
          <p className="text-sm text-text-muted">Ask me anything about your security posture</p>
        </div>
        <div className="flex items-center gap-1 text-sm text-cyber-success bg-cyber-success bg-opacity-20 px-2 py-1 rounded-full">
          <div className="w-2 h-2 bg-cyber-success rounded-full animate-pulse"></div>
          <span>Online</span>
        </div>
      </div>

      {/* Quick Actions */}
      {chatHistory.length === 0 && (
        <div className="p-4 border-b border-border-primary">
          <div className="text-sm font-medium text-text-primary mb-3">Quick Actions</div>
          <div className="grid grid-cols-2 gap-2">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={() => handleQuickAction(action.query)}
                className="flex items-center gap-2 p-2 text-sm text-text-primary bg-bg-tertiary rounded-lg hover:bg-bg-hover transition-colors border border-border-secondary"
              >
                {action.icon}
                <span>{action.text}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Chat Messages */}
      <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatHistory.length === 0 && (
          <div className="text-center text-text-muted mt-8">
            <Bot className="w-12 h-12 mx-auto mb-3 text-text-muted" />
            <h4 className="font-medium text-text-primary mb-2">Welcome to your AI Security Assistant</h4>
            <p className="text-sm text-text-muted">Ask me about threats, incidents, or security recommendations.</p>
          </div>
        )}

        {chatHistory.map((message, index) => (
          <div key={index} className={`flex gap-3 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex gap-3 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`p-2 rounded-full flex-shrink-0 ${
                message.type === 'user' 
                  ? 'bg-cyber-primary bg-opacity-20 text-cyber-primary' 
                  : 'bg-bg-tertiary text-text-muted'
              }`}>
                {message.type === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>
              <div className={`p-3 rounded-lg ${
                message.type === 'user'
                  ? 'bg-cyber-primary text-white'
                  : 'bg-bg-tertiary text-text-primary'
              }`}>
                <div 
                  className={`text-sm ${message.type === 'user' ? 'text-white' : 'text-text-primary'}`}
                  dangerouslySetInnerHTML={{ 
                    __html: message.type === 'ai' ? formatMessage(message.content) : message.content 
                  }}
                />
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 justify-start">
            <div className="p-2 bg-bg-tertiary text-text-muted rounded-full">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-bg-tertiary text-text-primary p-3 rounded-lg">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-cyber-primary rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-cyber-primary rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-cyber-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Suggested Queries */}
      {chatHistory.length === 0 && (
        <div className="p-4 border-t border-border-primary">
          <div className="text-sm font-medium text-text-primary mb-3">Suggested Questions</div>
          <div className="flex flex-wrap gap-2">
            {suggestedQueries.slice(0, 4).map((query, index) => (
              <button
                key={index}
                onClick={() => handleSuggestedQuery(query)}
                className="text-xs bg-cyber-primary bg-opacity-20 text-cyber-primary px-3 py-2 rounded-full hover:bg-opacity-30 transition-colors border border-cyber-primary border-opacity-30"
              >
                {query}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="p-4 border-t border-border-primary">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <textarea
              value={currentMessage}
              onChange={(e) => setCurrentMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about security incidents, threats, or get recommendations..."
              className="w-full p-3 bg-bg-tertiary border border-border-primary rounded-lg resize-none focus:ring-2 focus:ring-cyber-primary focus:border-cyber-primary text-text-primary placeholder-text-muted"
              rows="1"
              style={{ minHeight: '44px', maxHeight: '120px' }}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!currentMessage.trim() || loading}
            className="px-4 py-2 bg-cyber-primary text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default EnhancedChat;
