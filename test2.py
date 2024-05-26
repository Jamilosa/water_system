from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

# The selected date (for example)
selected_date = "2024/04/20"

# Authenticate to Firebase
cred = credentials.Certificate("database\\credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://waterlevelmonitoringsystem-db-default-rtdb.asia-southeast1.firebasedatabase.app"})

ref = db.reference('waterLevels')

# Fetch data from Firebase Realtime Database
water_levels = ref.get()

# Initialize the 2D array
records = []

# Iterate over the water_levels dictionary
for key, record in water_levels.items():
    # Get the timestamp from the record
    timestamp = record["timestamp"]
    # Parse the timestamp into a datetime object
    dt = datetime.strptime(timestamp, "%Y/%m/%d %H:%M:%S")
    # Format the date part of the datetime object in "YYYY/MM/DD" format
    date = dt.strftime("%Y/%m/%d")
    # Check if the date matches the selected date
    if date == selected_date:
        # Format the time part of the datetime object in "HH:MM:SS" format
        time = dt.strftime("%H:%M:%S")
        # Get the value from the record
        value = record["value"]
        # Append the time and value to the 2D array
        records.append([time, value])

# Now, 'records' is a 2D array containing the time and value of the records associated with the selected date
print(records)
