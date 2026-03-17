import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, CheckCircle, Info, Share2, TrendingUp, ShieldCheck } from 'lucide-react';
import TrustScore from './TrustScore';

const ResultsPanel = ({ result }) => {
  if (!result) return null;

  const {
    verdict,
    explanation,
    virality_score,
    confidence_score,
    transcription,
    counter_message,
    virality_reasons
  } = result;

  const isFalse = verdict === 'FALSE';
  const isTrue = verdict === 'TRUE';
  const isUncertain = verdict === 'UNCERTAIN';

  const getVerdictStyles = () => {
    if (isFalse) return {
      bg: 'bg-red-500/10',
      border: 'border-red-500/20',
      text: 'text-red-500',
      icon: AlertTriangle,
      label: 'MISINFORMATION DETECTED'
    };
    if (isTrue) return {
      bg: 'bg-brand-cyan/10',
      border: 'border-brand-cyan/20',
      text: 'text-brand-cyan',
      icon: CheckCircle,
      label: 'VERIFIED AUTHENTIC'
    };
    return {
      bg: 'bg-brand-purple/10',
      border: 'border-brand-purple/20',
      text: 'text-brand-purple',
      icon: Info,
      label: 'UNCERTAIN EVIDENCE'
    };
  };

  const styles = getVerdictStyles();
  const Icon = styles.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8 pb-20"
    >
      {/* Main Verdict Card */}
      <div className="lg:col-span-2 space-y-8">
        <div className={`card-premium p-8 border-2 ${styles.border} ${styles.bg} relative overflow-hidden`}>
          {/* Breaking Chain Animation Overlay (if false) */}
          {isFalse && (
            <motion.div 
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="absolute top-4 right-4 text-red-500/20"
            >
              <ShieldCheck size={120} />
            </motion.div>
          )}

          <div className="flex items-center gap-4 mb-6">
            <div className={`w-12 h-12 rounded-xl ${styles.bg} flex items-center justify-center border ${styles.border}`}>
              <Icon className={styles.text} size={28} />
            </div>
            <div>
              <span className={`text-xs font-black tracking-[0.2em] ${styles.text}`}>
                {styles.label}
              </span>
              <h2 className="text-4xl font-black text-white glow-text">Analysis Detailed</h2>
            </div>
          </div>

          <div className="space-y-6 relative z-10">
            <div>
              <h4 className="text-xs uppercase tracking-widest text-premium-light/30 font-bold mb-2">Transcription / Input</h4>
              <p className="text-lg text-white/80 font-medium italic">"{transcription}"</p>
            </div>

            <div>
              <h4 className="text-xs uppercase tracking-widest text-premium-light/30 font-bold mb-2">AI Explanation</h4>
              <p className="text-xl text-white leading-relaxed">{explanation}</p>
            </div>

            {counter_message && (
              <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                <h4 className="text-xs uppercase tracking-widest text-brand-cyan font-bold mb-2">Recommended Counter Message</h4>
                <p className="text-brand-cyan/80">{counter_message}</p>
                <button className="mt-3 text-xs font-bold flex items-center gap-2 hover:text-white transition-colors">
                  <Share2 size={14} /> COPY TO STOP THE SPREAD
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Truth vs False Comparison (Split Cards) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card-premium p-6 border-red-500/10 bg-red-500/5">
            <h4 className="text-red-500 font-bold flex items-center gap-2 mb-4">
              <AlertTriangle size={18} /> Claims Made
            </h4>
            <ul className="space-y-3 text-premium-light/60 text-sm">
              <li>• Unverified scientific assertions</li>
              <li>• Emotional manipulation tactics</li>
              <li>• Lack of primary source citation</li>
            </ul>
          </div>
          <div className="card-premium p-6 border-brand-cyan/10 bg-brand-cyan/5">
            <h4 className="text-brand-cyan font-bold flex items-center gap-2 mb-4">
              <CheckCircle size={18} /> Verified Facts
            </h4>
            <ul className="space-y-3 text-premium-light/60 text-sm">
              <li>• Consistent with WHO guidelines</li>
              <li>• Peer-reviewed evidence available</li>
              <li>• Transparent methodology</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Sidebar Metrics */}
      <div className="space-y-8">
        <div className="card-premium p-8 flex flex-col items-center">
          <TrustScore score={confidence_score} />
          <p className="mt-4 text-center text-sm text-premium-light/50 font-medium px-4">
            Confidence score based on cross-referencing global databases.
          </p>
        </div>

        <div className="card-premium p-8">
          <div className="flex items-center justify-between mb-6">
            <h4 className="font-bold flex items-center gap-2">
              <TrendingUp className="text-brand-purple" size={20} /> Virality Risk
            </h4>
            <span className="text-2xl font-black text-brand-purple italic">{virality_score}/10</span>
          </div>
          
          <div className="w-full bg-white/5 h-3 rounded-full mb-6 overflow-hidden border border-white/5">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${virality_score * 10}%` }}
              className="h-full bg-gradient-to-r from-brand-blue to-brand-purple"
            />
          </div>

          <div className="space-y-3">
            {virality_reasons?.map((reason, i) => (
              <div key={i} className="flex gap-2 text-xs text-premium-light/40">
                <span className="text-brand-purple">•</span>
                {reason}
              </div>
            ))}
          </div>
        </div>

        <button className="w-full btn-premium py-4 justify-center">
          GENERATE FULL REPORT (PDF)
        </button>
      </div>
    </motion.div>
  );
};

export default ResultsPanel;
