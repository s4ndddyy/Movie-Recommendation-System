import os
import sys
import subprocess

app_path = "app.py"
subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])

#Just run this file to start the app in the browser.