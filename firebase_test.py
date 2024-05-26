# import required modules
import firebase_admin
from firebase_admin import db, credentials

# authenticate to firebase
cred = credentials.Certificate("database\\credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://waterlevelmonitoringsystem-db-default-rtdb.asia-southeast1.firebasedatabase.app"})

# Reference to the residents table
ref = db.reference('residents')

# Fetch data from Firebase Realtime Database
residents = ref.get()

# Prepare the resident_list
resident_list = []
for resident_id, resident_data in residents.items():
    resident_entry = [
        resident_id,
        resident_data.get('firstName', ''),
        resident_data.get('middleInitial', ''),
        resident_data.get('lastName', ''),
        resident_data.get('houseNumber', ''),
        resident_data.get('streetNumber', ''),
        resident_data.get('phoneNumber', '')
    ]
    resident_list.append(resident_entry)

# Print the resident_list
for resident in resident_list:
    print(resident)