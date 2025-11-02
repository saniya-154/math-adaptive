import time
from typing import Dict
from models import Difficulty

class PerformanceTracker:
    def __init__(self):
        self.user_sessions: Dict = {}
    
    def start_session(self, user_id: str, initial_difficulty: Difficulty):
        """Start a new tracking session for user"""
        self.user_sessions[user_id] = {
            'start_time': time.time(),
            'puzzles_attempted': 0,
            'correct_answers': 0,
            'response_times': [],
            'difficulty_history': [initial_difficulty],
            'current_puzzle_start': None
        }
    
    def start_puzzle_timer(self, user_id: str):
        """Start timer for current puzzle"""
        if user_id in self.user_sessions:
            self.user_sessions[user_id]['current_puzzle_start'] = time.time()
    
    def record_answer(self, user_id: str, is_correct: bool, difficulty: Difficulty):
        """Record user answer and calculate response time"""
        if user_id not in self.user_sessions:
            return 0
        
        session = self.user_sessions[user_id]
        response_time = 0
        
        if session['current_puzzle_start']:
            response_time = time.time() - session['current_puzzle_start']
            session['response_times'].append(response_time)
        
        session['puzzles_attempted'] += 1
        session['difficulty_history'].append(difficulty)
        
        if is_correct:
            session['correct_answers'] += 1
        
        session['current_puzzle_start'] = None
        return response_time
    
    def get_session_summary(self, user_id: str) -> dict:
        """Get comprehensive session summary"""
        if user_id not in self.user_sessions:
            return {}
        
        session = self.user_sessions[user_id]
        total = session['puzzles_attempted']
        correct = session['correct_answers']
        
        accuracy = correct / total if total > 0 else 0
        avg_time = sum(session['response_times']) / len(session['response_times']) if session['response_times'] else 0
        
        # Generate recommendation
        if accuracy > 0.8:
            recommendation = "Excellent! You're ready for more challenging problems!"
        elif accuracy > 0.6:
            recommendation = "Good progress! Keep practicing to improve consistency."
        else:
            recommendation = "Consider focusing on fundamental concepts. You'll get better with practice!"
        
        return {
            'total_questions': total,
            'correct_answers': correct,
            'accuracy': accuracy,
            'average_response_time': avg_time,
            'difficulty_history': session['difficulty_history'],
            'recommendation': recommendation
        }