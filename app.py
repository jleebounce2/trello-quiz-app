#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
import os, json
from psycopg2 import connect

app = Flask(__name__)
NEON_URL = os.environ.get('NEON_DATABASE_URL')
VALID_MEMBERS = ['Jason', 'Edward', 'Gourav', 'Ibitola', 'Olabode']

def get_db_connection():
    if not NEON_URL: raise Exception("NEON_DATABASE_URL not set")
    conn = connect(NEON_URL)
    conn.autocommit = False
    return conn

@app.route('/')
def index():
    return render_template('index.html', members=VALID_MEMBERS)

@app.route('/quiz')
def quiz_list():
    member = request.args.get('member', '')
    if not member or member not in VALID_MEMBERS: return redirect(url_for('index'))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT q.*, qa.answer as user_answer, qa.correct as user_correct FROM quizzes q LEFT JOIN quiz_attempts qa ON q.id = qa.quiz_id AND qa.member_name = %s ORDER BY q.category', (member,))
        quizzes = [{'id': r[0], 'question': r[1], 'options': json.loads(r[2]), 'correct_answer': r[3], 'category': r[4], 'xp_reward': r[5], 'user_answer': r[7], 'user_correct': r[8]} for r in cursor.fetchall()]
        cursor.execute('SELECT total_xp FROM members WHERE name = %s', (member,))
        total_xp = cursor.fetchone()[0] if cursor.fetchone() else 0
    finally:
        cursor.close(); conn.close()
    categories = {}
    for q in quizzes:
        categories.setdefault(q['category'], []).append(q)
    return render_template('quiz_list.html', categories=categories, member=member, total_xp=total_xp)

@app.route('/quiz/<quiz_id>')
def quiz_take(quiz_id):
    member = request.args.get('member', '')
    if not member or member not in VALID_MEMBERS: return redirect(url_for('index'))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM quizzes WHERE id = %s', (quiz_id,))
        r = cursor.fetchone()
        if not r: return "Quiz not found", 404
        quiz = {'id': r[0], 'question': r[1], 'options': json.loads(r[2]), 'correct_answer': r[3], 'xp_reward': r[5]}
        cursor.execute('SELECT * FROM quiz_attempts WHERE quiz_id = %s AND member_name = %s', (quiz_id, member))
        attempt = cursor.fetchone()
        cursor.execute('SELECT total_xp FROM members WHERE name = %s', (member,))
        total_xp = cursor.fetchone()[0]
    finally:
        cursor.close(); conn.close()
    return render_template('quiz_take.html', quiz=quiz, attempt=attempt, member=member, total_xp=total_xp)

@app.route('/quiz/<quiz_id>/submit', methods=['POST'])
def quiz_submit(quiz_id):
    member = request.args.get('member', '')
    answer = request.form.get('answer', '')
    if not member or member not in VALID_MEMBERS: return redirect(url_for('index'))
    if not answer: return "No answer selected", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM quizzes WHERE id = %s', (quiz_id,))
        r = cursor.fetchone()
        quiz = {'id': r[0], 'question': r[1], 'options': json.loads(r[2]), 'correct_answer': r[3], 'xp_reward': r[5]}
        cursor.execute('SELECT * FROM quiz_attempts WHERE quiz_id = %s AND member_name = %s', (quiz_id, member))
        if cursor.fetchone(): return redirect(url_for('quiz_take', quiz_id=quiz_id, member=member))
        correct = (answer == quiz['correct_answer'])
        xp = quiz['xp_reward'] if correct else 0
        cursor.execute('INSERT INTO quiz_attempts (member_name, quiz_id, answer, correct, xp_awarded) VALUES (%s, %s, %s, %s, %s)', (member, quiz_id, answer, correct, xp))
        if xp > 0:
            cursor.execute('UPDATE members SET total_xp = total_xp + %s WHERE name = %s', (xp, member))
            cursor.execute('INSERT INTO xp_log (member_name, xp_change, reason, card_id, card_name) VALUES (%s, %s, %s, %s, %s)', (member, xp, f"Quiz: {quiz['question'][:50]}", 'QUIZ', quiz['question']))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close(); conn.close()
    return render_template('quiz_result.html', quiz=quiz, answer=answer, correct=correct, xp_awarded=xp, member=member)

@app.route('/leaderboard')
def leaderboard():
    member = request.args.get('member', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT name, total_xp FROM members ORDER BY total_xp DESC')
        overall = cursor.fetchall()
        cursor.execute('SELECT member_name, COUNT(*), SUM(CASE WHEN correct THEN 1 ELSE 0 END), SUM(xp_awarded) FROM quiz_attempts GROUP BY member_name ORDER BY SUM(xp_awarded) DESC')
        quiz_stats = cursor.fetchall()
    finally:
        cursor.close(); conn.close()
    return render_template('leaderboard.html', overall=overall, quiz_stats=quiz_stats, member=member)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
