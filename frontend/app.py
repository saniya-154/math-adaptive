import streamlit as st
import requests
import time
import pandas as pd
import plotly.express as px
from datetime import datetime

# API configuration
API_BASE_URL = "http://localhost:8000"

def initialize_session_state():
    """Initialize session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'current_puzzle' not in st.session_state:
        st.session_state.current_puzzle = None
    if 'session_started' not in st.session_state:
        st.session_state.session_started = False
    if 'puzzle_start_time' not in st.session_state:
        st.session_state.puzzle_start_time = None
    if 'performance_history' not in st.session_state:
        st.session_state.performance_history = []
    if 'current_difficulty' not in st.session_state:
        st.session_state.current_difficulty = "MEDIUM"

def start_session(difficulty):
    """Start a new learning session"""
    try:
        response = requests.post(f"{API_BASE_URL}/start-session", params={"difficulty": difficulty})
        if response.status_code == 200:
            data = response.json()
            st.session_state.user_id = data['user_id']
            st.session_state.session_started = True
            st.session_state.current_difficulty = difficulty
            st.session_state.performance_history = []
            st.success(f"Session started! Initial difficulty: {difficulty}")
            return True
        else:
            st.error("Failed to start session")
            return False
    except Exception as e:
        st.error(f"Error starting session: {e}")
        st.info("Make sure the backend is running on http://localhost:8000")
        return False

def get_new_puzzle():
    """Get a new puzzle from the API"""
    if not st.session_state.user_id:
        st.error("No active session")
        return None
    
    try:
        request_data = {
            "user_id": st.session_state.user_id,
            "difficulty": st.session_state.current_difficulty
        }
        response = requests.post(f"{API_BASE_URL}/get-puzzle", json=request_data)
        if response.status_code == 200:
            puzzle_data = response.json()
            st.session_state.current_puzzle = puzzle_data
            st.session_state.puzzle_start_time = time.time()
            return puzzle_data
        else:
            st.error("Failed to get new puzzle")
            return None
    except Exception as e:
        st.error(f"Error getting puzzle: {e}")
        st.info("Make sure the backend is running on http://localhost:8000")
        return None

def submit_answer(user_answer):
    """Submit answer and process response"""
    if not st.session_state.current_puzzle:
        st.error("No active puzzle")
        return None
    
    try:
        response_time = time.time() - st.session_state.puzzle_start_time
        
        request_data = {
            "user_id": st.session_state.user_id,
            "puzzle_id": st.session_state.current_puzzle['puzzle_id'],
            "user_answer": float(user_answer),
            "response_time": response_time
        }
        
        response = requests.post(f"{API_BASE_URL}/submit-answer", json=request_data)
        if response.status_code == 200:
            result = response.json()
            
            # Record performance for visualization
            st.session_state.performance_history.append({
                'difficulty': st.session_state.current_difficulty,
                'is_correct': result['is_correct'],
                'response_time': response_time,
                'timestamp': datetime.now()
            })
            
            # Update current difficulty
            st.session_state.current_difficulty = result['next_difficulty']
            st.session_state.current_puzzle = None
            
            return result
        else:
            st.error("Failed to submit answer")
            return None
    except Exception as e:
        st.error(f"Error submitting answer: {e}")
        return None

def get_session_summary():
    """Get session summary from API"""
    if not st.session_state.user_id:
        return None
    
    try:
        response = requests.get(f"{API_BASE_URL}/session-summary/{st.session_state.user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def display_welcome():
    """Display welcome page"""
    st.title("🎯 Math Adventures")
    st.subheader("AI-Powered Adaptive Learning")
    
    st.markdown("""
    Welcome to Math Adventures! This intelligent learning system adapts to your skill level 
    and provides personalized math challenges to help you learn effectively.
    
    
    ### How it works:
    1. Choose your starting difficulty
    2. Solve math problems
    3. The system adapts based on your performance
    4. Review your progress and get recommendations
    """)
    
    # Difficulty selection - using a single row without nesting
    st.markdown("### Let's Get Started!")
    
    # Create buttons in a row without nested columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎈 Easy", use_container_width=True, key="easy_btn"):
            if start_session("EASY"):
                st.rerun()
    
    with col2:
        if st.button("🎯 Medium", use_container_width=True, key="medium_btn"):
            if start_session("MEDIUM"):
                st.rerun()
    
    with col3:
        if st.button("🚀 Hard", use_container_width=True, key="hard_btn"):
            if start_session("HARD"):
                st.rerun()
    
    # Difficulty descriptions
    st.markdown("""
    **Difficulty Levels:**
    - **Easy**: Single-digit addition and subtraction
    - **Medium**: Two-digit operations and simple multiplication  
    - **Hard**: Larger numbers, division, and complex operations
    """)

def display_puzzle_interface():
    """Display the main puzzle interface without nested columns"""
    st.header("🧩 Math Challenge")
    
    # Session info - single row of metrics
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    
    with metrics_col1:
        st.metric("Current Difficulty", st.session_state.current_difficulty)
    
    with metrics_col2:
        total_questions = len(st.session_state.performance_history)
        st.metric("Questions Solved", total_questions)
    
    with metrics_col3:
        correct_answers = sum(1 for p in st.session_state.performance_history if p['is_correct'])
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    st.markdown("---")
    
    # Puzzle section - no nested columns here
    if not st.session_state.current_puzzle:
        st.markdown("### Ready for a challenge?")
        if st.button("🎲 Get New Puzzle", type="primary", key="get_puzzle"):
            get_new_puzzle()
            st.rerun()
    else:
        puzzle = st.session_state.current_puzzle
        
        # Display puzzle in a clean layout
        st.markdown(f"### {puzzle['question']}")
        
        # Answer input
        user_answer = st.number_input(
            "Your answer:",
            value=None,
            placeholder="Enter your answer here...",
            key="answer_input"
        )
        
        # Action buttons in a single row
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            if st.button("✅ Submit Answer", type="primary", use_container_width=True, key="submit_btn"):
                if user_answer is not None:
                    result = submit_answer(user_answer)
                    if result:
                        display_feedback(result)
                else:
                    st.warning("Please enter an answer before submitting.")
        
        with action_col2:
            if st.button("🔄 Skip Puzzle", use_container_width=True, key="skip_btn"):
                st.session_state.current_puzzle = None
                st.rerun()

def display_feedback(result):
    """Display feedback after answering"""
    st.markdown("---")
    
    if result['is_correct']:
        st.success("🎉 Correct! Well done!")
        st.balloons()
    else:
        st.error(f"❌ Incorrect. The correct answer was: **{result['correct_answer']}**")
    
    # Performance stats in a single row
    stats = result.get('performance_stats', {})
    if stats:
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.metric("Total Questions", stats.get('total_questions', 0))
        
        with stat_col2:
            accuracy = stats.get('accuracy', 0)
            st.metric("Accuracy", f"{accuracy:.1%}")
        
        with stat_col3:
            st.metric("Next Difficulty", result['next_difficulty'])
    
    # Continue button
    if st.button("➡️ Continue", type="primary", key="continue_btn"):
        st.rerun()

def display_analytics():
    """Display performance analytics without nested columns"""
    if not st.session_state.performance_history:
        return
    
    st.header("📊 Performance Analytics")
    
    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.performance_history)
    df['question_number'] = range(1, len(df) + 1)
    
    # Accuracy over time chart
    df['cumulative_accuracy'] = df['is_correct'].expanding().mean()
    
    st.subheader("Accuracy Progress Over Time")
    fig_accuracy = px.line(
        df, 
        x='question_number', 
        y='cumulative_accuracy',
        title='',
        labels={'question_number': 'Question Number', 'cumulative_accuracy': 'Accuracy'}
    )
    fig_accuracy.update_layout(yaxis_tickformat='.0%')
    st.plotly_chart(fig_accuracy, use_container_width=True)
    
    # Response time and difficulty charts in separate sections
    st.subheader("Response Time Analysis")
    fig_time = px.box(
        df, 
        x='difficulty', 
        y='response_time',
        title='Response Time by Difficulty Level',
        labels={'difficulty': 'Difficulty', 'response_time': 'Response Time (seconds)'}
    )
    st.plotly_chart(fig_time, use_container_width=True)
    
    st.subheader("Questions by Difficulty")
    difficulty_counts = df['difficulty'].value_counts()
    fig_pie = px.pie(
        values=difficulty_counts.values,
        names=difficulty_counts.index,
        title='Distribution of Questions Across Difficulty Levels'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

def display_session_summary():
    """Display end of session summary"""
    summary = get_session_summary()
    
    st.header("📋 Session Summary")
    
    if summary:
        # Summary metrics in a single row
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric("Total Questions", summary['total_questions'])
        
        with summary_col2:
            st.metric("Correct Answers", summary['correct_answers'])
        
        with summary_col3:
            st.metric("Accuracy", f"{summary['accuracy']:.1%}")
        
        with summary_col4:
            st.metric("Avg Response Time", f"{summary['average_response_time']:.1f}s")
        
        # Recommendation
        st.info(f"💡 **Recommendation**: {summary['recommendation']}")
        
        # Difficulty progression
        st.subheader("Difficulty Progression")
        difficulty_text = " → ".join([f"**{diff}**" for diff in summary['difficulty_history'][-10:]])
        st.markdown(difficulty_text)
    else:
        st.warning("No session summary available. Complete some puzzles first!")
    
    # Restart session button
    if st.button("🔄 Start New Session", type="primary", key="new_session"):
        st.session_state.session_started = False
        st.session_state.user_id = None
        st.session_state.current_puzzle = None
        st.rerun()

def main():
    """Main application without complex nesting"""
    st.set_page_config(
        page_title="Math Adventures",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    
    # Sidebar - simple layout
    with st.sidebar:
        st.title("Math Adventures")
        st.markdown("---")
        
        if st.session_state.session_started:
            st.subheader("Session Controls")
            if st.button("📊 Show Summary", key="sidebar_summary"):
                # This will show the summary in the main area
                pass
            if st.button("🛑 End Session", key="sidebar_end"):
                st.session_state.session_started = False
                st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This adaptive learning system uses AI to personalize 
        your math learning experience based on your performance.
        
        **Features:**
        - Adaptive difficulty adjustment
        - Real-time performance tracking
        - Visual progress analytics
        - Personalized recommendations
        """)
    
    # Main content area - simple conditional rendering
    if not st.session_state.session_started:
        display_welcome()
    else:
        # Main game interface
        display_puzzle_interface()
        
        # Analytics section (appears after some questions)
        if len(st.session_state.performance_history) >= 3:
            st.markdown("---")
            display_analytics()
        
        # Show summary if requested or after enough questions
        if len(st.session_state.performance_history) >= 5:
            st.markdown("---")
            if st.button("📋 View Detailed Summary", type="secondary", key="main_summary"):
                display_session_summary()
        elif st.session_state.get('show_summary', False):
            display_session_summary()

if __name__ == "__main__":
    main()