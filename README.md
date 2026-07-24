# SendFlow

> WhatsApp bulk message dispatcher with scheduling and real-time status tracking.

## Features

- Send personalized messages to multiple contacts
- Schedule messages for a specific time or send instantly
- Live status tracking: pending → sending → sent/failed
- Stop/reset jobs mid-flight
- Auto-opens browser on startup
- Clean dark UI with toast notifications

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Opens at http://localhost:5000 automatically.

## Stack

- Flask (Python backend)
- PyWhatKit (WhatsApp automation)
- Vanilla JS + CSS (frontend)
