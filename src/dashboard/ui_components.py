import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import os
from PIL import Image

def display_metrics_cards(metrics):
    """Display metrics as cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Stress Level", f"{metrics['stress']:.2f}", 
                 delta=None, delta_color="inverse")
    
    with col2:
        st.metric("Engagement", f"{metrics['engagement']:.2f}", 
                 delta=None, delta_color="normal")
    
    with col3:
        st.metric("Confusion", f"{metrics['confusion']:.2f}", 
                 delta=None, delta_color="inverse")
    
    with col4:
        st.metric("Confidence", f"{metrics['confidence']:.2f}", 
                 delta=None, delta_color="normal")

def display_stress_heat_indicator(stress_level):
    """Display stress heat indicator"""
    if stress_level < 0.3:
        color = "🟢"
        status = "Low"
    elif stress_level < 0.7:
        color = "🟡"
        status = "Moderate"
    else:
        color = "🔴"
        status = "High"
    
    st.markdown(f"### Stress Heat: {color} {status} ({stress_level:.2f})")

def display_dominant_state(dominant_state):
    """Display dominant emotional state"""
    state_colors = {
        'stressed': '🔴',
        'engaged': '🟢', 
        'calm': '🔵',
        'positive': '🟡',
        'negative': '🟠',
        'neutral': '⚪'
    }
    
    icon = state_colors.get(dominant_state, '⚪')
    st.subheader(f"Current State: {icon} {dominant_state.title()}")

def display_stress_alert(stress_history, threshold=0.7, duration=5):
    """Display stress alert if threshold exceeded for duration"""
    if len(stress_history) < duration:
        return False
    
    recent_stress = stress_history[-duration:]
    if all(stress > threshold for stress in recent_stress):
        st.error(f"⚠️ HIGH STRESS ALERT: Stress level above {threshold:.1f} for {duration} seconds!")
        return True
    return False

def display_emotion_breakdown(face_emotions):
    """Display face emotion breakdown with forced refresh"""
    if not face_emotions or not isinstance(face_emotions, dict):
        st.write("No emotion data available")
        return
    
    current_time = datetime.now().strftime('%H:%M:%S')
    st.subheader(f"Face Emotion Breakdown - {current_time}")
    
    emotion_data = []
    for emotion, score in face_emotions.items():
        if isinstance(score, (int, float)):
            emotion_data.append({
                "Emotion": emotion.title(), 
                "Score": f"{score:.3f}",
                "Percentage": f"{score*100:.1f}%"
            })
    
    if emotion_data:
        emotion_df = pd.DataFrame(emotion_data)
        # Use placeholder for forced refresh
        table_placeholder = st.empty()
        table_placeholder.dataframe(emotion_df, use_container_width=True, hide_index=True)

def display_session_comparison(df):
    """Display early vs late session comparison"""
    if df.empty or len(df) < 10:
        st.info("Not enough data for session comparison (need at least 10 data points)")
        return
    
    session_length = len(df)
    quarter_size = max(1, session_length // 4)
    
    early_session = df.head(quarter_size)
    late_session = df.tail(quarter_size)
    
    st.subheader("📊 Session Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Early Session (First 25%)**")
        st.metric("Avg Stress", f"{early_session['stress'].mean():.2f}")
        st.metric("Avg Engagement", f"{early_session['engagement'].mean():.2f}")
    
    with col2:
        st.write("**Late Session (Last 25%)**")
        st.metric("Avg Stress", f"{late_session['stress'].mean():.2f}")
        st.metric("Avg Engagement", f"{late_session['engagement'].mean():.2f}")

def display_session_analytics(stats):
    """Display advanced session analytics"""
    if not stats:
        return
    
    st.subheader("📊 Session Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'most_stressed' in stats and stats['most_stressed']:
            st.write(f"**Most Stressed:** {stats['most_stressed']['score']:.2f} at {stats['most_stressed']['timestamp'].strftime('%H:%M:%S')}")
        else:
            st.write("**Most Stressed:** Not available")
        
        if 'longest_stress_duration' in stats:
            st.write(f"**Longest Stress Duration:** {stats['longest_stress_duration']} seconds")
    
    with col2:
        if 'most_engaged' in stats and stats['most_engaged']:
            st.write(f"**Most Engaged:** {stats['most_engaged']['score']:.2f} at {stats['most_engaged']['timestamp'].strftime('%H:%M:%S')}")
        else:
            st.write("**Most Engaged:** Not available")
        
        if 'stability_score' in stats:
            st.write(f"**Emotional Stability:** {stats['stability_score']:.2f}")

def display_critical_moments(stats):
    """Display top critical moments"""
    if 'critical_moments' not in stats or not stats['critical_moments']:
        return
    
    st.subheader("⚠️ Top Critical Moments")
    
    for i, moment in enumerate(stats['critical_moments'], 1):
        st.write(f"**{i}.** {moment['timestamp'].strftime('%H:%M:%S')} - Stress: {moment['stress']:.2f}, Confusion: {moment['confusion']:.2f}")

def display_session_feedback(stats):
    """Display session feedback"""
    if 'feedback' not in stats:
        return
    
    st.subheader("💡 Session Feedback")
    
    for feedback in stats['feedback']:
        st.write(f"• {feedback}")
    
    if 'quality_score' in stats:
        quality = stats['quality_score']
        if quality >= 80:
            color = "🟢"
            grade = "Excellent"
        elif quality >= 60:
            color = "🟡"
            grade = "Good"
        else:
            color = "🔴"
            grade = "Needs Improvement"
        
        st.metric("Session Quality Score", f"{quality:.0f}/100", help=f"{color} {grade}")

def display_screenshot_gallery(screenshots):
    """Display screenshot gallery"""
    if not screenshots:
        st.info("No screenshots captured during this session. Use the '📸 Mark Moment' button to capture screenshots manually.")
        return
    
    st.subheader("📸 Screenshot Gallery")
    
    for screenshot in screenshots:
        if 'filepath' in screenshot and os.path.exists(screenshot['filepath']):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.write(f"**Type:** {screenshot['type']}")
                st.write(f"**Time:** {screenshot['timestamp'].strftime('%H:%M:%S')}")
                st.write(f"**Score:** {screenshot['score']:.2f}")
            
            with col2:
                try:
                    image = Image.open(screenshot['filepath'])
                    image.thumbnail((400, 300))
                    st.image(image, caption=f"{screenshot['type']} - {screenshot['timestamp'].strftime('%H:%M:%S')}")
                except Exception as e:
                    st.error(f"Could not load screenshot: {e}")
            
            st.divider()
        else:
            st.warning(f"Screenshot file not found: {screenshot.get('filepath', 'Unknown path')}")

def display_session_controls():
    """Display session control buttons"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        start_session = st.button("Start Session", type="primary")
    
    with col2:
        stop_session = st.button("Stop Session", type="secondary")
    
    with col3:
        simulation_mode = st.checkbox("Simulation Mode")
    
    with col4:
        manual_screenshot = st.button("📸 Mark Moment", help="Capture screenshot manually")
    
    return start_session, stop_session, simulation_mode, manual_screenshot

