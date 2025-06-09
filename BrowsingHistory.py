import os
import shutil
import sqlite3
import tempfile

# Copy history DB safely
edge_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default")
history_path = os.path.join(edge_path, "History")
temp_history = os.path.join(tempfile.gettempdir(), "edge_history_copy.db")
shutil.copy2(history_path, temp_history)

def extract_history(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 20")

    print("=== Browsing History (Recent 20) ===")
    for row in cursor.fetchall():
        print(f"URL: {row[0]}\nTitle: {row[1]}\n")

    conn.close()

extract_history(temp_history)
