# Mukund — Personal Portfolio & Engineering System

A modern, responsive, cyber-minimalist personal portfolio and full-stack web application designed for **Mukund (Software Engineer & Tech Innovator)**.

---

## 🚀 Key Features

- **Personal Portrait Presentation**: High-resolution 3:4 portrait photo of Mukund (`assets/mukund-portrait-3x4.jpg` and `assets/mukund.jpeg`) centered with glowing cyber-ring and floating skill badges.
- **Full-Stack Flask Backend**: RESTful API endpoints for contact form delivery, live project likes, dynamic terminal commands, and system analytics.
- **SQLite Database Persistence**: Thread-safe storage in `data/portfolio.db` recording contact inquiries, likes, subscribers, and visitor traffic.
- **Interactive In-Browser CLI Terminal**: Emulates an interactive developer terminal with built-in commands (`help`, `about`, `skills`, `projects`, `stats`, `contact`, `hire`, `clear`).
- **Dynamic Projects & Like System**: Projects showcase with interactive categories and real-time like counts synchronized with the database.
- **Dark / Light Theme System**: High-contrast modern dark mode with smooth transition to light mode and persistent `localStorage` preference.
- **Email Dispatcher**: Delivers contact submissions directly to email via SMTP or opens a pre-formatted Gmail Compose Web link.
- **Isolated Directory**: Independent project in `c:\Users\Dilshaj-Ashrafi\Documents\webpage 3` running on port 5001 so both portfolios can run simultaneously.

---

## 📂 Project Directory Structure

```text
webpage 3/
├── assets/
│   ├── favicon.svg             # Custom SVG monogram favicon
│   ├── mukund.jpeg             # Original portrait image
│   ├── mukund-portrait-3x4.jpg # 3:4 aspect ratio portrait
│   ├── mukund-face-cropped.jpg # Square portrait crop
│   └── mukund-photo-base64.txt # Base64 encoded portrait
├── css/
│   └── style.css               # Modern glassmorphism & responsive styles
├── js/
│   └── main.js                 # Typewriter, canvas particles, terminal, API
├── data/
│   └── portfolio.db            # SQLite database
├── app.py                      # Flask backend API server (Port 5001)
├── database.py                 # SQLite database models & query layer
├── mailer.py                   # Email notification and Gmail compose
├── .env                        # Configuration (port, SMTP credentials)
├── start.bat                   # Double-click launcher for Windows
├── start.ps1                   # PowerShell startup script
├── index.html                  # Main portfolio single-page application
└── README.md                   # Documentation
```

---

## ⚡ How to Run

### Method 1: Double-Click Launcher
Double-click `start.bat` inside `c:\Users\Dilshaj-Ashrafi\Documents\webpage 3`.

### Method 2: PowerShell Terminal
```powershell
cd "c:\Users\Dilshaj-Ashrafi\Documents\webpage 3"
python app.py
```
Then open your browser at:
👉 **`http://localhost:5001`**

---

## 🛠️ REST API Endpoints

- `GET /api/health` — System status and server health
- `GET /api/stats` — Aggregated metrics (views, messages, likes)
- `POST /api/contact` — Submits contact form, stores in SQLite, dispatches email
- `GET /api/projects/likes` — Fetches project likes counts
- `POST /api/projects/like` — Increments project likes
- `POST /api/terminal` — Executes dynamic CLI commands via backend