def display_about_info():
    """Display about information"""
    st.markdown("""
    ## About EMOTISENSE AI
    
    **EMOTISENSE AI** is a multimodal emotion recognition system that combines:
    
    - 🎥 **Face Emotion Detection**: Real-time facial emotion analysis using computer vision
    - 🎤 **Audio Stress Analysis**: Voice stress detection using audio signal processing
    - 🧠 **Fusion Engine**: Intelligent combination of multiple modalities
    - 📊 **Live Dashboard**: Real-time monitoring and visualization
    - 📈 **Session Reports**: Comprehensive analysis and PDF reports
    - 📸 **Smart Screenshots**: Automatic capture during critical moments
    - 🧠 **Session Intelligence**: Advanced analytics and feedback
    - 📊 **Quality Scoring**: Comprehensive session evaluation
    
    ### Features:
    - Real-time emotion monitoring
    - Stress level alerts
    - Session logging and reporting
    - Fallback mode for hardware failures
    - Export capabilities (CSV, PDF)
    - Automatic screenshot capture
    - Session analytics and feedback
    - Critical moment detection
    - Quality scoring system
    
    ### Technology Stack:
    - **Frontend**: Streamlit
    - **Computer Vision**: OpenCV, FER
    - **Audio Processing**: librosa, sounddevice
    - **Data Analysis**: pandas, numpy
    - **Visualization**: plotly
    - **Reports**: reportlab
    - **Screenshots**: pyautogui, Pillow
    """)