import os
import shutil
import sqlite3
import tempfile

# Get the Edge user profile path
edge_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default")
web_data_path = os.path.join(edge_path, "Web Data")

# Create a temporary copy of the file (Edge must be closed!)
temp_dir = tempfile.gettempdir()
temp_web_data = os.path.join(temp_dir, "Web_Data_Copy.db")
shutil.copy2(web_data_path, temp_web_data)

def extract_autofill_data(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch autofill values (simple name/value pairs)
        print("=== Autofill Entries ===")
        cursor.execute("SELECT name, value FROM autofill")
        for row in cursor.fetchall():
            print(f"Field: {row[0]}  →  Value: {row[1]}")

        print("\n=== Autofill Profiles (Structured Info) ===")
        cursor.execute("SELECT full_name, email_address, company_name, address_line_1, address_line_2, city, state, zipcode, country_code, phone_number FROM autofill_profiles")
        for row in cursor.fetchall():
            print(f"Name: {row[0]}, Email: {row[1]}, Phone: {row[9]}, Address: {row[3]} {row[4]}, {row[5]}, {row[6]} {row[7]}, {row[8]}")

        conn.close()
    except Exception as e:
        print("Error:", e)

# Run the extractor
extract_autofill_data(temp_web_data)
