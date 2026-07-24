from flask import Flask, request, jsonify, send_from_directory
import threading
import pywhatkit
import time
from datetime import datetime
import os
import webbrowser

app = Flask(__name__)

jobs = {}
job_lock = threading.Lock()
stop_event = threading.Event()


def send_messages(contacts, send_time_str, send_now):
    if not send_now:
        while not stop_event.is_set():
            if datetime.now().strftime("%H:%M") == send_time_str:
                break
            time.sleep(1)

    for c in contacts:
        if stop_event.is_set():
            break

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

        time.sleep(3)

    with job_lock:
        for jid in jobs:
            if jobs[jid]["status"] == "sending":
                jobs[jid]["status"] = "failed"
                jobs[jid]["error"] = "Stopped by user"


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
        return jsonify({"error": "No contacts provided"}), 400

    stop_event.clear()

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
    stop_event.set()
    with job_lock:
        jobs.clear()
    return jsonify({"ok": True})


@app.route("/stop", methods=["POST"])
def stop():
    stop_event.set()
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = 5000
    url = f"http://localhost:{port}"
    print(f"\n  SendFlow running -> {url}\n")

    def open_browser():
        time.sleep(1)
        webbrowser.open("https://web.whatsapp.com")
        time.sleep(1)
        webbrowser.open(url)

    threading.Timer(0, open_browser).start()
    app.run(debug=False, port=port)
