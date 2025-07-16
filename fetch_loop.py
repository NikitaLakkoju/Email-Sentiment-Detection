import time
import subprocess

while True:
    print("🔁 Checking for new emails...")
    subprocess.run(["python3", "process_email.py"])
    time.sleep(180)  # 180 seconds = 3 minutes
