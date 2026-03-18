import React, { useState, useRef } from 'react';
import axios from 'axios';
import confetti from 'canvas-confetti';
import { motion, AnimatePresence } from 'framer-motion';
import Hero from './components/Hero';
import Features from './components/Features';
import AnalysisBox from './components/AnalysisBox';
import ResultsPanel from './components/ResultsPanel';
import Timeline from './components/Timeline';
import { Shield, Github, Twitter, Menu, X } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://chainbreaker-api.onrender.com/api/analysis';

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const resultsRef = useRef(null);
  const analysisRef = useRef(null);

  const scrollToAnalysis = () => {
    analysisRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleAnalyze = async (input, mode) => {
    setIsLoading(true);
    setResult(null);

    try {
      let response;
      if (mode === 'text') {
        response = await axios.post(`${API_BASE_URL}/analyze-text`, { text: input });
      } else {
        const formData = new FormData();
        formData.append('file', input);
        response = await axios.post(`${API_BASE_URL}/analyze`, formData);
      }

      setResult(response.data);
      
      // If fake, trigger "chain breaking" celebration
      if (response.data.verdict === 'FALSE') {
        confetti({
          particleCount: 150,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#00D1FF', '#9D00FF', '#FF0055']
        });
      }

      // Smooth scroll to results
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);

    } catch (error) {
      console.error('Analysis failed', error);
      let errorMessage = 'Analysis failed. Please ensure the backend is running.';
      if (error.response && error.response.data && error.response.data.detail) {
        // Handle FastAPI validation/internal errors natively
        const detail = error.response.data.detail;
        if (typeof detail === 'string') {
          errorMessage = `Backend Error: ${detail}`;
        } else if (Array.isArray(detail)) {
          errorMessage = `Validation Error: ${detail.map(e => e.msg).join(', ')}`;
        } else {
          errorMessage = `Backend Error: ${JSON.stringify(detail)}`;
        }
      } else if (error.message) {
        errorMessage = `Network Error: ${error.message}`;
      }
      alert(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 px-6 py-4 flex justify-between items-center backdrop-blur-md border-b border-white/5 bg-black/20">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-brand-blue to-brand-purple flex items-center justify-center">
            <Shield className="text-white" size={24} />
          </div>
          <span className="text-2xl font-black tracking-tighter text-white uppercase italic">
            Chain<span className="text-brand-cyan">Breaker</span>
          </span>
        </div>

        <div className="hidden md:flex items-center gap-8 text-sm font-bold tracking-widest text-premium-light/60 uppercase">
          <a href="#" className="hover:text-brand-cyan transition-colors">Intelligence</a>
          <a href="#" className="hover:text-brand-cyan transition-colors">Mission</a>
          <a href="#" className="hover:text-brand-cyan transition-colors">Global Metrics</a>
          <button className="px-6 py-2 rounded-full border border-white/10 hover:bg-white/5 transition-all">
            Connect API
          </button>
        </div>

        <button className="md:hidden text-white" onClick={() => setIsMenuOpen(!isMenuOpen)}>
          {isMenuOpen ? <X /> : <Menu />}
        </button>
      </nav>

      {/* Main Content */}
      <main>
        <Hero onGetStarted={scrollToAnalysis} />
        
        <div ref={analysisRef} className="py-24 px-4 bg-black relative z-10">
          <div className="max-w-4xl mx-auto text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-black mb-4 glow-text">Analysis Laboratory</h2>
            <p className="text-premium-light/40">Feed the neural engine suspicious claims or audio evidence.</p>
          </div>
          
          <AnalysisBox onAnalyze={handleAnalyze} isLoading={isLoading} />
          
          <div ref={resultsRef}>
            <AnimatePresence>
              {result && <ResultsPanel result={result} />}
            </AnimatePresence>
          </div>
        </div>

        <Features />
        <Timeline />

        {/* Impact Dashboard Preview */}
        <section className="py-32 bg-gradient-to-b from-black to-[#0A0A0A] px-4">
          <div className="max-w-6xl mx-auto card-premium p-12 border-brand-cyan/20 bg-brand-cyan/5">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
              <div>
                <h3 className="text-6xl font-black text-brand-cyan mb-2">1,204,502</h3>
                <p className="text-premium-light/40 uppercase tracking-[0.2em] font-bold text-sm">Fake Messages Halted</p>
              </div>
              <div>
                <h3 className="text-6xl font-black text-brand-purple mb-2">99.82%</h3>
                <p className="text-premium-light/40 uppercase tracking-[0.2em] font-bold text-sm">LLM Accuracy Rate</p>
              </div>
              <div>
                <h3 className="text-6xl font-black text-brand-blue mb-2">420ms</h3>
                <p className="text-premium-light/40 uppercase tracking-[0.2em] font-bold text-sm">Avg Reaction Time</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="py-12 border-t border-white/5 bg-black px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:row justify-between items-center gap-8">
          <div className="flex items-center gap-2">
            <Shield className="text-brand-cyan" size={20} />
            <span className="font-bold tracking-tighter text-premium-light/40 uppercase">ChainBreaker AI © 2026</span>
          </div>
          
          <div className="flex gap-6">
            <Github className="text-premium-light/40 hover:text-white transition-colors cursor-pointer" />
            <Twitter className="text-premium-light/40 hover:text-white transition-colors cursor-pointer" />
          </div>

          <div className="text-xs text-premium-light/20 font-medium">
            BUILT FOR THE FUTURE OF INFORMATION INTEGRITY
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
