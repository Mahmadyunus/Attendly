# ScanClass (Attendly)

Face and voice powered attendance system, built with Streamlit and Supabase.

> **Status:** Work in progress. Core flows are in place, and some features are still being debugged (see [Known Issues](#known-issues)).

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Security](#security)
- [Known Issues](#known-issues)
- [Roadmap](#roadmap)
- [Author](#author)

## About

Taking attendance by roll call wastes class time and is easy to fake. **ScanClass** replaces it with AI: students register once with their face (and optionally their voice), and teachers mark a whole class present with a single scan. Every record is stored in Supabase so teachers and students can review attendance at any time.

## Features

### Students
- **Face login:** sign in with the camera, no password required
- **Instant registration:** unrecognized faces can create a new profile on the spot
- **Voice enrollment (optional):** enables voice-based attendance
- **Personal dashboard:** enrolled subjects with total classes and classes attended
- **Enroll or unenroll** from subjects, including joining through a shared join code

### Teachers
- **Secure accounts** with bcrypt-hashed passwords
- **Subject management:** create subjects (code, name, section) and share them with students
- **Take attendance** by scanning faces, with a voice attendance option
- **Attendance records** for every subject

## How It Works

1. A student registers; their face (and optional voice) is converted into an **embedding** and saved to Supabase.
2. A classifier is trained on the stored embeddings so it can recognize every registered student.
3. The teacher scans the class; faces are detected, matched against the classifier and the students found are marked present.
4. The results are written to the `attendance_logs` table and shown in the dashboards.

## Tech Stack

| Area | Tools |
| --- | --- |
| App framework | Python 3.11, Streamlit |
| Database | Supabase (PostgreSQL) |
| AI pipelines | Face recognition and voice embeddings |
| Utilities | bcrypt, httpx, Pillow, NumPy |

## Project Structure

```
Attendly/
├── app.py                  # Entry point and routing
├── requirements.txt
├── assets/                 # Static assets
└── src/
    ├── components/         # Header, footer, subject card, dialogs
    ├── database/           # Supabase client (config.py) and queries (db.py)
    ├── pipelines/          # face_pipeline.py, voice_pipeline.py
    ├── screens/            # Home, student and teacher screens
    └── ui/                 # Base layout and styling
```

## Database Schema

| Table | Purpose |
| --- | --- |
| `teachers` | Teacher accounts: username, hashed password, name |
| `students` | Student profiles with face and voice embeddings |
| `subjects` | Subjects created by teachers |
| `subject_students` | Links students to the subjects they are enrolled in |
| `attendance_logs` | One row per student per class, with timestamp and presence |

## Getting Started

### Prerequisites

- Python 3.11
- A [Supabase](https://supabase.com) project with the tables above
- A webcam (and a microphone for voice features)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Mahmadyunus/Attendly.git
cd Attendly

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Create the file `.streamlit/secrets.toml` in the project root:

```toml
SUPABASE_URL = "your-supabase-project-url"
SUPABASE_KEY = "your-supabase-secret-key"
```

### Run

```bash
streamlit run app.py
```

Open http://localhost:8501 and allow camera access when the browser asks.

## Usage

**As a teacher:** sign up or log in, create a subject, share its join code with students, then use **Take Attendance** to scan the class. Review results under **Attendance Records**.

**As a student:** look into the camera to sign in (or register if you are new), then join a subject with its code. Your dashboard shows how many classes you have attended.

## Security

- Secrets live only in `.streamlit/secrets.toml`, which is git-ignored. Never commit real keys.
- Teacher passwords are hashed with bcrypt before they are stored.
- Use a dedicated Supabase key for this project and rotate it if it is ever exposed.

## Known Issues

- Attendance may not be saved to `attendance_logs` after a scan, so Attendance Records can appear empty. Under investigation.
- The camera works in one browser tab at a time. Close extra tabs if the scanner shows a black screen.

## Roadmap

- [ ] Fix attendance saving after scan
- [ ] Improve voice-based attendance
- [ ] Export attendance records (CSV / Excel)
- [ ] Add automated tests and a LICENSE

## Author

Made by **Mahmad Yunus** ([@Mahmadyunus](https://github.com/Mahmadyunus))