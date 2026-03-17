import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileAudio, FileText, Send, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const AnalysisBox = ({ onAnalyze, isLoading }) => {
  const [text, setText] = useState('');
  const [mode, setMode] = useState('text'); // 'text' or 'audio'

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles?.length > 0) {
      onAnalyze(acceptedFiles[0], 'audio');
    }
  }, [onAnalyze]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'audio/*': [] },
    multiple: false
  });

  const handleTextSubmit = () => {
    if (text.trim()) {
      onAnalyze(text.trim(), 'text');
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto mb-16">
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setMode('text')}
          className={`px-6 py-2 rounded-full font-bold transition-all ${mode === 'text' ? 'bg-brand-blue text-white shadow-lg shadow-brand-blue/20' : 'bg-white/5 text-premium-light/40 hover:bg-white/10'}`}
        >
          Text Analysis
        </button>
        <button
          onClick={() => setMode('audio')}
          className={`px-6 py-2 rounded-full font-bold transition-all ${mode === 'audio' ? 'bg-brand-purple text-white shadow-lg shadow-brand-purple/20' : 'bg-white/5 text-premium-light/40 hover:bg-white/10'}`}
        >
          Audio Analysis
        </button>
      </div>

      <motion.div 
        layout
        className="card-premium p-1 border-white/5 group"
      >
        <div className="bg-black/40 rounded-xl overflow-hidden p-6">
          <AnimatePresence mode="wait">
            {mode === 'text' ? (
              <motion.div
                key="text-input"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="relative"
              >
                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Paste a suspicious news article, social media post, or claim here..."
                  className="w-full h-40 bg-transparent text-xl text-white placeholder:text-premium-light/20 resize-none focus:outline-none"
                />
                <div className="flex justify-end mt-4">
                  <button
                    onClick={handleTextSubmit}
                    disabled={isLoading || !text.trim()}
                    className="btn-premium py-2 px-6 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? <Loader2 className="animate-spin" /> : <Send size={20} />}
                    {isLoading ? 'Analyzing...' : 'Break the Chain'}
                  </button>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="audio-input"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                {...getRootProps()}
                className={`h-48 border-2 border-dashed rounded-xl flex flex-col items-center justify-center cursor-pointer transition-all ${isDragActive ? 'border-brand-cyan bg-brand-cyan/5' : 'border-white/10 hover:border-brand-purple/50'}`}
              >
                <input {...getInputProps()} />
                <motion.div
                  animate={{ y: isDragActive ? -10 : 0 }}
                  className="w-16 h-16 rounded-full bg-brand-purple/10 flex items-center justify-center mb-4"
                >
                  {isLoading ? <Loader2 className="text-brand-purple animate-spin" size={32} /> : <Upload className="text-brand-purple" size={32} />}
                </motion.div>
                <p className="text-lg font-medium text-premium-light/60">
                  {isDragActive ? 'Drop the recording here' : 'Drag & Drop audio file or click to browse'}
                </p>
                <span className="text-sm text-premium-light/20 mt-2">MP3, WAV, OGG (Max 25MB)</span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  );
};

export default AnalysisBox;
