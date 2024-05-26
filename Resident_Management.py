import firebase_admin
from firebase_admin import db, credentials
from tkinter import messagebox
from re import match


"""
UPDATE
24 05 18 : Implemented Firebase database on all functions (if required)






"""

global resident_list
resident_list = []

def update_residents():
    # Reference to the residents table
    ref = db.reference('residents')

    # Fetch data from Firebase Realtime Database
    residents = ref.get()

    if residents == None:
        return None

    resident_lis = []
    # Prepare the resident_list
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
        resident_lis.append(resident_entry)

    # Extract the id of the resident
    for resident in resident_lis:
        res_id = resident[0].split('_')[-1]
        resident[0] = res_id

    return resident_lis


def add_resident(first_name=None, middle_initial=None, last_name=None, house_number=None, street=None, phone_number=None):
    # Update residents
    global resident_list
    resident_list = update_residents()

    # Reference to the residents table
    ref = db.reference('residents')

    # New resident data
    new_resident = {
        'firstName': f'{first_name}',
        'middleInitial': f'{middle_initial}',
        'lastName': f'{last_name}',
        'houseNumber': f'{house_number}',
        'streetNumber': f'{street}',
        'phoneNumber': f'{phone_number}'
    }

    if resident_list == None:
        res_id_counter = 1
        new_resident_id = f"resident_id_{res_id_counter}"
        res_id_counter += 1
    else:
        res_id_counter = int(resident_list[-1][0])
        new_resident_id = f"resident_id_{res_id_counter + 1}"

    # Add the new resident to the database
    ref.child(new_resident_id).set(new_resident)    

    return messagebox.askyesno("Add Another Resident?", "Do you want to add another resident?")
    
def search_resident(keyword1):
    """ Query database and store data on a list """
    global resident_list
    resident_list = update_residents()
    
    records = resident_list

    results = []
    for record in records:
        for item in record:
            if (str(item).lower() == keyword1.lower()):
                results.append(record)

    return results
            
def delete_resident(id):
    # Reference to the specific resident
    id = "resident_id_" + str(id)
    resident_ref = db.reference(f'residents/{id}')
    
    # Fetch resident data to show in the confirmation message
    resident = resident_ref.get()
    
    if not resident:
        messagebox.showinfo("Delete Cancelled", "Resident not found in the database.")
        return False
    
    # Ask for confirmation
    wanna_delete = messagebox.askyesno("Delete Resident", f"Are you sure you want to delete {resident['firstName']} {resident['lastName']} ({resident['streetNumber']})?")
    
    if wanna_delete:
        # Delete the resident from the database
        resident_ref.delete()
        messagebox.showinfo("Delete Successful", f"{resident['firstName']} {resident['lastName']} ({resident['streetNumber']}) was deleted permanently.")
        return True
    else:
        messagebox.showinfo("Delete Cancelled", f"{resident['firstName']} {resident['lastName']} ({resident['streetNumber']}) was not deleted.")
        return False

def get_residents():
    resident_list = update_residents()
    return resident_list 


def resident_phone_available(phone): # Used in Validation
    resident_list = get_residents()  

    if resident_list == None:
        return True
    
    for resident in resident_list:
        for element in resident:
            if str(element) == str(phone):
                return False
    
    return True
 
if __name__ == '__main__':

    # authenticate to firebase
    cred = credentials.Certificate("database\\credentials.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://waterlevelmonitoringsystem-db-default-rtdb.asia-southeast1.firebasedatabase.app"})


    resident_list = update_residents()

    #print(search_resident("John"))

    #add_resident(first_name="TEST2", middle_initial="X", last_name="FROM PYTHON", house_number="125", street="Purok 69", phone_number="09234356789")

    #delete_resident(3)
    
    print("Current Module: Resident_Management.py")

