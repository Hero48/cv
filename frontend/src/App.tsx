import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { School, ArrowLeft } from 'lucide-react';
import ChatInterview from './components/ChatInterview';

const API_BASE_URL = 'http://localhost:5000';

interface Template {
  id: string;
  name: string;
  category: string;
  style: string;
  preview_url: string;
}

type AppStep = 'gallery' | 'chat' | 'refine' | 'preview';

function App() {
  const [step, setStep] = useState<AppStep>('gallery');
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<{id: string, category: string} | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_BASE_URL}/api/templates`)
      .then(res => {
        setTemplates(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching templates:", err);
        setLoading(false);
      });
  }, []);

  const handleSelectTemplate = (id: string, category: string) => {
    setSelectedTemplate({ id, category });
    setStep('chat');
  };

  const handleInterviewComplete = () => {
    setStep('refine');
  };

  return (
    <div className="min-h-screen bg-[#f6f6f6] text-[#2d2f2f] font-body">
      {/* Header */}
      <header className="sticky top-0 z-50 flex justify-between items-center w-full px-6 py-4 bg-[#f6f6f6] border-b-4 border-[#2d2f2f]">
        <div className="flex items-center gap-2">
          {step !== 'gallery' && (
            <button 
              onClick={() => setStep(step === 'chat' ? 'gallery' : 'chat')}
              className="mr-2 p-2 hover:bg-stone-200 transition-colors"
            >
              <ArrowLeft size={24} />
            </button>
          )}
          <School className="text-[#715800] w-8 h-8" />
          <span className="text-2xl font-black tracking-tighter font-headline">EduCV</span>
        </div>
        <div className="hidden md:flex items-center gap-6">
          <button onClick={() => setStep('gallery')} className={`font-bold ${step === 'gallery' ? 'text-[#715800]' : ''}`}>Templates</button>
          <a className="font-bold hover:bg-[#f8cd50] px-3 py-1 transition-all" href="#">Pricing</a>
        </div>
        <button className="bg-brand-gold text-white px-6 py-2 font-black uppercase tracking-wider text-sm border-2 border-[#2d2f2f] neo-shadow neo-shadow-active">
          Help
        </button>
      </header>

      <main className="px-6 md:px-20 py-12">
        {step === 'gallery' && (
          <>
            <div className="mb-12 border-l-8 border-brand-gold pl-6">
              <h2 className="font-headline text-5xl font-black italic mb-2">Select Your Style</h2>
              <p className="text-xl text-stone-600 font-medium">Choose a template that reflects your professional identity.</p>
            </div>

            {loading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-gold"></div>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                {templates.map(template => (
                  <div key={template.id} className="bg-white border-4 border-brand-black neo-shadow-lg flex flex-col group hover:-translate-y-2 transition-all">
                    <div className="aspect-[3/4] bg-stone-100 border-b-4 border-brand-black overflow-hidden relative">
                      <iframe 
                        src={`${API_BASE_URL}${template.preview_url}`} 
                        className="w-[1000px] h-[1414px] border-none transform scale-[0.3] origin-top-left pointer-events-none absolute top-0 left-0"
                      />
                      <div className="absolute inset-0 bg-brand-gold/0 group-hover:bg-brand-gold/40 transition-all flex items-center justify-center backdrop-blur-[1px] group-hover:backdrop-blur-none">
                        <button 
                          onClick={() => handleSelectTemplate(template.id, template.category)}
                          className="bg-white text-brand-black font-black px-6 py-3 border-2 border-brand-black neo-shadow opacity-0 group-hover:opacity-100 transition-all uppercase tracking-wider scale-90 group-hover:scale-100"
                        >
                          Select Template
                        </button>
                      </div>
                    </div>
                    <div className="p-4 flex flex-col">
                      <span className="font-headline font-black text-xl truncate mb-1">{template.name}</span>
                      <span className="text-sm font-bold text-stone-500 uppercase tracking-widest">{template.style}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {step === 'chat' && selectedTemplate && (
          <ChatInterview 
            templateId={selectedTemplate.id} 
            category={selectedTemplate.category} 
            onComplete={handleInterviewComplete}
          />
        )}

        {step === 'refine' && (
          <div className="flex flex-col items-center justify-center h-64 border-4 border-dashed border-stone-300">
            <h2 className="text-2xl font-black mb-4">Refinement Phase</h2>
            <p className="text-stone-500 font-bold uppercase tracking-widest">Coming Soon: Interactive Editor</p>
            <button 
              onClick={() => setStep('gallery')}
              className="mt-6 bg-brand-black text-white px-8 py-3 font-black uppercase tracking-widest neo-shadow-active"
            >
              Back to Start
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
