# AI Real-time Gym Coach

A real-time workout companion that watches you through your webcam, counts reps, checks your form, and coaches you out loud — built with Streamlit, MediaPipe pose estimation, and an LLM-powered voice coach.

**[Live demo landing page](https://github.com/Ridanshi/real-time-ai-gym)** — Streamlit app runs locally (see setup below).

---

## What it does

1. **Login** with a username (no password — single-user local tool, see [Notes](#notes-and-limitations)).
2. **Plan your workout** — pick an exercise, number of sets, and reps per set.
3. **Start the camera** — your browser streams live video to the backend over WebRTC.
4. **Pose tracking** — a pretrained MediaPipe model extracts 33 body landmarks per frame and draws a skeleton overlay.
5. **Rep counting & form checking** — per-exercise angle math (hip/knee/elbow/back angles) drives a rep-counting state machine and flags common form mistakes.
6. **Voice coaching** — when a set completes, the workout ends, or a form issue is detected, an LLM (Groq `llama-3.3-70b-versatile`) generates a short spoken coaching line, converted to audio via gTTS and autoplayed.
7. **History** — completed sets and partial progress are saved to a local SQLite database and shown in a workout history table.

## Supported exercises

- Squats
- Push-ups
- Biceps Curls (Dumbbell)
- Shoulder Press
- Lunges

## Tech stack

| Layer | Tool |
|---|---|
| UI / app framework | Streamlit |
| Live camera streaming | streamlit-webrtc (WebRTC) |
| Pose estimation | MediaPipe PoseLandmarker (pretrained) |
| Image processing | OpenCV |
| Rep counting / form logic | Custom rule-based angle-threshold detectors (Python) |
| Coaching language generation | Groq API (Llama 3.3 70B) |
| Text-to-speech | gTTS |
| Database | SQLite |
| Landing page | Static HTML/CSS |

## Architecture

```
Camera → WebRTC → VideoProcessor
   → MediaPipe (33 landmarks) → skeleton overlay
   → Exercise detector (angle math + rep state machine)
      ↓
   Metrics synced to session state (~4x/sec)
      → SQLite write (on set/workout completion)
      → Rule-based form-issue detection
         → LLM generates coaching text
         → gTTS → audio autoplay
```

The vision model (MediaPipe) and the language model (Groq LLM) never share data directly — MediaPipe outputs joint coordinates, which drive deterministic angle-based logic, which produces a short text description that's the *only* thing sent to the LLM. No frames, images, or raw coordinates ever reach the LLM.

## Project structure

```
app/
├── main.py                          # Streamlit entrypoint / page layout
├── core/base_exercise.py            # Shared exercise detector base class
├── detectors/                       # Per-exercise rep-counting + form logic
│   ├── squat.py
│   ├── pushup.py
│   ├── biceps_curl.py
│   ├── shoulder_press.py
│   └── lunges.py
├── services/
│   ├── auth/login_wall.py           # Username-based session gate
│   ├── config/workout_config.py     # Exercise list, metric fields, coach prompt
│   ├── vision/exercise_video_processor.py  # WebRTC frame → MediaPipe → detector
│   ├── tracking/metrics.py          # Session state sync + DB write triggers
│   ├── coaching/                    # LLM + TTS + voice event pipeline
│   ├── persistence/exercise_repository.py  # SQLite access layer
│   ├── state/session_defaults.py
│   └── ui/style_loader.py           # Custom CSS / font injection
├── ml_models/pose_landmarker_full.task  # Pretrained MediaPipe pose model
└── static/style.css

LandingPage/
├── index.html                       # Marketing/landing page
├── style.css
└── IMGs/, videos/                   # Landing page media
```

## Setup

Requires Python 3.10 or 3.11 (MediaPipe does not yet ship 3.13 wheels).

```bash
cd app

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

# Set your Groq API key (get one free at https://console.groq.com/keys)
set GROQ_API_KEY=your_key_here        # Windows (cmd)
# $env:GROQ_API_KEY="your_key_here"   # Windows (PowerShell)
# export GROQ_API_KEY=your_key_here   # macOS/Linux

streamlit run main.py
```

Open `http://localhost:8501`, allow camera access, and start a workout.
