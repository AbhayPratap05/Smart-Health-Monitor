# Smart Health Monitor

Smart Health Monitor is a Django-based computer vision project that tries to make screen time a little healthier and a little more disciplined. The idea is simple: use a webcam to observe posture, blinking, focus, and movement patterns in real time, then save short session summaries so the user can look back at how they have been doing.

The project currently has three working modes:

- `Weekday Mode` watches posture during desk work. It tracks blink count, bad posture duration, drowsiness, head tilt, slouching, and whether the user is sitting too far from the screen.
- `Weekend Mode` is a yoga practice mode. It uses pose estimation to recognize a small set of yoga poses and asks the user to hold a detected pose steadily for a few seconds.
- `Exam Mode` is a basic proctoring-style mode. It checks whether the user is looking away from the screen, whether no face is visible, and whether multiple people appear in frame.

Session history is stored in SQLite and shown through the history pages inside the app.

## Tech Stack

- Django
- MediaPipe
- OpenCV
- NumPy
- pyttsx3
- SQLite

## What The Project Tracks

### Weekday Mode

- Blink count per session
- Total bad posture time
- Drowsiness based on prolonged eye closure
- Head tilt, slouching, shoulder tilt, and forward-head posture

### Weekend Mode

- Yoga session duration
- Pose recognition for:
	- T Pose
	- Virabhadrasana II
	- Vrikshasana
	- Adho Mukha Svanasana
	- Uttanasana
	- Utkatasana
	- Urdhva Hastasana

### Exam Mode

- Eyes-away time
- Multiple-person time
- Alert count during the session
- Violation percentage in session history

## Project Structure

```text
Smart Health Monitor/
├── README.md
├── mp_env/
└── smart_health/
		├── manage.py
		├── db.sqlite3
		├── face_landmarker.task
		├── requirements.txt
		├── monitor/
		│   ├── camera/
		│   ├── migrations/
		│   ├── templates/
		│   ├── models.py
		│   ├── urls.py
		│   └── views.py
		└── smart_health/
				├── settings.py
				├── urls.py
				└── wsgi.py
```

## Setup

This project already includes a virtual environment folder named `mp_env`, but you can also create your own if you prefer.

### 1. Move into the project

```bash
cd "/Users/abhaypratap/Smart Health Monitor"
```

### 2. Activate the virtual environment

```bash
source mp_env/bin/activate
```

### 3. Move into the Django app directory

```bash
cd smart_health
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## Important Notes

- A webcam is required for all three modes.
- On macOS, the terminal or Python process may need camera and microphone permissions depending on system settings.
- `Exam Mode` depends on the `face_landmarker.task` file being present inside the `smart_health/` directory, which is already the case in this repo.
- The app is configured for local development. `DEBUG` is enabled and `ALLOWED_HOSTS` is empty.

## Session Data

The application stores data in `smart_health/db.sqlite3`.

The main models are:

- `YogaSession`
- `WeekdaySession`
- `ExamSession`

These records are used to populate the combined history page and the mode-specific summaries.

## Available Routes

- `/` for the home page
- `/weekday/` for weekday posture monitoring
- `/weekend/` for yoga mode
- `/exam/` for exam monitoring
- `/history/` for combined session history

There are also backend endpoints for saving sessions and refreshing or selecting available cameras.

## Current Status

This is best described as a practical prototype with a real working pipeline rather than a production-ready health platform. The core experience is already there: camera stream, live analysis, voice or sound alerts, and session history. What it still needs, if it is going to grow further, is harder testing, a cleaner deployment story, and more defensive handling around camera access and platform-specific audio behavior.
