import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Save, Download, RefreshCcw, User, Briefcase, GraduationCap, Wrench, FileText } from 'lucide-react';
import { motion } from 'framer-motion';

const API_BASE_URL = 'http://localhost:5000';

interface CVData {
  full_name: string;
  professional_summary: string;
  contact: {
    email: string;
    phone: string;
    location: string;
  };
  experience: {
    company: string;
    role: string;
    dates: string;
    achievements: string[];
  }[];
  education: {
    institution: string;
    degree: string;
    year: string;
  }[];
  skills: string[];
}

interface CVEditorProps {
  onBack: () => void;
}

const CVEditor: React.FC<CVEditorProps> = ({ onBack }) => {
  const [data, setData] = useState<CVData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [previewKey, setPreviewKey] = useState(0); // Used to force iframe refresh

  useEffect(() => {
    // First, trigger the extraction API
    axios.post(`${API_BASE_URL}/api/refine`, {}, { withCredentials: true })
      .then(res => {
        setData(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error extracting data:", err);
        // Try to fallback to existing data if refinement fails
        axios.get(`${API_BASE_URL}/api/extracted_data`, { withCredentials: true })
          .then(res => {
            setData(res.data);
            setLoading(false);
          })
          .catch(() => setLoading(false));
      });
  }, []);

  const handleUpdate = (path: string, value: any) => {
    if (!data) return;
    const newData = { ...data };
    
    // Simple path handling for MVP
    if (path === 'full_name') newData.full_name = value;
    if (path === 'professional_summary') newData.professional_summary = value;
    if (path.startsWith('contact.')) {
        const field = path.split('.')[1] as keyof CVData['contact'];
        newData.contact[field] = value;
    }
    
    setData(newData);
  };

  const saveAndRefresh = async () => {
    if (!data) return;
    setSaving(true);
    try {
      await axios.post(`${API_BASE_URL}/preview`, data, { withCredentials: true });
      setPreviewKey(prev => prev + 1); // Refresh iframe
    } catch (err) {
      console.error("Save error:", err);
    } finally {
      setSaving(false);
    }
  };

  const downloadPDF = () => {
    window.location.href = `${API_BASE_URL}/download`;
  };

  if (loading) return (
    <div className="flex flex-col items-center justify-center h-96">
      <RefreshCcw className="animate-spin text-brand-gold mb-4" size={48} />
      <h2 className="font-headline text-3xl font-black italic">Extracting Your Legacy...</h2>
      <p className="font-bold text-stone-500 uppercase tracking-widest mt-2">The Rebel Mentor is organizing your files</p>
    </div>
  );

  if (!data) return <div>Failed to load data. Please try the interview again.</div>;

  return (
    <div className="flex flex-col lg:flex-row gap-8 h-[calc(100vh-140px)]">
      {/* Editor Panel */}
      <div className="w-full lg:w-1/2 overflow-y-auto pr-4 space-y-8 scroll-smooth">
        <div className="flex justify-between items-center bg-brand-black text-white p-4 border-4 border-brand-black neo-shadow">
          <h3 className="font-headline text-2xl font-black italic">Refine Your Arsenal</h3>
          <button 
            onClick={saveAndRefresh}
            disabled={saving}
            className="bg-brand-gold text-white px-4 py-2 border-2 border-white flex items-center gap-2 font-black uppercase tracking-widest text-xs hover:bg-brand-purple transition-colors disabled:opacity-50"
          >
            <Save size={16} />
            {saving ? 'Syncing...' : 'Sync Preview'}
          </button>
        </div>

        {/* Basic Info */}
        <section className="bg-white border-4 border-brand-black p-6 neo-shadow space-y-4">
          <div className="flex items-center gap-2 mb-2 text-brand-gold font-black uppercase tracking-widest text-sm">
            <User size={18} /> Basic Information
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-[10px] font-black uppercase tracking-widest text-stone-400 mb-1">Full Name</label>
              <input 
                value={data.full_name} 
                onChange={e => handleUpdate('full_name', e.target.value)}
                className="w-full p-3 border-2 border-brand-black font-bold focus:bg-brand-gold/5 outline-none" 
              />
            </div>
            <div>
                <label className="block text-[10px] font-black uppercase tracking-widest text-stone-400 mb-1">Email</label>
                <input 
                    value={data.contact.email} 
                    onChange={e => handleUpdate('contact.email', e.target.value)}
                    className="w-full p-3 border-2 border-brand-black font-bold outline-none" 
                />
            </div>
          </div>
          <div>
            <label className="block text-[10px] font-black uppercase tracking-widest text-stone-400 mb-1">Professional Summary</label>
            <textarea 
                rows={4}
                value={data.professional_summary} 
                onChange={e => handleUpdate('professional_summary', e.target.value)}
                className="w-full p-3 border-2 border-brand-black font-bold outline-none resize-none" 
            />
          </div>
        </section>

        {/* Placeholder for Experience/Education list editing */}
        <div className="p-8 border-4 border-dashed border-stone-300 text-center">
            <p className="font-bold text-stone-400 uppercase tracking-widest italic">Experience & Education List Editor Coming Soon</p>
            <p className="text-xs text-stone-400 mt-2">(Use the Chat to refine these sections for now)</p>
        </div>

        <button 
          onClick={downloadPDF}
          className="w-full bg-brand-purple text-brand-black font-black py-6 border-4 border-brand-black neo-shadow-active flex items-center justify-center gap-4 text-2xl uppercase tracking-tighter italic"
        >
          <Download size={32} strokeWidth={3} />
          Secure Your PDF
        </button>
      </div>

      {/* Preview Panel */}
      <div className="w-full lg:w-1/2 bg-stone-200 border-4 border-brand-black relative min-h-[500px] overflow-hidden">
        <div className="absolute top-4 left-4 z-10 bg-brand-black text-white px-3 py-1 font-black text-[10px] uppercase tracking-widest flex items-center gap-2">
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div> Live Preview
        </div>
        <iframe 
          key={previewKey}
          src={`${API_BASE_URL}/render_cv?t=${Date.now()}`} 
          className="w-full h-full bg-white"
        />
      </div>
    </div>
  );
};

export default CVEditor;
