import React from 'react';
import { motion } from 'framer-motion';

const Hero = ({ onGetStarted }) => {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center pt-20 px-4 overflow-hidden">
      {/* Animated Background Elements */}
      <div className="mesh-gradient" />
      
      {/* Background Animation: Breaking Chains Placeholder */}
      <div className="absolute inset-0 z-0 opacity-20 pointer-events-none">
        <svg width="100%" height="100%" viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="grad1" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
              <stop offset="0%" style={{ stopColor: '#00D1FF', stopOpacity: 0.2 }} />
              <stop offset="100%" style={{ stopColor: 'transparent', stopOpacity: 0 }} />
            </radialGradient>
          </defs>
          <motion.circle 
            cx="500" cy="500" r="400" 
            fill="url(#grad1)" 
            animate={{ scale: [1, 1.2, 1], opacity: [0.1, 0.3, 0.1] }}
            transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
          />
        </svg>
      </div>

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="z-10 text-center max-w-4xl"
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="inline-block px-4 py-1.5 mb-8 rounded-full border border-brand-cyan/30 bg-brand-cyan/10 backdrop-blur-md"
        >
          <span className="text-brand-cyan font-medium tracking-wider text-sm uppercase">Next-Gen Fact Checking</span>
        </motion.div>

        <h1 className="text-6xl md:text-8xl font-black mb-6 tracking-tighter leading-none">
          Break the <span className="bg-clip-text text-transparent bg-gradient-to-r from-brand-blue to-brand-purple glow-text">Chain</span> Of Misinformation
        </h1>
        
        <p className="text-xl md:text-2xl text-premium-light/70 mb-10 max-w-2xl mx-auto leading-relaxed">
          The world's first real-time, AI-powered misinformation defense system. Verify text, audio, and viral content in milliseconds.
        </p>

        <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
          <motion.button 
            onClick={onGetStarted}
            className="btn-premium group"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
          >
            Launch Neural Engine
            <motion.span 
              animate={{ x: [0, 5, 0] }}
              transition={{ repeat: Infinity, duration: 1.5 }}
            >
              →
            </motion.span>
          </motion.button>
          
          <button className="px-8 py-3 rounded-full font-bold border border-white/10 hover:bg-white/5 transition-all duration-300">
            View Live Metrics
          </button>
        </div>
      </motion.div>

      {/* Stats Preview */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 1 }}
        className="absolute bottom-12 flex gap-12 text-sm uppercase tracking-widest text-premium-light/40"
      >
        <div className="flex flex-col items-center">
          <span className="text-brand-cyan font-bold text-lg mb-1">99.8%</span>
          <span>Accuracy</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-brand-purple font-bold text-lg mb-1">200ms</span>
          <span>Latency</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-brand-blue font-bold text-lg mb-1">1M+</span>
          <span>Filtered</span>
        </div>
      </motion.div>
    </section>
  );
};

export default Hero;
