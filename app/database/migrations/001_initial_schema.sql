-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Threads table
CREATE TABLE IF NOT EXISTS threads (
    thread_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    persona VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    message_id UUID PRIMARY KEY,
    thread_id UUID REFERENCES threads(thread_id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Checkpoints table (for LangGraph state)
CREATE TABLE IF NOT EXISTS checkpoints (
    checkpoint_id UUID PRIMARY KEY,
    thread_id UUID REFERENCES threads(thread_id) ON DELETE CASCADE,
    state JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

