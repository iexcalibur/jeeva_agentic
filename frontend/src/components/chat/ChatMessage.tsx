'use client';

import React from 'react';
import { Sparkles, Loader2 } from 'lucide-react';
import type { ChatMessage as ChatMessageType, Persona } from '@/types';

const PERSONA_CONFIG: Record<Persona, { name: string; icon: string; color: string }> = {
  mentor: { name: 'Mentor', icon: '🎓', color: 'from-emerald-600 to-green-600' },
  investor: { name: 'Investor', icon: '💰', color: 'from-blue-600 to-cyan-600' },
  technical_advisor: { name: 'Technical Advisor', icon: '🔧', color: 'from-orange-600 to-amber-600' },
  business_expert: { name: 'Business Expert', icon: '💼', color: 'from-purple-600 to-violet-600' },
};

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.sender === 'user';
  const persona = message.persona;
  const personaConfig = persona ? PERSONA_CONFIG[persona] : null;

  return (
    <div className={`flex gap-6 ${isUser ? 'justify-end' : ''}`}>
      
      {!isUser && (
        <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${personaConfig?.color || 'from-indigo-600 to-violet-600'} flex items-center justify-center flex-shrink-0 mt-1 shadow-lg shadow-indigo-500/20 border border-indigo-400/20`}>
          {personaConfig ? (
            <span className="text-lg">{personaConfig.icon}</span>
          ) : (
            <Sparkles size={18} className="text-white" />
          )}
        </div>
      )}

      <div className="flex-1 max-w-3xl space-y-4">
        
        {!isUser && personaConfig && (
          <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium bg-gradient-to-r ${personaConfig.color} bg-opacity-20 border border-white/10`}>
            <span>{personaConfig.icon}</span>
            <span className="text-slate-300">{personaConfig.name}</span>
          </div>
        )}
        
        <div className={`p-6 rounded-2xl backdrop-blur-md border relative ${
          isUser 
            ? 'bg-slate-800/60 border-white/5 text-white rounded-tr-none' 
            : 'bg-slate-900/50 border-white/10 text-slate-300 rounded-tl-none shadow-[0_0_40px_-10px_rgba(79,70,229,0.1)]'
        }`}>
          
          {message.isLoading ? (
            <div className="flex items-center gap-3">
              <Loader2 size={18} className="animate-spin text-indigo-400" />
              <span className="text-slate-400">Thinking...</span>
            </div>
          ) : message.error ? (
            <div className="text-rose-400">
              <p>{message.content}</p>
              <p className="text-xs mt-2 text-rose-500/70">{message.error}</p>
            </div>
          ) : (
            <p className="leading-relaxed text-[15px] whitespace-pre-wrap">{message.content}</p>
          )}
        </div>
      </div>

      {isUser && (
        <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center flex-shrink-0 mt-1">
          <span className="text-xs font-bold text-slate-400">YOU</span>
        </div>
      )}
    </div>
  );
}
