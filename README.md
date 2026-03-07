# 🧠 Team Quiz App

A simple quiz web app integrated with the Trello gamification system.

## Features

- ✅ 12 starter quiz questions (Security, Git, API, Troubleshooting)
- ✅ XP integration with existing gamification database
- ✅ Individual progress tracking
- ✅ Live leaderboard
- ✅ One attempt per quiz per person (anti-cheat)
- ✅ Mobile-friendly interface

## Quick Start

### Local Development

```bash
cd quiz-app
pip3 install -r requirements.txt
python3 init_quizzes.py  # Initialize quiz questions
python3 app.py
```

Open http://localhost:5001

### Deploy to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Done!

## How It Works

1. User selects their name (Jason, Edward, Gourav, Ibitola, Olabode)
2. Browse available quizzes by category
3. Answer multiple choice questions
4. Get instant feedback + XP if correct
5. XP is stored in the same database as Trello gamification
6. Unified leaderboard shows all XP sources

## Database

Uses the existing `trello-gamification.db` with two new tables:

- `quizzes` - Question bank
- `quiz_attempts` - Track who answered what

## Adding New Quizzes

Edit `init_quizzes.py` and add to the `quizzes` list:

```python
{
    'id': 'quiz-unique-id',
    'question': 'Your question here?',
    'options': [['A', 'Option 1'], ['B', 'Option 2'], ...],
    'correct_answer': 'A',
    'category': 'Security',  # or Git, API, Troubleshooting
    'xp_reward': 5
}
```

Then run `python3 init_quizzes.py` again.

## Tech Stack

- **Backend:** Python Flask
- **Database:** SQLite (shared with Trello system)
- **Frontend:** HTML/CSS (no JS framework needed)
- **Hosting:** Vercel (free tier)

## Routes

- `/` - Home (select user)
- `/quiz?member=Jason` - Quiz list
- `/quiz/<id>?member=Jason` - Take quiz
- `/leaderboard` - View rankings

## Future Enhancements

- [ ] Streak tracking
- [ ] Quiz seasons (monthly resets)
- [ ] Badge system
- [ ] Hard mode quizzes
- [ ] Team challenges
- [ ] Telegram bot integration

---

Built for Group A3 gamification 🦞
