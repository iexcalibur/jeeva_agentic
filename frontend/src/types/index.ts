// Persona types
export type Persona = 'mentor' | 'investor' | 'technical_advisor' | 'business_expert';

export interface PersonaConfig {
  name: string;
  icon: string;
  color: string;
  description: string;
}

// Chat API types (matching backend)
export interface ChatRequest {
  user_id: string;
  message: string;
  thread_id?: string;
}

export interface ChatResponse {
  thread_id: string;
  persona: Persona;
  response: string;
  created_at: string;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface Thread {
  thread_id: string;
  user_id: string;
  persona: Persona;
  created_at: string;
  updated_at: string;
}

export interface ChatHistoryResponse {
  threads: Thread[];
  messages: Message[];
}

export interface HealthResponse {
  status: string;
  version?: string;
}

// Frontend chat message type
export interface ChatMessage {
  id: string | number;
  sender: 'user' | 'ai';
  content: string;
  persona?: Persona;
  thread_id?: string;
  created_at?: string;
  isLoading?: boolean;
  error?: string;
}
