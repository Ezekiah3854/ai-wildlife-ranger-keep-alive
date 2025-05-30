"""Flask-based keep alive worker for the AI Wildlife Ranger server on Render."""
import time
import os
from datetime import datetime
from multiprocessing import Process
from dotenv import load_dotenv
from flask import Flask, jsonify
import requests

load_dotenv('.env')
# Flask app setup
app = Flask(__name__)


# endpoint to ai wildlife ranger
PING_ARTS_EXPERIENCE_TATTOO = os.getenv('PING_ARTS_EXPERIENCE_TATTOO')

LOG_FILE = "keep_alive_log.txt"

def log_message(message):
    """Log a message with a timestamp to a file."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")
        log_file.flush()  # Ensure logs are written immediately
    print(f"[{timestamp}] {message}")  # Print to console for debugging

def ping_servers():
    """Send a request to each app server to keep them alive."""
    while True:
        try:
            res_arts_experience_tattoo = requests.get(PING_ARTS_EXPERIENCE_TATTOO, timeout=10)
            if res_arts_experience_tattoo.status_code == 200:
                message_arts = f"Ping to arts-experience-tattoo was successful. Response: {res_arts_experience_tattoo.json().get('message')}"
                print(message_arts)
                log_message(message_arts)

            else:
                message_arts = f"Either the app server is restarting or is busy: {res_arts_experience_tattoo.status_code}"
                print(message_arts)
                log_message(message_arts)

        except requests.RequestException as e:
            message = f"Failed to reach app.py. Network Issue: {e}"
            log_message(message)
        finally:
            # Wait for 10 minutes before sending the next request
            time.sleep(600)

@app.route('/ping', methods=['GET'])
def handle_ping():
    """Handle incoming ping requests"""
    log_message("Received ping from arts-experience-tattoo: Active")
    return jsonify({"message": "Keep Alive Worker is active"}), 200


if __name__ == "__main__":
    # Start the ping app servers function as a separate process
    ping_process = Process(target=ping_servers)
    ping_process.start()
    
    # Start the Flask app
    app.run(debug=False, port=5001)
