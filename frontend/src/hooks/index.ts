import { useState, useCallback, useRef, useEffect } from 'react';
import { sendChatMessage, getChatHistory, checkHealth } from '@/lib/api';
import type { 
  ChatRequest,
  ChatResponse,
  ChatMessage,
  Persona,
} from '@/types';
import { generateId } from '@/lib/utils';

// Get or create user ID from localStorage
function getUserId(): string {
  if (typeof window === 'undefined') return 'user_' + Date.now();
  const stored = localStorage.getItem('jeeva_user_id');
  if (stored) return stored;
  const newId = 'user_' + Date.now();
  localStorage.setItem('jeeva_user_id', newId);
  return newId;
}

interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  currentPersona: Persona | null;
  threadId: string | null;
  sendMessage: (content: string) => Promise<void>;
  clearMessages: () => void;
  loadHistory: (threadId: string) => Promise<void>;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPersona, setCurrentPersona] = useState<Persona | null>(null);
  const [threadId, setThreadId] = useState<string | null>(null);
  const [userId] = useState<string>(getUserId());
  const isRequestInFlight = useRef(false);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isRequestInFlight.current) return;

    const userMessage: ChatMessage = {
      id: generateId(),
      sender: 'user',
      content: content.trim(),
      created_at: new Date().toISOString(),
    };

    const aiMessageId = generateId();
    const aiMessage: ChatMessage = {
      id: aiMessageId,
      sender: 'ai',
      content: '',
      isLoading: true,
    };

    isRequestInFlight.current = true;
    setMessages((prev) => [...prev, userMessage, aiMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const request: ChatRequest = {
        user_id: userId,
        message: content.trim(),
        thread_id: threadId || undefined,
      };

      const response: ChatResponse = await sendChatMessage(request);

      // Update thread ID and persona
      setThreadId(response.thread_id);
      setCurrentPersona(response.persona);

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === aiMessageId
            ? {
                ...msg,
                content: response.response,
                persona: response.persona,
                thread_id: response.thread_id,
                created_at: response.created_at,
                isLoading: false,
              }
            : msg
        )
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get response';
      setError(errorMessage);
      
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === aiMessageId
            ? {
                ...msg,
                content: 'Sorry, I encountered an error processing your request. Please make sure the backend server is running on http://localhost:8000',
                isLoading: false,
                error: errorMessage,
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
      isRequestInFlight.current = false;
    }
  }, [userId, threadId]);

  const loadHistory = useCallback(async (threadIdToLoad: string) => {
    try {
      const history = await getChatHistory(userId, threadIdToLoad);
      if (history.messages.length > 0) {
        const chatMessages: ChatMessage[] = history.messages.map((msg, idx) => ({
          id: generateId() + idx,
          sender: msg.role === 'user' ? 'user' : 'ai',
          content: msg.content,
          created_at: msg.created_at,
        }));
        setMessages(chatMessages);
        setThreadId(threadIdToLoad);
        if (history.threads.length > 0) {
          setCurrentPersona(history.threads[0].persona);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load history');
    }
  }, [userId]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
    setThreadId(null);
    setCurrentPersona(null);
    isRequestInFlight.current = false;
  }, []);

  return { messages, isLoading, error, currentPersona, threadId, sendMessage, clearMessages, loadHistory };
}


interface UseHealthReturn {
  isHealthy: boolean | null;
  isChecking: boolean;
  checkAPI: () => Promise<void>;
}

export function useHealth(): UseHealthReturn {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(false);

  const checkAPI = useCallback(async () => {
    setIsChecking(true);
    try {
      const response = await checkHealth();
      setIsHealthy(response.status === 'healthy' || response.status === 'ok');
    } catch {
      setIsHealthy(false);
    } finally {
      setIsChecking(false);
    }
  }, []);

  return { isHealthy, isChecking, checkAPI };
}
