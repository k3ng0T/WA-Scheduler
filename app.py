from flask import Flask, request, jsonify, send_from_directory
import threading
import pywhatkit
import time
from datetime import datetime
import os

app = Flask(__name__)

# Global job state
jobs = {}       # id -> { phone, message, status, error }
job_lock = threading.Lock()


def send_messages(contacts, send_time_str, send_now):
    """Run in background thread. Waits for time then sends each message."""

    # Wait until scheduled time
    if not send_now:
        while True:
            if datetime.now().strftime("%H:%M") == send_time_str:
                break
            time.sleep(10)

    for c in contacts:
        cid = c["id"]
        with job_lock:
            jobs[cid]["status"] = "sending"

        try:
            pywhatkit.sendwhatmsg_instantly(
                c["phone"],
                c["message"],
                wait_time=10,
                tab_close=True,
            )
            with job_lock:
                jobs[cid]["status"] = "sent"
        except Exception as e:
            with job_lock:
                jobs[cid]["status"] = "failed"
                jobs[cid]["error"] = str(e)

        time.sleep(5)   # small gap between messages


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/dispatch", methods=["POST"])
def dispatch():
    data = request.json
    contacts = data.get("contacts", [])
    send_now = data.get("sendNow", False)
    send_time = data.get("time", "")

    if not contacts:
        return jsonify({"error": "No contacts"}), 400

    with job_lock:
        jobs.clear()
        for c in contacts:
            jobs[c["id"]] = {
                "id": c["id"],
                "phone": c["phone"],
                "message": c["message"],
                "status": "pending",
                "error": None,
            }

    t = threading.Thread(
        target=send_messages,
        args=(contacts, send_time, send_now),
        daemon=True,
    )
    t.start()

    return jsonify({"ok": True, "total": len(contacts)})


@app.route("/status")
def status():
    with job_lock:
        return jsonify(list(jobs.values()))


@app.route("/reset", methods=["POST"])
def reset():
    with job_lock:
        jobs.clear()
    return jsonify({"ok": True})


if __name__ == "__main__":
    print("\n  WA Scheduler running → http://localhost:5000\n")
    app.run(debug=False, port=5000)
