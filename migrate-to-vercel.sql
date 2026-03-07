-- Complete Migration Script for Trello Gamification Database
-- Run this in Vercel Postgres SQL editor after creating the database
-- Project: gamification-quiz (prj_0XueRQl9DiNsIjDp0mItqGK46HH7)

-- ============================================
-- STEP 1: Create Tables
-- ============================================

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

-- ============================================
-- STEP 2: Insert Members Data
-- ============================================

INSERT INTO members (name, total_xp, cards_done, badges, last_updated) VALUES
('Edward', 35, 7, '["🏆"]'::jsonb, '2026-03-06 15:10:40'),
('Gourav', 30, 6, '["🏆"]'::jsonb, '2026-03-06 15:10:40'),
('Ibitola', 35, 7, '["🏆"]'::jsonb, '2026-03-06 15:10:40'),
('Jason', 55, 11, '["🏆"]'::jsonb, '2026-03-06 15:10:40'),
('Olabode', 30, 6, '["🏆"]'::jsonb, '2026-03-06 15:10:40');

-- ============================================
-- STEP 3: Insert XP Log Data
-- ============================================

INSERT INTO xp_log (id, member_name, xp_change, reason, card_id, card_name, timestamp) VALUES
(72, 'Jason', 5, 'Checklist: Course 2 Module 5 - JH', '69a990fe689410847843e76d', 'Course 2 Module 5 - JH', '2026-03-06 15:05:11'),
(73, 'Jason', 5, 'Checklist: Course 2 Module 4 - JH', '69a990f488127e62cea18f7d', 'Course 2 Module 4 - JH', '2026-03-06 15:05:11'),
(74, 'Jason', 5, 'Checklist: Course 2 Module 3 - JH', '69a99038636636bc69a5bf54', 'Course 2 Module 3 - JH', '2026-03-06 15:05:11'),
(75, 'Jason', 5, 'Checklist: Course 2 Module 2 - JH', '69a98fdd9008779cd2629c12', 'Course 2 Module 2 - JH', '2026-03-06 15:05:11'),
(76, 'Jason', 5, 'Checklist: Course 2 Module 1 - JH', '69a98fceb64387507362ba85', 'Course 2 Module 1 - JH', '2026-03-06 15:05:11'),
(77, 'Edward', 5, 'Checklist: Course 2 Module 1 - EH', '69a98fceb64387507362ba86', 'Course 2 Module 1 - EH', '2026-03-06 15:05:11'),
(78, 'Ibitola', 5, 'Checklist: Course 2 Module 1 - IA', '69a98fceb64387507362ba8a', 'Course 2 Module 1 - IA', '2026-03-06 15:05:11'),
(79, 'Jason', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 1', '2026-03-06 15:10:40'),
(80, 'Jason', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 2', '2026-03-06 15:10:40'),
(81, 'Jason', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 3', '2026-03-06 15:10:40'),
(82, 'Jason', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 4', '2026-03-06 15:10:40'),
(83, 'Jason', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 5', '2026-03-06 15:10:40'),
(84, 'Jason', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 6', '2026-03-06 15:10:40'),
(85, 'Edward', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 1', '2026-03-06 15:10:40'),
(86, 'Edward', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 2', '2026-03-06 15:10:40'),
(87, 'Edward', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 3', '2026-03-06 15:10:40'),
(88, 'Edward', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 4', '2026-03-06 15:10:40'),
(89, 'Edward', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 5', '2026-03-06 15:10:40'),
(90, 'Edward', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 6', '2026-03-06 15:10:40'),
(91, 'Gourav', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 1', '2026-03-06 15:10:40'),
(92, 'Gourav', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 2', '2026-03-06 15:10:40'),
(93, 'Gourav', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 3', '2026-03-06 15:10:40'),
(94, 'Gourav', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 4', '2026-03-06 15:10:40'),
(95, 'Gourav', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 5', '2026-03-06 15:10:40'),
(96, 'Gourav', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 6', '2026-03-06 15:10:40'),
(97, 'Ibitola', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 1', '2026-03-06 15:10:40'),
(98, 'Ibitola', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 2', '2026-03-06 15:10:40'),
(99, 'Ibitola', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 3', '2026-03-06 15:10:40'),
(100, 'Ibitola', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 4', '2026-03-06 15:10:40'),
(101, 'Ibitola', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 5', '2026-03-06 15:10:40'),
(102, 'Ibitola', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 6', '2026-03-06 15:10:40'),
(103, 'Olabode', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 1', '2026-03-06 15:10:40'),
(104, 'Olabode', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 2', '2026-03-06 15:10:40'),
(105, 'Olabode', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 3', '2026-03-06 15:10:40'),
(106, 'Olabode', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 4', '2026-03-06 15:10:40'),
(107, 'Olabode', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 5', '2026-03-06 15:10:40'),
(108, 'Olabode', 5, 'Tech Deliverables - Module completion', 'CHECKLIST-001', 'Module 6', '2026-03-06 15:10:40');

-- Reset the sequence for xp_log
SELECT setval('xp_log_id_seq', 108, true);

-- ============================================
-- STEP 4: Insert Quizzes Data
-- ============================================

INSERT INTO quizzes (id, question, options, correct_answer, category, xp_reward, created_at) VALUES
('quiz-c2m1-001', 'What is a computer network?', '[["A", "A single computer"], ["B", "A group of interconnected computers that can communicate"], ["C", "A type of software"], ["D", "A storage device"]]'::jsonb, 'B', 'Module 1: Intro to Networking', 5, '2026-03-06 03:39:53'),
('quiz-c2m1-002', 'What does LAN stand for?', '[["A", "Large Area Network"], ["B", "Local Access Network"], ["C", "Local Area Network"], ["D", "Long Distance Area Network"]]'::jsonb, 'C', 'Module 1: Intro to Networking', 5, '2026-03-06 03:39:53'),
('quiz-c2m1-003', 'Which device connects multiple networks together?', '[["A", "Hub"], ["B", "Switch"], ["C", "Router"], ["D", "Repeater"]]'::jsonb, 'C', 'Module 1: Intro to Networking', 5, '2026-03-06 03:39:53'),
('quiz-c2m2-001', 'What does IP stand for?', '[["A", "Internet Protocol"], ["B", "Internal Processing"], ["C", "Interconnected Systems"], ["D", "Information Packet"]]'::jsonb, 'A', 'Module 2: Network Layer', 5, '2026-03-06 03:39:53'),
('quiz-c2m2-002', 'How many bits are in an IPv4 address?', '[["A", "16 bits"], ["B", "32 bits"], ["C", "64 bits"], ["D", "128 bits"]]'::jsonb, 'B', 'Module 2: Network Layer', 5, '2026-03-06 03:39:53'),
('quiz-c2m2-003', 'What is the purpose of a subnet mask?', '[["A", "To encrypt data"], ["B", "To divide an IP address into network and host portions"], ["C", "To speed up the network"], ["D", "To block viruses"]]'::jsonb, 'B', 'Module 2: Network Layer', 5, '2026-03-06 03:39:53'),
('quiz-c2m3-001', 'Which protocol is connection-oriented and guarantees delivery?', '[["A", "UDP"], ["B", "IP"], ["C", "TCP"], ["D", "HTTP"]]'::jsonb, 'C', 'Module 3: Transport Layer', 5, '2026-03-06 03:39:53'),
('quiz-c2m3-002', 'What does TCP stand for?', '[["A", "Transfer Control Protocol"], ["B", "Transmission Control Protocol"], ["C", "Transport Communication Protocol"], ["D", "Technical Connection Protocol"]]'::jsonb, 'B', 'Module 3: Transport Layer', 5, '2026-03-06 03:39:53'),
('quiz-c2m3-003', 'Which protocol is faster but does NOT guarantee delivery?', '[["A", "TCP"], ["B", "UDP"], ["C", "FTP"], ["D", "SMTP"]]'::jsonb, 'B', 'Module 3: Transport Layer', 5, '2026-03-06 03:39:53'),
('quiz-c2m4-001', 'What port does HTTP use by default?', '[["A", "Port 21"], ["B", "Port 22"], ["C", "Port 80"], ["D", "Port 443"]]'::jsonb, 'C', 'Module 4: Application Layer', 5, '2026-03-06 03:39:53'),
('quiz-c2m4-002', 'What does DNS stand for?', '[["A", "Domain Name System"], ["B", "Digital Network Service"], ["C", "Data Naming Service"], ["D", "Domain Network Server"]]'::jsonb, 'A', 'Module 4: Application Layer', 5, '2026-03-06 03:39:53'),
('quiz-c2m4-003', 'Which protocol is used for secure web browsing?', '[["A", "HTTP"], ["B", "HTTPS"], ["C", "FTP"], ["D", "SMTP"]]'::jsonb, 'B', 'Module 4: Application Layer', 5, '2026-03-06 03:39:53'),
('quiz-c2m5-001', 'What does ISP stand for?', '[["A", "Internet Service Provider"], ["B", "Internal System Protocol"], ["C", "International Security Program"], ["D", "Internet Security Protocol"]]'::jsonb, 'A', 'Module 5: Connecting to Internet', 5, '2026-03-06 03:39:53'),
('quiz-c2m5-002', 'Which technology uses phone lines to provide internet?', '[["A", "Fiber"], ["B", "Cable"], ["C", "DSL"], ["D", "Satellite"]]'::jsonb, 'C', 'Module 5: Connecting to Internet', 5, '2026-03-06 03:39:53'),
('quiz-c2m5-003', 'What is a modem used for?', '[["A", "To store data"], ["B", "To modulate and demodulate signals for internet connection"], ["C", "To block viruses"], ["D", "To connect wireless devices only"]]'::jsonb, 'B', 'Module 5: Connecting to Internet', 5, '2026-03-06 03:39:53'),
('quiz-c2m6-001', 'What command tests connectivity to another host?', '[["A", "ls"], ["B", "cd"], ["C", "ping"], ["D", "mkdir"]]'::jsonb, 'C', 'Module 6: Troubleshooting', 5, '2026-03-06 03:39:53'),
('quiz-c2m6-002', 'What does traceroute do?', '[["A", "Deletes files"], ["B", "Shows the path packets take to reach a destination"], ["C", "Creates new directories"], ["D", "Backs up data"]]'::jsonb, 'B', 'Module 6: Troubleshooting', 5, '2026-03-06 03:39:53'),
('quiz-c2m6-003', 'What is the cloud in networking terms?', '[["A", "Actual clouds in the sky"], ["B", "A type of weather phenomenon"], ["C", "Remote servers that store and process data"], ["D", "A wireless mouse"]]'::jsonb, 'C', 'Module 6: Troubleshooting', 5, '2026-03-06 03:39:53');

-- ============================================
-- STEP 5: Insert Quiz Attempts Data
-- ============================================

INSERT INTO quiz_attempts (id, member_name, quiz_id, answer, correct, xp_awarded, timestamp) VALUES
(1, 'Jason', 'quiz-api-001', 'C', true, 5, '2026-03-06 03:32:40'),
(2, 'Jason', 'quiz-api-002', 'C', true, 5, '2026-03-06 03:33:13'),
(3, 'Jason', 'quiz-api-003', 'C', false, 0, '2026-03-06 03:33:46'),
(4, 'Jason', 'quiz-git-001', 'C', false, 0, '2026-03-06 03:38:29'),
(5, 'Jason', 'quiz-git-002', 'A', false, 0, '2026-03-06 03:38:45'),
(6, 'Jason', 'quiz-git-003', 'C', false, 0, '2026-03-06 03:39:00'),
(7, 'Jason', 'quiz-sec-001', 'B', true, 5, '2026-03-06 03:39:08'),
(8, 'Jason', 'quiz-sec-002', 'C', true, 5, '2026-03-06 03:39:16'),
(9, 'Jason', 'quiz-sec-003', 'A', true, 5, '2026-03-06 03:39:25');

-- Reset the sequence for quiz_attempts
SELECT setval('quiz_attempts_id_seq', 9, true);

-- ============================================
-- Migration Complete!
-- ============================================
