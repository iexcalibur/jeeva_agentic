'use client';

import React, { useState } from 'react';
import { ArrowRight } from 'lucide-react';

interface ChatInputProps {
  onSubmit: (message: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

export default function ChatInput({ onSubmit, isLoading, placeholder }: ChatInputProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSubmit(input.trim());
      setInput('');
    }
  };

  return (
    <div className="absolute bottom-0 left-0 w-full z-20">
      <div className="bg-slate-950/0 px-4 pb-6 pt-2">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative group">
          
          <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-500 rounded-2xl opacity-10 blur-xl group-hover:opacity-30 transition duration-500" />

          {/* Glass Input Container */}
          <div className="bg-slate-900/60 backdrop-blur-md border border-white/10 rounded-2xl p-2 flex flex-col relative">
            <textarea 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={placeholder || "Ask me anything... I'll adapt to help you best!"} 
              className="w-full resize-none border-none focus:ring-0 outline-none text-slate-200 placeholder-slate-600 p-4 min-h-[60px] max-h-[200px] bg-transparent text-base scrollbar-thin scrollbar-thumb-slate-700"
              rows={1}
              disabled={isLoading}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            
            <div className="flex justify-end items-center px-2 pb-1">
              <button 
                type="submit"
                className="bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl px-5 py-2 font-medium flex items-center gap-2 text-sm transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={!input.trim() || isLoading}
              >
                <span>{isLoading ? 'Thinking...' : 'Send'}</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
