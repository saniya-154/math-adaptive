import random
import uuid
from models import Difficulty

class PuzzleGenerator:
    def __init__(self):
        self.operations = ['+', '-', '*', '/']
    
    def generate_puzzle(self, difficulty: Difficulty) -> tuple:
        """Generate math puzzles based on difficulty level"""
        puzzle_id = str(uuid.uuid4())[:8]
        
        if difficulty == Difficulty.EASY:
            question, answer = self._generate_easy()
        elif difficulty == Difficulty.MEDIUM:
            question, answer = self._generate_medium()
        else:  # Difficulty.HARD
            question, answer = self._generate_hard()
            
        return question, answer, puzzle_id
    
    def _generate_easy(self):
        """Easy: Single-digit addition/subtraction"""
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        operation = random.choice(['+', '-'])
        
        if operation == '+':
            answer = a + b
            question = f"{a} + {b} = ?"
        else:
            # Ensure positive results for subtraction
            a, b = max(a, b), min(a, b)
            answer = a - b
            question = f"{a} - {b} = ?"
            
        return question, answer
    
    def _generate_medium(self):
        """Medium: Two-digit operations, simple multiplication"""
        operation = random.choice(['+', '-', '*'])
        
        if operation in ['+', '-']:
            a = random.randint(10, 50)
            b = random.randint(10, 50)
            if operation == '+':
                answer = a + b
                question = f"{a} + {b} = ?"
            else:
                a, b = max(a, b), min(a, b)
                answer = a - b
                question = f"{a} - {b} = ?"
        else:  # multiplication
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            answer = a * b
            question = f"{a} × {b} = ?"
            
        return question, answer
    
    def _generate_hard(self):
        """Hard: Larger numbers, division, mixed operations"""
        operation = random.choice(['+', '-', '*', '/'])
        
        if operation in ['+', '-']:
            a = random.randint(50, 100)
            b = random.randint(50, 100)
            if operation == '+':
                answer = a + b
                question = f"{a} + {b} = ?"
            else:
                a, b = max(a, b), min(a, b)
                answer = a - b
                question = f"{a} - {b} = ?"
        elif operation == '*':
            a = random.randint(5, 20)
            b = random.randint(5, 20)
            answer = a * b
            question = f"{a} × {b} = ?"
        else:  # division
            b = random.randint(2, 12)
            answer = random.randint(2, 12)
            a = b * answer  # Ensure integer division
            question = f"{a} ÷ {b} = ?"
            
        return question, answer