import React from 'react';
import { Shield, Zap, Volume2, Globe, BarChart3, Lock } from 'lucide-react';
import { motion } from 'framer-motion';

const FeatureCard = ({ icon: Icon, title, description, delay }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ delay, duration: 0.5 }}
    viewport={{ once: true }}
    className="card-premium group"
  >
    <div className="w-14 h-14 rounded-2xl bg-brand-blue/10 flex items-center justify-center mb-6 border border-brand-blue/20 group-hover:scale-110 transition-transform duration-300">
      <Icon className="text-brand-cyan w-8 h-8 glow-text" />
    </div>
    <h3 className="text-2xl font-bold mb-3 text-white">{title}</h3>
    <p className="text-premium-light/60 leading-relaxed font-medium">
      {description}
    </p>
  </motion.div>
);

const Features = () => {
  const features = [
    {
      icon: Zap,
      title: "Real-Time Detection",
      description: "Analyze messages, social posts, and viral content as they spread. Stop the chain before it reaches the masses.",
      delay: 0.1
    },
    {
      icon: Shield,
      title: "AI Fact-Check Engine",
      description: "Advanced neural networks verify claims against verified global databases with 99.8% precision.",
      delay: 0.2
    },
    {
      icon: Volume2,
      title: "Audio + Text Analysis",
      description: "Seamlessly process voice notes and text. Our multi-modal AI breaks down nuance and context.",
      delay: 0.3
    },
    {
      icon: Globe,
      title: "Multi-Language Support",
      description: "Detect misinformation across 100+ languages including regional dialects and slang.",
      delay: 0.4
    },
    {
      icon: BarChart3,
      title: "Virality Prediction",
      description: "Understand the risk of content going viral with our proprietary virality scoring algorithm.",
      delay: 0.5
    },
    {
      icon: Lock,
      title: "Privacy First",
      description: "End-to-end encrypted analysis. Your data is processed securely and never stored without consent.",
      delay: 0.6
    }
  ];

  return (
    <section className="py-32 px-4 relative z-10 bg-black/50 backdrop-blur-3xl">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-24">
          <motion.h2 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            className="text-4xl md:text-5xl font-black mb-6 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-brand-blue to-brand-cyan"
          >
            Smarter Defense for a Complex World
          </motion.h2>
          <div className="w-24 h-1 bg-brand-purple mx-auto rounded-full" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => (
            <FeatureCard key={idx} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
