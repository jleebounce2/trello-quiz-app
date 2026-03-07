#!/usr/bin/env python3
"""Initialize quiz database with Google IT Support Course 2 questions."""

import sqlite3
import json

DB_PATH = "/Users/abc/.openclaw/workspace/trello-gamification.db"

def init_quizzes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id TEXT PRIMARY KEY,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            xp_reward INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_name TEXT NOT NULL,
            quiz_id TEXT NOT NULL,
            answer TEXT NOT NULL,
            correct BOOLEAN NOT NULL,
            xp_awarded INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Clear existing quizzes
    cursor.execute('DELETE FROM quizzes')
    
    # Course 2: The Bits and Bytes of Computer Networking
    # 6 Modules with 3 questions each = 18 questions total
    quizzes = [
        # Module 1: Introduction to Networking
        {
            'id': 'quiz-c2m1-001',
            'question': 'What is a computer network?',
            'options': [
                ['A', 'A single computer'],
                ['B', 'A group of interconnected computers that can communicate'],
                ['C', 'A type of software'],
                ['D', 'A storage device']
            ],
            'correct_answer': 'B',
            'category': 'Module 1: Intro to Networking',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m1-002',
            'question': 'What does LAN stand for?',
            'options': [
                ['A', 'Large Area Network'],
                ['B', 'Local Access Network'],
                ['C', 'Local Area Network'],
                ['D', 'Long Distance Area Network']
            ],
            'correct_answer': 'C',
            'category': 'Module 1: Intro to Networking',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m1-003',
            'question': 'Which device connects multiple networks together?',
            'options': [
                ['A', 'Hub'],
                ['B', 'Switch'],
                ['C', 'Router'],
                ['D', 'Repeater']
            ],
            'correct_answer': 'C',
            'category': 'Module 1: Intro to Networking',
            'xp_reward': 5
        },
        
        # Module 2: The Network Layer
        {
            'id': 'quiz-c2m2-001',
            'question': 'What does IP stand for?',
            'options': [
                ['A', 'Internet Protocol'],
                ['B', 'Internal Processing'],
                ['C', 'Interconnected Systems'],
                ['D', 'Information Packet']
            ],
            'correct_answer': 'A',
            'category': 'Module 2: Network Layer',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m2-002',
            'question': 'How many bits are in an IPv4 address?',
            'options': [
                ['A', '16 bits'],
                ['B', '32 bits'],
                ['C', '64 bits'],
                ['D', '128 bits']
            ],
            'correct_answer': 'B',
            'category': 'Module 2: Network Layer',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m2-003',
            'question': 'What is the purpose of a subnet mask?',
            'options': [
                ['A', 'To encrypt data'],
                ['B', 'To divide an IP address into network and host portions'],
                ['C', 'To speed up the network'],
                ['D', 'To block viruses']
            ],
            'correct_answer': 'B',
            'category': 'Module 2: Network Layer',
            'xp_reward': 5
        },
        
        # Module 3: The Transport Layer
        {
            'id': 'quiz-c2m3-001',
            'question': 'Which protocol is connection-oriented and guarantees delivery?',
            'options': [
                ['A', 'UDP'],
                ['B', 'IP'],
                ['C', 'TCP'],
                ['D', 'HTTP']
            ],
            'correct_answer': 'C',
            'category': 'Module 3: Transport Layer',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m3-002',
            'question': 'What does TCP stand for?',
            'options': [
                ['A', 'Transfer Control Protocol'],
                ['B', 'Transmission Control Protocol'],
                ['C', 'Transport Communication Protocol'],
                ['D', 'Technical Connection Protocol']
            ],
            'correct_answer': 'B',
            'category': 'Module 3: Transport Layer',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m3-003',
            'question': 'Which protocol is faster but does NOT guarantee delivery?',
            'options': [
                ['A', 'TCP'],
                ['B', 'UDP'],
                ['C', 'FTP'],
                ['D', 'SMTP']
            ],
            'correct_answer': 'B',
            'category': 'Module 3: Transport Layer',
            'xp_reward': 5
        },
        
        # Module 4: The Application Layer
        {
            'id': 'quiz-c2m4-001',
            'question': 'What port does HTTP use by default?',
            'options': [
                ['A', 'Port 21'],
                ['B', 'Port 22'],
                ['C', 'Port 80'],
                ['D', 'Port 443']
            ],
            'correct_answer': 'C',
            'category': 'Module 4: Application Layer',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m4-002',
            'question': 'What does DNS stand for?',
            'options': [
                ['A', 'Domain Name System'],
                ['B', 'Digital Network Service'],
                ['C', 'Data Naming Service'],
                ['D', 'Domain Network Server']
            ],
            'correct_answer': 'A',
            'category': 'Module 4: Application Layer',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m4-003',
            'question': 'Which protocol is used for secure web browsing?',
            'options': [
                ['A', 'HTTP'],
                ['B', 'HTTPS'],
                ['C', 'FTP'],
                ['D', 'SMTP']
            ],
            'correct_answer': 'B',
            'category': 'Module 4: Application Layer',
            'xp_reward': 5
        },
        
        # Module 5: Connecting to the Internet
        {
            'id': 'quiz-c2m5-001',
            'question': 'What does ISP stand for?',
            'options': [
                ['A', 'Internet Service Provider'],
                ['B', 'Internal System Protocol'],
                ['C', 'International Security Program'],
                ['D', 'Internet Security Protocol']
            ],
            'correct_answer': 'A',
            'category': 'Module 5: Connecting to Internet',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m5-002',
            'question': 'Which technology uses phone lines to provide internet?',
            'options': [
                ['A', 'Fiber'],
                ['B', 'Cable'],
                ['C', 'DSL'],
                ['D', 'Satellite']
            ],
            'correct_answer': 'C',
            'category': 'Module 5: Connecting to Internet',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m5-003',
            'question': 'What is a modem used for?',
            'options': [
                ['A', 'To store data'],
                ['B', 'To modulate and demodulate signals for internet connection'],
                ['C', 'To block viruses'],
                ['D', 'To connect wireless devices only']
            ],
            'correct_answer': 'B',
            'category': 'Module 5: Connecting to Internet',
            'xp_reward': 5
        },
        
        # Module 6: Troubleshooting and the Future of Networking
        {
            'id': 'quiz-c2m6-001',
            'question': 'What command tests connectivity to another host?',
            'options': [
                ['A', 'ls'],
                ['B', 'cd'],
                ['C', 'ping'],
                ['D', 'mkdir']
            ],
            'correct_answer': 'C',
            'category': 'Module 6: Troubleshooting',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m6-002',
            'question': 'What does traceroute do?',
            'options': [
                ['A', 'Deletes files'],
                ['B', 'Shows the path packets take to reach a destination'],
                ['C', 'Creates new directories'],
                ['D', 'Backs up data']
            ],
            'correct_answer': 'B',
            'category': 'Module 6: Troubleshooting',
            'xp_reward': 5
        },
        {
            'id': 'quiz-c2m6-003',
            'question': 'What is the cloud in networking terms?',
            'options': [
                ['A', 'Actual clouds in the sky'],
                ['B', 'A type of weather phenomenon'],
                ['C', 'Remote servers that store and process data'],
                ['D', 'A wireless mouse']
            ],
            'correct_answer': 'C',
            'category': 'Module 6: Troubleshooting',
            'xp_reward': 5
        }
    ]
    
    # Insert quizzes
    for quiz in quizzes:
        cursor.execute('''
            INSERT OR REPLACE INTO quizzes 
            (id, question, options, correct_answer, category, xp_reward)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            quiz['id'],
            quiz['question'],
            json.dumps(quiz['options']),
            quiz['correct_answer'],
            quiz['category'],
            quiz['xp_reward']
        ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Initialized {len(quizzes)} quiz questions!")
    print("\n📚 Course 2: The Bits and Bytes of Computer Networking")
    print("\nModules:")
    categories = set(q['category'] for q in quizzes)
    for cat in sorted(categories):
        count = sum(1 for q in quizzes if q['category'] == cat)
        print(f"  - {cat}: {count} questions")
    print(f"\n🎯 Total XP Available: {len(quizzes) * 5} XP")

if __name__ == "__main__":
    init_quizzes()
