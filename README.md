
# AI Face Authentication Attendance System

## Project Description

This project is a **web-based face authentication attendance system** built using **Flask and MediaPipe**.
It allows users to register their face and mark attendance using **real-time webcam input** with basic **liveness detection (eye blink)**.

The system ensures that only **registered users** can mark attendance and enforces proper **punch-in / punch-out rules**.

---

## Features

* Face registration using webcam
* Face recognition for attendance
* Punch-in and punch-out support
* Eye-blink based liveness detection
* Blocks unregistered users
* Prevents punch-out without punch-in
* Automatic working duration calculation
* Attendance stored in structured CSV format
* Simple and clean web interface

---

## Tech Stack

* Backend: Flask (Python)
* Face Detection: MediaPipe Face Mesh
* Computer Vision: OpenCV
* Liveness Detection: Eye Blink
* Storage: CSV File
* Frontend: HTML, CSS

---

## Folder Structure

```
face_attendance_flask/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── faces/
│   └── attendance.csv
│
├── models/
│   ├── face_embedder.py
│   └── liveness.py
│
├── utils/
│   └── attendance.py
│
├── templates/
│   ├── index.html
│   ├── register.html
│   └── attendance.html
│
└── static/
    └── css/
        └── style.css
```

---

## How to Run

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Run the application:

```bash
python app.py
```

3. Open browser:
## Attendance Rules

* User must register before marking attendance
* Punch-out is allowed only after punch-in
* Eye blink is required to verify liveness
* Invalid attempts are blocked with proper messages

---

## Attendance CSV Format

```csv
Employee ID,Employee Name,Date,Day,Punch In,Punch Out,Working Duration,Attendance Status
```

---

## Known Limitations

* Accuracy may reduce in poor lighting
* Does not fully prevent advanced spoofing attacks
* Designed for small-scale use

---

## Future Improvements

* Database integration
* Admin dashboard
* Attendance analytics
* Advanced liveness detection

---

## Author

**Anand Golla**
