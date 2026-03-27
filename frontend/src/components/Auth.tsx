import React, { useState } from 'react';
import axios from 'axios';
import { Mail, Lock, LogIn, UserPlus, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

const API_BASE_URL = 'http://localhost:5000';

interface AuthProps {
  onAuthSuccess: (user: any) => void;
}

const Auth: React.FC<AuthProps> = ({ onAuthSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const endpoint = isLogin ? '/api/login' : '/api/signup';
    
    try {
      const res = await axios.post(`${API_BASE_URL}${endpoint}`, { email, password }, { withCredentials: true });
      onAuthSuccess(res.data.user);
    } catch (err: any) {
      setError(err.response?.data?.error || "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh]">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md bg-white border-4 border-brand-black p-8 neo-shadow-lg"
      >
        <div className="flex flex-col items-center mb-8">
          <div className="bg-brand-gold p-3 border-4 border-brand-black neo-shadow mb-4">
            <Sparkles className="text-white w-8 h-8" />
          </div>
          <h2 className="font-headline text-4xl font-black italic">
            {isLogin ? 'Welcome Back' : 'Join the Rebellion'}
          </h2>
          <p className="font-bold text-stone-500 uppercase tracking-widest text-xs mt-2">
            {isLogin ? 'Your legacy awaits its next chapter' : 'Start building your professional arsenal'}
          </p>
        </div>

        {error && (
          <div className="bg-red-100 border-2 border-red-500 text-red-700 p-3 mb-6 font-bold text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-[10px] font-black uppercase tracking-widest text-stone-400 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-400" size={18} />
              <input 
                type="email"
                required
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="w-full p-3 pl-10 border-2 border-brand-black font-bold focus:bg-brand-gold/5 outline-none"
                placeholder="rebel@educv.gh"
              />
            </div>
          </div>

          <div>
            <label className="block text-[10px] font-black uppercase tracking-widest text-stone-400 mb-1">Secret Key</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-400" size={18} />
              <input 
                type="password"
                required
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="w-full p-3 pl-10 border-2 border-brand-black font-bold focus:bg-brand-gold/5 outline-none"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button 
            type="submit"
            disabled={loading}
            className="w-full bg-brand-gold text-white font-black py-4 border-4 border-brand-black neo-shadow-active flex items-center justify-center gap-3 uppercase tracking-widest text-lg disabled:opacity-50"
          >
            {loading ? (
              <RefreshCcw className="animate-spin" size={20} />
            ) : isLogin ? (
              <LogIn size={20} />
            ) : (
              <UserPlus size={20} />
            )}
            {isLogin ? 'Login to Portal' : 'Create Legacy Account'}
          </button>
        </form>

        <div className="mt-8 text-center">
          <button 
            onClick={() => setIsLogin(!isLogin)}
            className="text-sm font-black uppercase tracking-widest text-brand-gold hover:text-brand-purple transition-colors"
          >
            {isLogin ? "New here? Create an account" : "Already a rebel? Sign in here"}
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default Auth;
