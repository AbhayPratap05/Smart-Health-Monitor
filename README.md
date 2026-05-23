# Smart Health Monitor

Smart Health Monitor (Unified Digital Wellness System) is a Django-based computer vision wellness app for healthier screen time and guided movement practice. It combines real-time webcam analysis with session tracking, a statistics dashboard, and a local AI assistant.

The current project focuses on two core experiences:

- `Weekday Mode` for desk-work wellness monitoring
- `Weekend Mode` for yoga pose practice and hold tracking

It also includes:

- a `Dashboard` for health insights and session summaries
- a `Chatbot` powered by local Ollama models for wellness and session-related questions
- a `History` page for previously saved weekday and yoga sessions

## Access Draft Research Report

https://docs.google.com/document/d/1_6lzPwtapeNzdi1CD5ztknLiEPz-RSHF/edit?usp=sharing&ouid=103688610499996797996&rtpof=true&sd=true

## Features

### Weekday Mode

- Real-time posture monitoring using face and pose landmarks
- Blink tracking per session
- Bad posture duration tracking
- Detection of:
  - slouching
  - forward head posture
  - shoulder tilt
  - head tilt
  - poor screen distance
- Voice feedback for posture and drowsiness alerts

### Weekend Mode

- Real-time yoga pose detection
- Pose stability check before confirmation
- Hold timer for detected poses
- Guided practice for:
  - T Pose
  - Virabhadrasana II
  - Vrikshasana
  - Adho Mukha Svanasana
  - Uttanasana
  - Utkatasana
  - Urdhva Hastasana

### Dashboard

- Total session count
- Total monitored hours
- Weekly activity summary
- Average session duration
- Blink and posture statistics
- Auto-generated health insights based on saved session data

### AI Health Assistant

- Local chatbot integration using Ollama
- Answers questions about:
  - posture and screen habits
  - blink rate and eye strain
  - yoga poses and benefits
  - session statistics and trends
- Uses Chroma as a local vector store for health-monitoring context

## Tech Stack

- Django 5.2
- OpenCV
- MediaPipe
- NumPy
- pyttsx3
- Pillow
- SQLite
- LangChain
- Ollama
- Chroma

## Project Structure

```text
Smart Health Monitor/
├── README.md
├── .gitignore
├── smart_health/
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── face_landmarker.task
│   ├── health_monitor_db/          # generated locally by the chatbot/vector store
│   ├── monitor/
│   │   ├── camera/
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── models.py
│   │   ├── rag_chatbot.py
│   │   ├── urls.py
│   │   └── views.py
│   └── smart_health/
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
```

## Requirements

Before running the project, make sure you have:

- Python 3.10.x
- A working webcam
- `pip`
- Ollama installed locally

For Ollama installation, see: https://ollama.com/download

## Setup

The most reliable setup for this project is to create a fresh virtual environment with Python 3.10. MediaPipe is the strict dependency here: using a newer Python version can easily cause install failures or incompatible wheels.

## macOS Setup

These steps are recommended for macOS. They are especially important on a new Mac where the default `python3` may be too new for MediaPipe.

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Smart-Health-Monitor
```

### 2. Install Python 3.10

Using Homebrew:

```bash
brew install python@3.10
```

Confirm the version:

```bash
$(brew --prefix python@3.10)/bin/python3.10 --version
```

Expected output should be Python 3.10.x. The tested environment used Python 3.10.19.

### 3. Create and activate a virtual environment

From the repository root:

```bash
$(brew --prefix python@3.10)/bin/python3.10 -m venv .venv
source .venv/bin/activate
```

Confirm the active Python:

```bash
python --version
which python
```

### 4. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r smart_health/requirements.txt
```

The pinned versions are based on the working Mac environment:

- Django 5.2.9
- MediaPipe 0.10.21
- NumPy 1.26.4
- OpenCV contrib 4.8.0.76
- pyttsx3 2.99

### 5. Start Ollama and pull the required models

Run Ollama in one terminal:

```bash
ollama serve
```

Then pull the models used by the chatbot:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Verify that Ollama can be reached and that both models are installed:

