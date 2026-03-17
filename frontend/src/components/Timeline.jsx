import React from 'react';
import { motion } from 'framer-motion';
import { Clock, AlertTriangle, ShieldCheck, Zap } from 'lucide-react';

const TimelineStep = ({ title, description, time, icon: Icon, color, isLast }) => (
  <div className="relative flex gap-8 pb-12 group">
    {!isLast && (
      <div className="absolute left-[27px] top-10 bottom-0 w-[2px] bg-white/5 group-hover:bg-brand-purple/20 transition-colors" />
    )}
    <div className={`w-14 h-14 rounded-2xl ${color} flex items-center justify-center border border-white/10 z-10 shrink-0 shadow-lg`}>
      <Icon size={24} className="text-white" />
    </div>
    <div className="pt-2">
      <div className="flex items-center gap-4 mb-1">
        <h4 className="text-lg font-bold text-white uppercase tracking-tight">{title}</h4>
        <span className="text-[10px] font-black text-premium-light/30 flex items-center gap-1 bg-white/5 px-2 py-0.5 rounded italic">
          <Clock size={10} /> {time}
        </span>
      </div>
      <p className="text-premium-light/50 max-w-lg leading-relaxed">{description}</p>
    </div>
  </div>
);

const Timeline = () => {
  return (
    <section className="py-32 px-4 relative z-10">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-24">
          <motion.h2 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            className="text-4xl md:text-5xl font-black mb-6 tracking-tight flex items-center justify-center gap-4"
          >
            <Zap className="text-brand-cyan" /> Visualizing the Impact
          </motion.h2>
          <p className="text-premium-light/40 font-medium">How ChainBreaker AI stops the spread in milliseconds.</p>
        </div>

        <div className="space-y-2">
          <TimelineStep 
            title="Ingestion"
            description="Our neural engine receives a suspicious message or audio clip from an encrypted source."
            time="T+0ms"
            icon={Zap}
            color="bg-brand-blue/20"
          />
          <TimelineStep 
            title="Neural Breakdown"
            description="The claim is decomposed into 12 core semantic features and compared against global datasets."
            time="T+45ms"
            icon={Clock}
            color="bg-brand-purple/20"
          />
          <TimelineStep 
            title="Misinformation Detected"
            description="Confidence threshold exceeded (98.4%). The system identifies specific logical fallacies."
            time="T+120ms"
            icon={AlertTriangle}
            color="bg-red-500/20"
          />
          <TimelineStep 
            title="The Chain Breaker"
            description="Analysis complete. Counter-intelligence generated. The spread is halted at source."
            time="T+180ms"
            icon={ShieldCheck}
            color="bg-brand-cyan/20"
            isLast={true}
          />
        </div>
      </div>
    </section>
  );
};

export default Timeline;
