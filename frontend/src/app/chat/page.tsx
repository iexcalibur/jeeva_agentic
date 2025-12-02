'use client';

import React, { useRef, useEffect, useMemo, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Loader2, Plus } from 'lucide-react';
import { useChat } from '@/hooks'; 
import { ChatMessage as ChatMessageComponent, ChatInput, WelcomeMessage } from '@/components/chat';

function ChatContent() {
  const { messages, isLoading, error, sendMessage, currentPersona, clearMessages } = useChat();
  
  const scrollRef = useRef<HTMLDivElement>(null);
  const searchParams = useSearchParams();
  const router = useRouter();
  const hasProcessedQuery = useRef(false);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const urlQuery = useMemo(() => searchParams.get('q'), [searchParams]);
  useEffect(() => {
    // Prevent double-firing or firing if already loading
    if (hasProcessedQuery.current || isLoading) return;
    if (urlQuery) {
      const trimmedQuery = urlQuery.trim();
      if (trimmedQuery && messages.length === 0) {
        hasProcessedQuery.current = true;
        sendMessage(trimmedQuery);
        
        // --- FIX: Clean the URL immediately after processing ---
        // This prevents the "Act like my mentor" from re-triggering on reload
        router.replace('/chat', { scroll: false });
      }
    }
  }, [urlQuery, sendMessage, messages.length, isLoading, router]);

  // Handler for New Chat
  const handleNewChat = () => {
    clearMessages();
    router.replace('/chat'); // Ensure URL is clean
    hasProcessedQuery.current = false; // Reset query processor
  };

  return (
    <div className="relative h-screen w-full bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30 overflow-hidden">

      {/* Header / Actions Overlay */}
      <div className="absolute top-4 right-4 z-20 flex gap-2">
        {messages.length > 0 && (
          <button 
            onClick={handleNewChat}
            className="flex items-center gap-2 px-3 py-2 bg-slate-800/50 backdrop-blur-md hover:bg-indigo-600/20 border border-white/10 hover:border-indigo-500/50 rounded-lg text-xs font-medium text-slate-300 hover:text-white transition-all shadow-lg"
          >
            <Plus size={14} />
            <span>New Chat</span>
          </button>
        )}
      </div>

      <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-violet-900/10 blur-[120px] pointer-events-none z-0"></div>
      <div className="fixed bottom-0 left-0 w-[500px] h-[500px] bg-indigo-900/10 blur-[120px] pointer-events-none z-0"></div>

      <div 
        ref={scrollRef}
        className="absolute top-16 bottom-0 left-0 right-0 overflow-y-auto px-4 md:px-8 pt-6 pb-40 scrollbar-thin scrollbar-thumb-slate-800 scrollbar-track-transparent z-10"
      >
        <div className="max-w-4xl mx-auto space-y-10">

          {messages.length === 0 && (
            <WelcomeMessage onQuickAction={sendMessage} />
          )}

          {messages.map((msg) => (
            <ChatMessageComponent key={msg.id} message={msg} />
          ))}
          
          {error && (
             <div className="text-center text-rose-400 text-sm py-4 bg-rose-500/5 rounded-lg border border-rose-500/10">
               {error}
             </div>
          )}
        </div>
      </div>

      <ChatInput 
        onSubmit={sendMessage} 
        isLoading={isLoading}
        placeholder={
          currentPersona 
            ? `Ask your ${currentPersona.replace('_', ' ')}...` 
            : "Ask me anything... I'll adapt to help you best!"
        }
      />
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="h-screen flex items-center justify-center bg-slate-950"><Loader2 size={32} className="animate-spin text-indigo-500" /></div>}>
      <ChatContent />
    </Suspense>
  );
}