```bash
ollama list
```

Notes:

- `llama3.2` is used for chatbot responses
- `nomic-embed-text` is used for embeddings in the Chroma vector store
- Django imports the chatbot during startup, so `manage.py migrate`, `manage.py check`, and `manage.py runserver` can fail if Ollama is not running or if these models are missing.
- If `ollama list` fails, fix Ollama first before running any Django command.

### 6. Move into the Django project directory

```bash
cd smart_health
```

### 7. Apply migrations

```bash
python manage.py migrate
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open the app at:

```text
http://127.0.0.1:8000/
```

When the browser asks for camera access, allow it. On macOS you may also need to allow camera and microphone access for Terminal, Python, or your IDE in System Settings.

## Windows Setup

Windows has not been fully tested for this project yet, so treat these as expected setup steps rather than a guaranteed supported path.

### 1. Install Python 3.10

Install 64-bit Python 3.10 from https://www.python.org/downloads/release/python-310/.

During installation, enable:

- `Add python.exe to PATH`
- `pip`

Confirm the version in PowerShell:

```powershell
python --version
```

### 2. Clone the repository

```powershell
git clone <your-repo-url>
cd Smart-Health-Monitor
```

### 3. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r smart_health\requirements.txt
```

### 5. Start Ollama and run Django

Install Ollama for Windows from https://ollama.com/download, then run:

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
ollama list
cd smart_health
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Windows note: OpenCV, MediaPipe, webcam permissions, and `pyttsx3` voice output can behave differently on Windows. If installation fails, first confirm that Python is 3.10 64-bit and that the virtual environment is active.

## Using the App

### Home

The home page introduces the project and includes the built-in AI assistant.

### Weekday Mode

Use Weekday Mode when working at your desk. The webcam stream is analyzed in real time to monitor posture and blink behavior. At the end of the session, the app saves:

- session duration
- blink count
- bad posture time

### Weekend Mode

Use Weekend Mode for yoga practice. The app detects supported poses, waits for a stable pose lock, then tracks the hold duration before saving the session.

### Dashboard

The dashboard summarizes your saved sessions and generates health-oriented feedback based on your data.

### History

The history page shows previously saved:

- weekday monitoring sessions
- yoga sessions

## Available Routes

- `/` - home page
- `/dashboard/` - health dashboard
- `/weekday/` - weekday posture monitoring
- `/weekend/` - yoga mode
- `/history/` - session history
- `/video_feed/?mode=weekday` - weekday camera stream
- `/video_feed/?mode=weekend` - weekend camera stream
- `/api/chatbot/` - chatbot API endpoint

## Data Storage

The project currently stores local data in:

- `smart_health/db.sqlite3` for Django session data
- `smart_health/health_monitor_db/` for the Chroma vector store used by the chatbot

Main active session models:

- `WeekdaySession`
- `YogaSession`

## Important Notes

- A webcam is required for Weekday Mode and Weekend Mode.
- The chatbot depends on Ollama being installed and running locally.
- On first use, the chatbot may create the `health_monitor_db/` directory automatically.
- If the chatbot is not working, confirm that both models are available:
  - `llama3.2`
  - `nomic-embed-text`
- On macOS, you may need to grant camera and microphone permissions to Terminal, Python, or your IDE.
- `pyttsx3` voice alerts may behave differently across operating systems.

## Known Limitations

- This is a local development project, not a production-ready health platform.
- Camera handling is designed for one active mode at a time.
- The chatbot is limited to Smart Health Monitor and wellness-related questions.
- Some legacy exam-related files may still exist in the codebase, but the current active app flow centers on dashboard, weekday, weekend, history, and chatbot features.

## Current Status

This version is best described as a more polished second iteration of the project. Compared with the earlier build, it now presents a clearer wellness-first experience with:

- a redesigned home flow
- a new dashboard
- a local AI assistant
- improved camera/session handling
- updated weekday and weekend mode experience

## Future Improvements

- stronger automated test coverage
- cleaner production deployment setup
- richer charts and trend visualizations
- more health recommendations and personalized coaching
- deeper yoga guidance and pose analytics
