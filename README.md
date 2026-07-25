# SendFlow

[Русский](README.ru.md)

Lightweight WhatsApp bulk messaging tool with a web UI. Add contacts, write messages, dispatch — all from one page.

## Prerequisites

You must be logged into [WhatsApp Web](https://web.whatsapp.com) in your default browser before using SendFlow. The app opens WhatsApp Web automatically on startup to give it time to load.

## Install

```bash
pip install -r requirements.txt
```

Python 3.12+ recommended.

## Run

```bash
python app.py
```

This opens two browser tabs:
1. `web.whatsapp.com` — log in by scanning the QR code if you haven't already
2. `localhost:5000` — SendFlow interface

## How it works

1. Add contacts (phone number + message)
2. Choose: send now or schedule for a specific time
3. Hit **Dispatch**
4. PyWhatKit opens a WhatsApp Web tab for each contact, pastes the message, and sends it
5. Status updates in real time: pending → sending → sent/failed

## Features

- Send to multiple contacts in sequence
- Schedule messages for a specific time (24h format)
- Instant send mode
- Stop/reset mid-dispatch
- Live status tracking with toast notifications
- Dark and light themes
- Russian and English interface

## Stack

- **Backend:** Flask
- **WhatsApp automation:** PyWhatKit
- **Frontend:** vanilla HTML/CSS/JS (no build step)

## Notes

- PyWhatKit uses your browser's WhatsApp Web session — no API keys needed
- Messages are sent sequentially with a short delay between each
- Phone numbers should include the country code (e.g. `+79991234567`)

