#!/usr/bin/env python3
"""
Quiz App for Trello Gamification
A simple web app for team quizzes with XP integration.
Deployed on Vercel with Neon PostgreSQL.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime
from psycopg2 import connect

app = Flask(__name__)

# Neon PostgreSQL connection
NEON_URL = os.environ.get('NEON_DATABASE_URL', 'postgresql://neondb_owner:npg_X8N6kQFSmcBa@ep-wandering-brook-adu1zeum-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require')

# Valid members
VALID_MEMBERS = ['Jason', 'Edward', 'Gourav', 'Ibitola', 'Olabode']

def get_db_connection():
    """Get database connection."""
    conn = connect(NEON_URL)
    conn.autocommit = False
    return conn

def award_xp(member_name, xp, reason, cursor):
    """Award XP to a member."""
    # Update member stats
    cursor.execute('''
        UPDATE members 
        SET total_xp = total_xp + %s,
            last_updated = NOW()
        WHERE name = %s
    ''', (xp, member_name))
    
    # Log the transaction
    cursor.execute('''
        INSERT INTO xp_log (member_name, xp_change, reason, card_id, card_name)
        VALUES (%s, %s, %s, %s, %s)
    ''', (member_name, xp, reason, 'QUIZ', 'Quiz Question'))

@app.route('/')
def index():
    """Home page - select user."""
    return render_template('index.html', members=VALID_MEMBERS)

@app.route('/quiz')
def quiz_list():
    """List all available quizzes."""
    member = request.args.get('member', '')
    
    if not member or member not in VALID_MEMBERS:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get all quizzes with user's attempt status
        cursor.execute('''
            SELECT 
                q.*,
                qa.answer as user_answer,
                qa.correct as user_correct,
                qa.xp_awarded
            FROM quizzes q
            LEFT JOIN quiz_attempts qa ON q.id = qa.quiz_id AND qa.member_name = %s
            ORDER BY q.category, q.created_at DESC
        ''', (member,))
        
        quizzes = []
        for row in cursor.fetchall():
            quiz = {
                'id': row[0],
                'question': row[1],
                'options': row[2] if isinstance(row[2], list) else json.loads(row[2]),
                'correct_answer': row[3],
                'category': row[4],
                'xp_reward': row[5],
                'created_at': row[6],
                'user_answer': row[7],
                'user_correct': row[8],
                'xp_awarded': row[9]
            }
            quizzes.append(quiz)
        
        # Get user's stats
        cursor.execute('SELECT total_xp FROM members WHERE name = %s', (member,))
        user_stats = cursor.fetchone()
        total_xp = user_stats[0] if user_stats else 0
        
    finally:
        cursor.close()
        conn.close()
    
    # Group by category
    categories = {}
    for quiz in quizzes:
        cat = quiz['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(quiz)
    
    return render_template('quiz_list.html', 
                         categories=categories, 
                         member=member, 
                         total_xp=total_xp)

@app.route('/quiz/<quiz_id>')
def quiz_take(quiz_id):
    """Take a quiz."""
    member = request.args.get('member', '')
    
    if not member or member not in VALID_MEMBERS:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get quiz
        cursor.execute('SELECT * FROM quizzes WHERE id = %s', (quiz_id,))
        quiz_row = cursor.fetchone()
        
        if not quiz_row:
            return "Quiz not found", 404
        
        quiz = {
            'id': quiz_row[0],
            'question': quiz_row[1],
            'options': quiz_row[2] if isinstance(quiz_row[2], list) else json.loads(quiz_row[2]),
            'correct_answer': quiz_row[3],
            'category': quiz_row[4],
            'xp_reward': quiz_row[5],
            'created_at': quiz_row[6]
        }
        
        # Check if already attempted
        cursor.execute('''
            SELECT * FROM quiz_attempts 
            WHERE quiz_id = %s AND member_name = %s
        ''', (quiz_id, member))
        
        attempt = cursor.fetchone()
        
        # Get user's stats
        cursor.execute('SELECT total_xp FROM members WHERE name = %s', (member,))
        user_stats = cursor.fetchone()
        total_xp = user_stats[0] if user_stats else 0
        
    finally:
        cursor.close()
        conn.close()
    
    return render_template('quiz_take.html', 
                         quiz=quiz, 
                         attempt=attempt, 
                         member=member,
                         total_xp=total_xp)

@app.route('/quiz/<quiz_id>/submit', methods=['POST'])
def quiz_submit(quiz_id):
    """Submit quiz answer."""
    member = request.args.get('member', '')
    answer = request.form.get('answer', '')
    
    if not member or member not in VALID_MEMBERS:
        return redirect(url_for('index'))
    
    if not answer:
        return "No answer selected", 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get quiz
        cursor.execute('SELECT * FROM quizzes WHERE id = %s', (quiz_id,))
        quiz_row = cursor.fetchone()
        
        if not quiz_row:
            return "Quiz not found", 404
        
        quiz = {
            'id': quiz_row[0],
            'question': quiz_row[1],
            'options': quiz_row[2] if isinstance(quiz_row[2], list) else json.loads(quiz_row[2]),
            'correct_answer': quiz_row[3],
            'category': quiz_row[4],
            'xp_reward': quiz_row[5],
            'created_at': quiz_row[6]
        }
        
        # Check if already attempted
        cursor.execute('''
            SELECT * FROM quiz_attempts 
            WHERE quiz_id = %s AND member_name = %s
        ''', (quiz_id, member))
        
        existing = cursor.fetchone()
        
        if existing:
            return redirect(url_for('quiz_take', quiz_id=quiz_id, member=member))
        
        # Check answer
        correct = (answer == quiz['correct_answer'])
        xp_awarded = quiz['xp_reward'] if correct else 0
        
        # Record attempt
        cursor.execute('''
            INSERT INTO quiz_attempts (member_name, quiz_id, answer, correct, xp_awarded)
            VALUES (%s, %s, %s, %s, %s)
        ''', (member, quiz_id, answer, correct, xp_awarded))
        
        # Award XP if correct
        if xp_awarded > 0:
            award_xp(member, xp_awarded, f"Quiz: {quiz['question'][:50]}", cursor)
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
    
    return render_template('quiz_result.html', 
                         quiz=quiz, 
                         answer=answer,
                         correct=correct,
                         xp_awarded=xp_awarded,
                         member=member)

@app.route('/leaderboard')
def leaderboard():
    """Show quiz leaderboard."""
    member = request.args.get('member', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get overall leaderboard
        cursor.execute('''
            SELECT name, total_xp FROM members 
            ORDER BY total_xp DESC
        ''')
        overall = cursor.fetchall()
        
        # Get quiz-specific stats
        cursor.execute('''
            SELECT 
                member_name,
                COUNT(*) as total_attempts,
                SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
                SUM(xp_awarded) as total_xp
            FROM quiz_attempts
            GROUP BY member_name
            ORDER BY total_xp DESC
        ''')
        quiz_stats = cursor.fetchall()
        
    finally:
        cursor.close()
        conn.close()
    
    return render_template('leaderboard.html', 
                         overall=overall,
                         quiz_stats=quiz_stats,
                         member=member)

# Vercel serverless handler
def handler(request):
    """Vercel serverless function handler."""
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
