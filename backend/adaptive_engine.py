from models import Difficulty

class AdaptiveEngine:
    def __init__(self):
        self.user_sessions = {}  # Store user session data
    
    def initialize_user_session(self, user_id: str, initial_difficulty: Difficulty = Difficulty.MEDIUM):
        """Initialize a new user session"""
        self.user_sessions[user_id] = {
            'current_difficulty': initial_difficulty,
            'consecutive_correct': 0,
            'consecutive_wrong': 0,
            'performance_history': []
        }
    
    def decide_next_difficulty(self, user_id: str, is_correct: bool, response_time: float) -> Difficulty:
        """Rule-based adaptive logic to determine next difficulty"""
        if user_id not in self.user_sessions:
            self.initialize_user_session(user_id)
        
        session = self.user_sessions[user_id]
        current_difficulty = session['current_difficulty']
        
        # Update consecutive counters
        if is_correct:
            session['consecutive_correct'] += 1
            session['consecutive_wrong'] = 0
        else:
            session['consecutive_wrong'] += 1
            session['consecutive_correct'] = 0
        
        # Record performance
        session['performance_history'].append({
            'is_correct': is_correct,
            'response_time': response_time,
            'difficulty': current_difficulty
        })
        
        # Define difficulty order
        difficulty_levels = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
        current_index = difficulty_levels.index(current_difficulty)
        
        # Adaptive logic
        if is_correct:
            if response_time < 5 and session['consecutive_correct'] >= 2:
                # Increase difficulty if not at max
                if current_index < len(difficulty_levels) - 1:
                    next_difficulty = difficulty_levels[current_index + 1]
                    session['consecutive_correct'] = 0
                    session['current_difficulty'] = next_difficulty
                    return next_difficulty
        else:
            if session['consecutive_wrong'] >= 2:
                # Decrease difficulty if not at min
                if current_index > 0:
                    next_difficulty = difficulty_levels[current_index - 1]
                    session['consecutive_wrong'] = 0
                    session['current_difficulty'] = next_difficulty
                    return next_difficulty
        
        # Maintain current difficulty
        return current_difficulty
    
    def get_user_stats(self, user_id: str) -> dict:
        """Get user performance statistics"""
        if user_id not in self.user_sessions:
            return {}
        
        session = self.user_sessions[user_id]
        history = session['performance_history']
        
        if not history:
            return {}
        
        total_questions = len(history)
        correct_answers = sum(1 for h in history if h['is_correct'])
        accuracy = correct_answers / total_questions if total_questions > 0 else 0
        avg_response_time = sum(h['response_time'] for h in history) / total_questions
        
        return {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'accuracy': accuracy,
            'average_response_time': avg_response_time,
            'current_difficulty': session['current_difficulty'],
            'difficulty_history': [h['difficulty'] for h in history]
        }