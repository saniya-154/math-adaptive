# Math Adventures - Adaptive Learning Prototype

An AI-powered adaptive math learning system that personalizes puzzle difficulty based on user performance using FastAPI backend and Streamlit frontend.

## 🚀 Features

- **Adaptive Difficulty**: Automatically adjusts math puzzle difficulty based on user performance
- **Real-time Analytics**: Track accuracy, response times, and progress with interactive charts
- **Rule-based AI**: Simple yet effective adaptive logic for optimal challenge zone
- **Web Interface**: Modern Streamlit frontend with FastAPI backend
- **Performance Tracking**: Comprehensive session summaries and recommendations

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: Streamlit, Plotly
- **Adaptive Engine**: Rule-based logic with performance tracking
- **Data Visualization**: Plotly charts for progress analytics

## 📋 Project Structure
<img width="682" height="422" alt="image" src="https://github.com/user-attachments/assets/abd8b745-f612-480e-b96e-2e05d6230d80" />

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or 3.12
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/saniya-154/math-adaptive.git
   cd math-adaptive

### Create virtual environment

- python -m venv math_env
- math_env\Scripts\activate  # Windows
#### OR
- source math_env/bin/activate  # macOS/Linux

### Install dependencies

- pip install -r requirements.txt

## Running the Application

### Start the Backend Server (Terminal 1)

- cd backend
- python main.py
- Server runs on: http://localhost:8000

### Start the Frontend (Terminal 2)

- cd frontend
- streamlit run app.py
- App runs on: http://localhost:8501

## 🎯 How It Works

- User Starts Session: Chooses initial difficulty (Easy/Medium/Hard)

- Puzzle Generation: System generates math problems appropriate to current level

- Performance Tracking: Records correctness and response time for each answer

- Adaptive Adjustment:

   2+ consecutive correct answers → Increase difficulty

   2+ consecutive wrong answers → Decrease difficulty

- Progress Analytics: Real-time charts show accuracy and response time trends

## 📊 Adaptive Logic
The system uses a rule-based approach:

- Easy: Single-digit addition/subtraction

- Medium: Two-digit operations, simple multiplication

- Hard: Larger numbers, division, complex operations

Adaptation based on:

- Correct/incorrect answer patterns

- Response time thresholds

- Consecutive performance streaks

## 🎨 Features Demo

- Interactive Math Challenges: Dynamic puzzle generation

- Real-time Performance Metrics: Live accuracy and timing stats

- Visual Progress Tracking: Plotly charts for analytics

- Session Summaries: Detailed performance reports

- Personalized Recommendations: AI-driven learning suggestions

🔧 API Endpoints
- POST /start-session - Initialize learning session

- POST /get-puzzle - Generate new math puzzle

- POST /submit-answer - Submit answer and get adaptive response

- GET /session-summary/{user_id} - Get comprehensive session report

## 📝 Assignment Requirements
✅ Core Components Implemented:

- Puzzle Generator with 3 difficulty levels

- Performance Tracker (correctness, response time)

- Adaptive Engine (rule-based logic)

- Progress Summary with analytics

✅ Technical Features:

- FastAPI RESTful backend

- Streamlit interactive frontend

- Real-time data visualization

- Modular, extensible architecture

## 🤝 Contributing

- Fork the repository

- Create a feature branch (git checkout -b feature/amazing-feature)

- Commit your changes (git commit -m 'Add amazing feature')

- Push to the branch (git push origin feature/amazing-feature)

- Open a Pull Request

## 📄 License
This project is created for educational purposes as part of an adaptive learning assignment.

## 👥 Authors
Saniya Sayyed
