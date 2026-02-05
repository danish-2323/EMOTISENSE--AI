project:
  name: "EMOTISENSE AI 🧠"
  subtitle: "Multimodal Emotion Recognition using Audio + Face"
  description: >
    A real-time emotion monitoring system that combines facial emotion detection
    and audio stress analysis to provide comprehensive emotional insights.

event:
  hackathon: "SRM IST × NOOBTRON — NOOB HACKFEST"
  host: "SRM Institute of Science and Technology, Tiruchirappalli"
  track:
    name: "Track – 1"
    theme: "Artificial Intelligence & Machine Learning"
    sub_theme: "1.1.6 Multimodal Emotion Recognition using Audio-Visual Cues"

quick_start:
  command: "pip install -r requirements.txt && streamlit run app.py"
  url: "http://localhost:8501"

project_structure:
  EMOTISENSE-AI:
    - app.py: "Main Streamlit application"
    - requirements.txt: "Python dependencies"
    - README.md: "Project documentation"
    - src:
        - config.py: "Configuration settings"
        - utils.py: "Utility functions"
        - webcam:
            - camera.py: "Camera capture"
            - face_emotion.py: "Face emotion detection"
        - audio:
            - mic_capture.py: "Microphone capture"
            - audio_emotion.py: "Audio stress analysis"
        - fusion:
            - fusion_engine.py: "Multimodal fusion logic"
        - dashboard:
            - ui_components.py: "UI components"
            - plots.py: "Visualization charts"
        - logger:
            - session_logger.py: "Session logging"
            - report_generator.py: "PDF report generation"
        - fallback:
            - rule_based.py: "Simulation / fallback mode"
        - analytics:
            - session_insights.py: "Session intelligence & metrics"
            - feedback_engine.py: "Rule-based feedback generation"
    - outputs:
        - session_logs: "Session CSV files"
        - reports: "Generated PDF reports"
        - snapshots: "Auto-captured screenshots"

features:
  core:
    - "Real-time face emotion detection (happy, sad, angry, fear, surprise, neutral)"
    - "Audio stress analysis from microphone input"
    - "Multimodal fusion engine (face + audio)"
    - "Live dashboard with real-time metrics and alerts"
    - "Session logging with CSV export"
    - "PDF report generation with insights"

  advanced:
    - "Automatic screenshot capture on extreme stress"
    - "Automatic screenshot capture on extreme happiness"
    - "Distraction-based screenshot capture"
    - "Emotion timeline analysis"
    - "Top critical moments detection"
    - "Emotion stability score"
    - "Recovery speed measurement"
    - "Attention span estimation"
    - "Session risk indicator (Low / Medium / High)"
    - "Session quality score (0–100)"

dashboard_tabs:
  - "Live Dashboard"
  - "Session Report"
  - "Screenshot Gallery"
  - "About"

fallback_and_safety:
  - "Simulation mode (no camera/microphone required)"
  - "Automatic hardware failure handling"
  - "Manual mark important moment button"
  - "Local execution for privacy"
  - "Graceful error handling"

technology_stack:
  frontend: "Streamlit"
  computer_vision: ["OpenCV", "FER"]
  audio_processing: ["sounddevice", "librosa"]
  data_analysis: ["pandas", "numpy"]
  visualization: "plotly"
  reports: "reportlab"
  backup: "DeepFace"

metrics:
  primary:
    - "Stress (0–1)"
    - "Engagement (0–1)"
    - "Confidence (0–1)"
    - "Confusion (0–1)"
  emotional_states:
    - "Stressed"
    - "Engaged"
    - "Calm"
    - "Positive"
    - "Negative"
    - "Neutral"
  audio_features:
    - "RMS Energy"
    - "Zero Crossing Rate"
    - "MFCC Coefficients"
    - "Spectral Centroid"

usage:
  start_session:
    - "Run: streamlit run app.py"
    - "Click Start Session"
    - "Allow camera and microphone access"
    - "Monitor emotions live"
  simulation_mode:
    - "Enable simulation mode if hardware unavailable"
    - "Generates realistic demo data"
  reports:
    - "Stop session"
    - "View analytics"
    - "Export CSV logs"
    - "Generate PDF reports"
    - "Review captured screenshots"

configuration:
  audio:
    sample_rate: 16000
    chunk_duration: 2.0
  video:
    width: 640
    height: 480
  thresholds:
    stress_threshold: 0.7
    alert_duration_seconds: 5
  fusion_weights:
    face: 0.6
    audio: 0.4

alerts:
  - "High stress sustained alert"
  - "Emotion heat indicator (green → red)"
  - "Real-time emotion timeline"
  - "Focus status badge"

fallback_mechanisms:
  - "Camera failure → simulated face emotions"
  - "Microphone failure → simulated audio stress"
  - "Library errors → default safe values"
  - "Complete demo mode without hardware"

license: "MIT"

author:
  name: "Danish"
  degree: "B.Tech Artificial Intelligence and Data Science"

team:
  name: "PRIMELOGIX"
  members:
    - name: "Danish M"
      role: "AI/ML Developer & Integration"
      contribution: "Core emotion pipeline, fusion logic, analytics, system integration"
    - name: "Chidarth H"
      role: "UI/UX & Dashboard Support"
      contribution: "Dashboard layout, UI flow, interaction design"
    - name: "Deepban T"
      role: "Research & Feature Design"
      contribution: "Problem research, use cases, feature planning"
    - name: "Jothik Rithin Bio J"
      role: "Testing & Validation"
      contribution: "Workflow testing, edge cases, demo stability"
    - name: "Deepak T A"
      role: "Documentation & Presentation"
      contribution: "README preparation, pitch structuring, submission formatting"

tagline: "Built for hackathons, designed for impact 🚀"
