import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Sparkles, User, ArrowRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE_URL = 'http://localhost:5000';

interface Message {
  role: 'user' | 'model';
  content: string;
}

interface ChatInterviewProps {
  templateId: string;
  category: string;
  onComplete: (data: any) => void;
}

const ChatInterview: React.FC<ChatInterviewProps> = ({ templateId, category, onComplete }) => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'model', content: "Akwaaba! I'm your Academic Rebel mentor. Let's build a CV that truly represents your legacy. To start, what is your full name and current contact information?" }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const chatBoxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;

    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await axios.post(`${API_BASE_URL}/api/chat`, { message: userMsg }, { withCredentials: true });
      setMessages(prev => [...prev, { role: 'model', content: res.data.response }]);
      if (res.data.is_ready) {
        setIsReady(true);
      }
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, { role: 'model', content: "My connection to the Ministry is weak. Try sending that again!" }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-160px)] max-w-4xl mx-auto">
      {/* Mentor Header */}
      <div className="mb-4 flex justify-between items-center bg-brand-black text-white p-4 border-4 border-brand-black neo-shadow-lg">
        <div className="flex items-center gap-3">
          <div className="bg-brand-yellow p-1 border-2 border-white">
            <Sparkles className="text-brand-black w-6 h-6" />
          </div>
          <span className="font-headline font-black text-xl uppercase italic">The Rebel Mentor</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-[10px] font-black uppercase tracking-widest opacity-80">Online</span>
        </div>
      </div>

      {/* Chat Messages */}
      <div ref={chatBoxRef} className="flex-1 overflow-y-auto mb-4 p-4 space-y-8 flex flex-col scroll-smooth">
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-4 max-w-[85%] font-bold text-lg border-4 border-brand-black neo-shadow ${
                msg.role === 'user' 
                  ? 'self-end bg-brand-yellow' 
                  : 'self-start bg-white'
              }`}
            >
              <div className={`flex items-center gap-2 mb-2 text-xs uppercase tracking-widest font-black ${
                msg.role === 'user' ? 'justify-end text-black' : 'text-brand-gold'
              }`}>
                {msg.role === 'model' && <Sparkles size={14} />}
                {msg.role === 'user' ? 'You' : 'The Rebel'}
                {msg.role === 'user' && <User size={14} />}
              </div>
              {msg.content}
            </motion.div>
          ))}
          {isTyping && (
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }} 
              className="self-start bg-white p-4 border-4 border-brand-black flex gap-1"
            >
              <div className="w-2 h-2 bg-brand-black rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-brand-black rounded-full animate-bounce delay-100"></div>
              <div className="w-2 h-2 bg-brand-black rounded-full animate-bounce delay-200"></div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Input or Ready Action */}
      <div className="pb-6">
        {isReady ? (
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-brand-purple p-8 border-4 border-brand-black neo-shadow-lg flex flex-col items-center gap-4"
          >
            <span className="font-headline text-4xl font-black italic">Legacy Secured!</span>
            <p className="font-bold text-center text-lg">Your professional arsenal is ready for review.</p>
            <button 
              onClick={() => onComplete({})}
              className="w-full md:w-auto flex items-center gap-3 bg-white text-brand-black font-black px-12 py-5 border-4 border-brand-black neo-shadow-active uppercase tracking-widest text-xl group"
            >
              Review & Polish
              <ArrowRight className="group-hover:translate-x-2 transition-transform" />
            </button>
          </motion.div>
        ) : (
          <div className="relative group">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Message the mentor..."
              className="w-full p-5 pr-16 bg-white border-4 border-brand-black neo-shadow-lg font-black text-lg focus:outline-none focus:bg-brand-gold/5 transition-colors"
            />
            <button 
              onClick={handleSend}
              className="absolute right-3 top-1/2 -translate-y-1/2 bg-brand-gold p-3 border-4 border-brand-black neo-shadow-active hover:bg-brand-purple transition-all"
            >
              <Send className="text-white font-black" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInterview;
