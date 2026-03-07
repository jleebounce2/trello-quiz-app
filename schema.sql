-- Vercel Postgres Schema for Trello Gamification
-- Created: 2026-03-06

-- Members table
CREATE TABLE IF NOT EXISTS members (
    name TEXT PRIMARY KEY,
    total_xp INTEGER DEFAULT 0,
    cards_done INTEGER DEFAULT 0,
    badges JSONB DEFAULT '[]'::jsonb,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- XP Log table
CREATE TABLE IF NOT EXISTS xp_log (
    id SERIAL PRIMARY KEY,
    member_name TEXT NOT NULL,
    xp_change INTEGER NOT NULL,
    reason TEXT,
    card_id TEXT,
    card_name TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Quizzes table
CREATE TABLE IF NOT EXISTS quizzes (
    id TEXT PRIMARY KEY,
    question TEXT NOT NULL,
    options JSONB NOT NULL,
    correct_answer TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    xp_reward INTEGER DEFAULT 5,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Quiz Attempts table
CREATE TABLE IF NOT EXISTS quiz_attempts (
    id SERIAL PRIMARY KEY,
    member_name TEXT NOT NULL,
    quiz_id TEXT NOT NULL,
    answer TEXT NOT NULL,
    correct BOOLEAN NOT NULL,
    xp_awarded INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_xp_log_member ON xp_log(member_name);
CREATE INDEX IF NOT EXISTS idx_xp_log_timestamp ON xp_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_member ON quiz_attempts(member_name);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_quiz ON quiz_attempts(quiz_id);
CREATE INDEX IF NOT EXISTS idx_members_total_xp ON members(total_xp DESC);
