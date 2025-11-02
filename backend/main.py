from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
import uuid
from models import *

app = FastAPI(title="Math Adventures API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage
user_sessions = {}
active_puzzles = {}

class Difficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

@app.post("/start-session")
async def start_session(difficulty: Difficulty = Difficulty.MEDIUM):
    """Start a new learning session"""
    user_id = str(uuid.uuid4())
    user_sessions[user_id] = {
        'current_difficulty': difficulty,
        'performance_history': [],
        'consecutive_correct': 0,
        'consecutive_wrong': 0
    }
    
    return {
        "user_id": user_id,
        "message": "Session started successfully",
        "initial_difficulty": difficulty
    }

@app.post("/get-puzzle")
async def get_puzzle(request: dict):
    """Get a new math puzzle"""
    user_id = request.get('user_id')
    difficulty = request.get('difficulty', 'MEDIUM')
    
    if user_id not in user_sessions:
        raise HTTPException(status_code=404, detail="User session not found")
    
    # Generate puzzle based on difficulty
    if difficulty == "EASY":
        a, b = random.randint(1, 10), random.randint(1, 10)
        operation = random.choice(['+', '-'])
        if operation == '+':
            question = f"{a} + {b} = ?"
            answer = a + b
        else:
            a, b = max(a, b), min(a, b)
            question = f"{a} - {b} = ?"
            answer = a - b
            
    elif difficulty == "MEDIUM":
        a, b = random.randint(10, 50), random.randint(10, 50)
        operation = random.choice(['+', '-', '*'])
        if operation == '+':
            question = f"{a} + {b} = ?"
            answer = a + b
        elif operation == '-':
            a, b = max(a, b), min(a, b)
            question = f"{a} - {b} = ?"
            answer = a - b
        else:
            a, b = random.randint(2, 12), random.randint(2, 12)
            question = f"{a} × {b} = ?"
            answer = a * b
    else:  # HARD
        a, b = random.randint(50, 100), random.randint(50, 100)
        operation = random.choice(['+', '-', '*', '/'])
        if operation == '+':
            question = f"{a} + {b} = ?"
            answer = a + b
        elif operation == '-':
            a, b = max(a, b), min(a, b)
            question = f"{a} - {b} = ?"
            answer = a - b
        elif operation == '*':
            question = f"{a} × {b} = ?"
            answer = a * b
        else:  # division
            b = random.randint(2, 12)
            answer = random.randint(2, 12)
            a = b * answer
            question = f"{a} ÷ {b} = ?"
    
    puzzle_id = str(uuid.uuid4())[:8]
    active_puzzles[puzzle_id] = {
        'correct_answer': answer,
        'user_id': user_id,
        'difficulty': difficulty
    }
    
    return {
        "question": question,
        "correct_answer": answer,
        "difficulty": difficulty,
        "puzzle_id": puzzle_id
    }

@app.post("/submit-answer")
async def submit_answer(request: dict):
    """Submit an answer and get adaptive response"""
    user_id = request.get('user_id')
    puzzle_id = request.get('puzzle_id')
    user_answer = request.get('user_answer')
    response_time = request.get('response_time', 0)
    
    if puzzle_id not in active_puzzles:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    puzzle_data = active_puzzles[puzzle_id]
    correct_answer = puzzle_data['correct_answer']
    
    # Check answer (with tolerance for floating point)
    is_correct = abs(user_answer - correct_answer) < 0.001
    
    # Update user session
    session = user_sessions[user_id]
    session['performance_history'].append({
        'is_correct': is_correct,
        'response_time': response_time,
        'difficulty': puzzle_data['difficulty']
    })
    
    # Simple adaptive logic
    if is_correct:
        session['consecutive_correct'] += 1
        session['consecutive_wrong'] = 0
        if session['consecutive_correct'] >= 2 and response_time < 8:
            # Increase difficulty
            difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
            current_index = difficulties.index(session['current_difficulty'])
            if current_index < len(difficulties) - 1:
                session['current_difficulty'] = difficulties[current_index + 1]
                session['consecutive_correct'] = 0
    else:
        session['consecutive_wrong'] += 1
        session['consecutive_correct'] = 0
        if session['consecutive_wrong'] >= 2:
            # Decrease difficulty
            difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
            current_index = difficulties.index(session['current_difficulty'])
            if current_index > 0:
                session['current_difficulty'] = difficulties[current_index - 1]
                session['consecutive_wrong'] = 0
    
    # Calculate stats
    history = session['performance_history']
    total_questions = len(history)
    correct_answers = sum(1 for h in history if h['is_correct'])
    accuracy = correct_answers / total_questions if total_questions > 0 else 0
    
    # Clean up
    del active_puzzles[puzzle_id]
    
    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "next_difficulty": session['current_difficulty'],
        "performance_stats": {
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy": accuracy,
            "current_difficulty": session['current_difficulty']
        }
    }

@app.get("/session-summary/{user_id}")
async def get_session_summary(user_id: str):
    """Get comprehensive session summary"""
    if user_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = user_sessions[user_id]
    history = session['performance_history']
    
    if not history:
        raise HTTPException(status_code=400, detail="No performance data available")
    
    total_questions = len(history)
    correct_answers = sum(1 for h in history if h['is_correct'])
    accuracy = correct_answers / total_questions
    avg_response_time = sum(h['response_time'] for h in history) / total_questions
    
    # Generate recommendation
    if accuracy > 0.8:
        recommendation = "Excellent! You're ready for more challenging problems!"
    elif accuracy > 0.6:
        recommendation = "Good progress! Keep practicing to improve consistency."
    else:
        recommendation = "Consider focusing on fundamental concepts. You'll get better with practice!"
    
    return {
        "user_id": user_id,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "accuracy": accuracy,
        "average_response_time": avg_response_time,
        "difficulty_history": [h['difficulty'] for h in history],
        "recommendation": recommendation
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Math Adventures API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)