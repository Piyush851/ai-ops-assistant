import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Github, CloudRain, Activity, BrainCircuit, Zap, ShieldCheck } from 'lucide-react';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [agentStatus, setAgentStatus] = useState(''); 
  
  // NEW: State to track which agents are enabled
  const [agentConfig, setAgentConfig] = useState({
    planning: true,
    execution: true,
    verification: true
  });

  const ws = useRef(null);
  const messagesEndRef = useRef(null); 

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, agentStatus]);

  useEffect(() => {
    let reconnectInterval;

    const connectWebSocket = () => {
      ws.current = new WebSocket('ws://localhost:8000/ws/chat');

      ws.current.onopen = () => {
        console.log("Connected to AI Agents");
        setAgentStatus('');
      };

      ws.current.onmessage = (event) => {
        const response = JSON.parse(event.data);
        if (response.type === 'status') {
          setAgentStatus(response.message);
        } else if (response.type === 'result') {
          setAgentStatus('');
          setMessages((prev) => [...prev, { 
            role: 'assistant', 
            content: response.message,
            data_type: response.data_type,
            payload: response.payload
          }]);
        }
      };

      ws.current.onclose = () => {
        setAgentStatus('🔌 Connection lost. Reconnecting...');
        reconnectInterval = setTimeout(connectWebSocket, 3000);
      };
      
      ws.current.onerror = (err) => {
        console.error("WebSocket Error:", err);
        ws.current.close(); 
      };
    };

    connectWebSocket();

    return () => {
      clearTimeout(reconnectInterval);
      if (ws.current) ws.current.close();
    };
  }, []);

  const handleSendMessage = () => {
    if (!input.trim() || !ws.current || ws.current.readyState !== WebSocket.OPEN) return;
    
    setMessages((prev) => [...prev, { role: 'user', content: input }]);
    
    // NEW: Send a JSON payload with the prompt AND the configuration
    const payload = {
      prompt: input,
      config: agentConfig
    };
    ws.current.send(JSON.stringify(payload));
    
    setInput('');
  };

  // NEW: Helper to toggle agent settings
  const toggleConfig = (key) => {
    setAgentConfig(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 font-sans text-gray-800">
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-3 shadow-sm z-10">
        <div className="bg-blue-600 p-2 rounded-lg text-white">
          <Bot size={24} />
        </div>
        <div>
          <h1 className="text-xl font-bold tracking-tight text-gray-900">CodeWar 2.0</h1>
          <p className="text-xs text-gray-500 font-medium">Multi-Agent Ops Assistant</p>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto p-4 sm:p-6 w-full max-w-4xl mx-auto flex flex-col gap-6">
        {messages.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center text-gray-400 opacity-70">
            <Bot size={64} className="mb-4" />
            <p className="text-lg">Ask me to check GitHub repos or the weather...</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
            <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${msg.role === 'user' ? 'bg-indigo-100 text-indigo-600' : 'bg-blue-100 text-blue-600'}`}>
              {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
            </div>

            <div className={`flex flex-col max-w-[80%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`px-4 py-3 rounded-2xl shadow-sm ${msg.role === 'user' ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-white border border-gray-200 text-gray-800 rounded-tl-none'}`}>
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
              </div>

              {msg.data_type === 'weather' && msg.payload && (
                <div className="mt-3 w-64 bg-white p-4 rounded-xl border border-blue-100 shadow-sm flex flex-col gap-2">
                  <div className="flex items-center gap-2 text-blue-600 font-semibold border-b pb-2">
                    <CloudRain size={18} /> Current Weather
                  </div>
                  <div className="text-sm text-gray-700">
                    <p className="flex justify-between"><span>Temp:</span> <span className="font-medium">{msg.payload.temperature}</span></p>
                    <p className="flex justify-between"><span>Wind:</span> <span className="font-medium">{msg.payload.wind_speed}</span></p>
                  </div>
                </div>
              )}

              {msg.data_type === 'github' && msg.payload?.data && (
                <div className="mt-3 w-full max-w-md bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                  <div className="flex items-center gap-2 text-gray-800 font-semibold border-b pb-2 mb-3">
                    <Github size={18} /> Top Repositories
                  </div>
                  <div className="flex flex-col gap-3">
                    {msg.payload.data.map((repo, idx) => (
                      <div key={idx} className="p-3 bg-gray-50 rounded-lg border border-gray-100 hover:border-blue-300 transition-colors">
                        <div className="flex justify-between items-center mb-1">
                          <a href={`https://github.com/${repo.name}`} target="_blank" rel="noopener noreferrer" className="text-blue-600 font-medium hover:underline truncate pr-2">
                            {repo.name}
                          </a>
                          <span className="text-yellow-500 text-sm font-medium flex-shrink-0">⭐ {repo.stars}</span>
                        </div>
                        <p className="text-xs text-gray-500 line-clamp-2">{repo.description || "No description provided."}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {agentStatus && (
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-50 text-blue-400 flex items-center justify-center animate-pulse">
              <Activity size={18} />
            </div>
            <div className="flex items-center px-4 py-2 bg-transparent text-sm text-gray-500 italic animate-pulse">
              {agentStatus}
            </div>
          </div>
        )}
        <div ref={messagesEndRef} /> 
      </main>

      <footer className="bg-white border-t border-gray-200 p-4 flex flex-col gap-3">
        {/* NEW: Agent Control Panel */}
        <div className="max-w-4xl mx-auto w-full flex justify-center gap-4">
          <button 
            onClick={() => toggleConfig('planning')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium transition-colors border ${agentConfig.planning ? 'bg-blue-50 border-blue-200 text-blue-700' : 'bg-gray-50 border-gray-200 text-gray-400 hover:bg-gray-100'}`}
          >
            <BrainCircuit size={14} /> Planning
          </button>
          <button 
            onClick={() => toggleConfig('execution')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium transition-colors border ${agentConfig.execution ? 'bg-purple-50 border-purple-200 text-purple-700' : 'bg-gray-50 border-gray-200 text-gray-400 hover:bg-gray-100'}`}
          >
            <Zap size={14} /> Execution
          </button>
          <button 
            onClick={() => toggleConfig('verification')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium transition-colors border ${agentConfig.verification ? 'bg-green-50 border-green-200 text-green-700' : 'bg-gray-50 border-gray-200 text-gray-400 hover:bg-gray-100'}`}
          >
            <ShieldCheck size={14} /> Verification
          </button>
        </div>

        {/* Input Box */}
        <div className="max-w-4xl mx-auto w-full flex gap-3 relative">
          <input 
            type="text" 
            className="flex-1 border border-gray-300 rounded-full pl-6 pr-14 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-sm"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type your command here..."
            disabled={!!agentStatus && !agentStatus.includes('Connection lost')}
          />
          <button 
            onClick={handleSendMessage} 
            disabled={!input.trim() || (!!agentStatus && !agentStatus.includes('Connection lost'))}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors"
          >
            <Send size={18} />
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;