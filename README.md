# EMOTISENSE AI 🧠

**Multimodal Emotion Recognition using Audio + Face**

A real-time emotion monitoring system that combines facial emotion detection and audio stress analysis to provide comprehensive emotional insights.

---

## 🚀 Quick Start

Run the application in **1 command**:

```bash
# Install dependencies and run
pip install -r requirements.txt && streamlit run app.py
The application will open in your browser at http://localhost:8501

📁 Project Structure
bash
Copy code
EMOTISENSE-AI/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                      # This file
├── src/
│   ├── config.py                  # Configuration settings
│   ├── utils.py                   # Utility functions
│   ├── webcam/
│   │   ├── camera.py              # Camera capture
│   │   └── face_emotion.py        # Face emotion detection
│   ├── audio/
│   │   ├── mic_capture.py         # Microphone capture
│   │   └── audio_emotion.py       # Audio stress analysis
│   ├── fusion/
│   │   └── fusion_engine.py       # Multimodal fusion logic
│   ├── dashboard/
│   │   ├── ui_components.py       # UI components
│   │   └── plots.py               # Visualization charts
│   ├── logger/
│   │   ├── session_logger.py      # Session logging
│   │   └── report_generator.py    # PDF report generation
│   ├── fallback/
│   │   └── rule_based.py          # Simulation / fallback mode
│   └── analytics/
│       ├── session_insights.py    # Session intelligence & metrics
│       └── feedback_engine.py     # Rule-based feedback generation
├── outputs/
│   ├── session_logs/              # Session CSV files
│   ├── reports/                   # Generated PDF reports
│   └── snapshots/                 # Auto-captured screenshots
🎯 Features
Core Functionality
Real-time Face Emotion Detection (happy, sad, angry, fear, surprise, neutral)

Audio Stress Analysis from microphone input

Multimodal Fusion Engine combining face and audio signals

Live Dashboard with real-time metrics and alerts

Session Logging with CSV export

PDF Report Generation with insights and recommendations

🆕 Advanced Intelligence Features
Automatic Screenshot Capture on:

Extreme stress peaks

Extreme happiness moments

Continuous distraction

Emotion Timeline Analysis

Top Critical Moments Detection

Emotion Stability Score

Recovery Speed Measurement after stress spikes

Session Quality Score (0–100)

Attention Span Estimation

Session Risk Indicator (Low / Medium / High)

Dashboard Tabs
Live Dashboard – Real-time video feed, emotion metrics, stress gauge, alerts

Session Report – Analytics, insights, and export options

Screenshot Gallery – Captured moments with timestamps & reasons

About – Project overview and technology stack

Fallback & Safety Features
Simulation Mode (works without camera/microphone)

Hardware Failure Handling

Manual “Mark Important Moment” Button

Privacy-first Local Execution

Graceful Error Handling

🛠️ Technology Stack
Frontend: Streamlit

Computer Vision: OpenCV, FER

Audio Processing: sounddevice, librosa

Data Analysis: pandas, numpy

Visualization: plotly

Reports: reportlab

Backup Detection: DeepFace (fallback)

📊 Metrics Provided
Primary Metrics
Stress Level (0–1)

Engagement (0–1)

Confidence (0–1)

Confusion (0–1)

Emotional States
Stressed, Engaged, Calm, Positive, Negative, Neutral

Audio Features
RMS Energy

Zero Crossing Rate

MFCC Coefficients

Spectral Centroid

🎮 Usage Instructions
Starting a Session
Run streamlit run app.py

Click Start Session

Allow camera and microphone permissions

Monitor emotions live on dashboard

Simulation Mode
Enable Simulation Mode if hardware is unavailable

Generates realistic emotion patterns

Ideal for demos and testing

Reports & Evidence
Stop session → View analytics

Export CSV logs

Generate PDF reports

Review auto-captured screenshots

🔧 Configuration
Key settings in src/config.py:

python
Copy code
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHUNK_DURATION = 2.0

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

STRESS_THRESHOLD = 0.7
ALERT_DURATION = 5

FACE_WEIGHT = 0.6
AUDIO_WEIGHT = 0.4
🚨 Alerts & Monitoring
High Stress Alert (sustained)

Emotion Heat Indicator (Green → Red)

Real-time Emotion Timeline

Focus Status Badge

🔄 Fallback Mechanisms
Camera failure → simulated face emotions

Microphone failure → simulated audio stress

Library issues → default safe values

Full demo mode without hardware

📝 License
MIT License

👨‍💻 Author
Danish — B.Tech Artificial Intelligence and Data Science

Hackathon Project: SRM IST × NOOBTRON — NOOB HACKFEST

👥 Team Members — PRIMELOGIX
Danish M — AI/ML Developer & Integration
Implemented the emotion pipeline, fusion logic, analytics engine, and system integration.

Chidarth H — UI/UX & Dashboard Support
Contributed to dashboard design, layout structure, and user interaction flow.

Deepban T — Research & Feature Design
Conducted problem research, use-case analysis, and feature ideation.

Jothik Rithin Bio J — Testing & Validation
Tested system workflows, edge cases, and improved demo reliability.

Deepak T A — Documentation & Presentation
Supported README preparation, pitch structuring, and submission formatting.

Built for hackathons, designed for impact. 🚀
