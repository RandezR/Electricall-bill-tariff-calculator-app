import threading
import time
import webview
from app import app


def run_server():
    app.run(port=5000, debug=False)


if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    time.sleep(1)  # give Flask a moment to start
    webview.create_window("Electricity Calculator", "http://127.0.0.1:5000")
    webview.start()