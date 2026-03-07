#!/bin/bash
# Start the Quiz App locally

echo "🧠 Starting Team Quiz App..."
echo ""

cd /Users/abc/.openclaw/workspace/quiz-app

# Initialize database if needed
python3 init_quizzes.py

# Start the app
echo ""
echo "✅ Quiz app ready!"
echo "🌐 Open: http://localhost:5001"
echo ""

python3 app.py
