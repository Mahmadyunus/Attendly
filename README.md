# Attendly (ScanClass)

AI-powered attendance system built with Streamlit. Students log in with their face, teachers take attendance by scanning the class, and everything is stored in Supabase.

> **Status:** Work in progress. Some features are still being built and debugged.

## Features

- **Face login for students** using the camera, with automatic new-profile registration if the face is not recognized
- **Optional voice enrollment** for voice-based attendance
- **Student dashboard** showing enrolled subjects, total classes and classes attended
- **Enroll / unenroll** from subjects
- **Teacher dashboard** with Take Attendance, Manage Subjects and Attendance Records
- **Secure teacher accounts** with bcrypt-hashed passwords

## Tech Stack

- Python, Streamlit
- Supabase (PostgreSQL)
- Face recognition and voice embedding pipelines
- bcrypt, httpx, Pillow, NumPy

## Project Structure

```
app.py
src/
  components/   # header, footer, subject card, dialogs
  database/     # Supabase config and queries
  pipelines/    # face and voice pipelines
  screens/      # student and teacher screens
  ui/           # base layout and styling
```

## Database Tables

`teachers`, `students`, `subjects`, `subject_students`, `attendance_logs`

## Setup

1. Clone the repo:

   ```
   git clone https://github.com/<your-username>/Attendly.git
   cd Attendly
   ```

2. (Recommended) Create a virtual environment and install the dependencies your project uses (Streamlit, supabase, bcrypt, httpx, Pillow, NumPy, plus the face/voice libraries):

   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -U streamlit supabase bcrypt httpx pillow numpy
   ```

3. Create `.streamlit/secrets.toml` in the project root:

   ```toml
   SUPABASE_URL = "your-supabase-project-url"
   SUPABASE_KEY = "your-supabase-secret-key"
   ```

   This file is git-ignored. Never commit your keys.

4. Run the app:

   ```
   streamlit run app.py
   ```

## Known Issues

- Attendance records may not appear if attendance is not saved to `attendance_logs` after scanning (being fixed).

## Roadmap

- Fix attendance saving after face scan
- Improve voice-based attendance
- Add export of attendance records
- Add `requirements.txt`

## Author

Created by Yunus