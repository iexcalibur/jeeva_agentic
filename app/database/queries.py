"""Raw SQL queries"""
from typing import Optional

# User queries
CREATE_USER = """
    INSERT INTO users (user_id, created_at)
    VALUES ($1, NOW())
    ON CONFLICT (user_id) DO NOTHING
    RETURNING user_id, created_at;
"""

GET_USER = """
    SELECT user_id, created_at
    FROM users
    WHERE user_id = $1;
"""

# Thread queries
CREATE_THREAD = """
    INSERT INTO threads (thread_id, user_id, persona, created_at, updated_at)
    VALUES ($1, $2, $3, NOW(), NOW())
    RETURNING thread_id, user_id, persona, created_at, updated_at;
"""

GET_THREAD = """
    SELECT thread_id, user_id, persona, created_at, updated_at
    FROM threads
    WHERE thread_id = $1;
"""

GET_USER_THREADS = """
    SELECT thread_id, user_id, persona, created_at, updated_at
    FROM threads
    WHERE user_id = $1
    ORDER BY updated_at DESC;
"""

UPDATE_THREAD_PERSONA = """
    UPDATE threads
    SET persona = $1, updated_at = NOW()
    WHERE thread_id = $2
    RETURNING thread_id, user_id, persona, created_at, updated_at;
"""

# Message queries
CREATE_MESSAGE = """
    INSERT INTO messages (message_id, thread_id, role, content, created_at)
    VALUES ($1, $2, $3, $4, NOW())
    RETURNING message_id, thread_id, role, content, created_at;
"""

GET_THREAD_MESSAGES = """
    SELECT message_id, thread_id, role, content, created_at
    FROM messages
    WHERE thread_id = $1
    ORDER BY created_at ASC;
"""

# Checkpoint queries
CREATE_CHECKPOINT = """
    INSERT INTO checkpoints (checkpoint_id, thread_id, state, created_at)
    VALUES ($1, $2, $3::jsonb, NOW())
    RETURNING checkpoint_id, thread_id, state, created_at;
"""

GET_LATEST_CHECKPOINT = """
    SELECT checkpoint_id, thread_id, state, created_at
    FROM checkpoints
    WHERE thread_id = $1
    ORDER BY created_at DESC
    LIMIT 1;
"""

GET_ALL_CHECKPOINTS = """
    SELECT checkpoint_id, thread_id, state, created_at
    FROM checkpoints
    WHERE thread_id = $1
    ORDER BY created_at ASC;
"""

