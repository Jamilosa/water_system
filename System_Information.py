import firebase_admin
from firebase_admin import db, credentials


from tkinter import messagebox

global sms_template, warning_levels
warning_levels = []
sms_template = []


def retrieve_sms_template():
    global sms_template

    # Reference to the smsTemplates node in the database
    ref = db.reference('smsTemplates')

    # Fetch data from Firebase Realtime Database
    templates = ref.get()

    # List of statuses in the order you want
    statuses = ["LOW", "NORMAL", "HIGH", "CRITICAL"]

    # Initialize the sms_template list
    sms_template = []

    # Process each status in the order specified
    for status in statuses:
        # Get the message for the current status
        message = templates[status.lower()]
        # Create a template entry and append it to the sms_template list
        template_entry = [status, message]
        sms_template.append(template_entry)

    return sms_template


def retrieve_warning_levels():
    global warning_levels
    # Reference to the warningLevels node in the database
    ref = db.reference('warningLevels')

    # Fetch data from Firebase Realtime Database
    levels = ref.get()

    # List to store warning levels
    warning_levels = []

    # List of statuses in the order you want
    statuses = ["LOW", "NORMAL", "HIGH", "CRITICAL"]

    # Process each status in the order specified
    for status in statuses:
        # Get the message for the current status
        message = levels[status.lower()]
        # Create a template entry and append it to the warning_levels list
        template_entry = [status, message]
        warning_levels.append(template_entry)
    
    return warning_levels


    
def get_sms_templates():
    global sms_template
    sms_template = retrieve_sms_template()

    ''' Get SMS Template on the database '''
    return sms_template

def get_warning_levels():
    global warning_levels
    warning_levels = retrieve_warning_levels()

    ''' Get warning levels on the database '''    
    return warning_levels


def update_sms_template(low=None, normal=None, high=None, critical=None):
    sms_reference = db.reference('smsTemplates')

    try:
        sms_reference.update({'low': f'{low}'})
        sms_reference.update({'normal': f'{normal}'})
        sms_reference.update({'high': f'{high}'})
        sms_reference.update({'critical': f'{critical}'})

        messagebox.showinfo("Changes Saved", "SMS template was updated successfully.")
    
    except:
        messagebox.showinfo("Changes Not Saved.", "An error occured. SMS template was not saved.")


def update_warning_levels(low=None, normal=None, high=None, critical=None):
    warning_reference = db.reference('warningLevels')
    try:
        warning_reference.update({'low': f'{low}'})
        warning_reference.update({'normal': f'{normal}'})
        warning_reference.update({'high': f'{high}'})
        warning_reference.update({'critical': f'{critical}'})

        messagebox.showinfo("Changes Saved.", "Warning levels was updated successfully.")

    except:
        messagebox.showinfo("Changes Not Saved.", "An error occured. Warning level was not saved.")


if __name__ == '__main__':
    # authenticate to firebase
    cred = credentials.Certificate("database\\credentials.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://waterlevelmonitoringsystem-db-default-rtdb.asia-southeast1.firebasedatabase.app"})

    #retrieve_sms_template()
    #print(sms_template)
    
    #retrieve_warning_levels()
    #print(warning_levels)

    #print(f"OLD SMS: {get_sms_templates()}")
    #update_sms_template(low="NEW LOWx", normal="NEW NORMALx", high="NEW HIGHx", critical="NEW CRITICALx")
    #print(f"NEW SMS: {get_sms_templates()}")
    

    #print(f"OLD LVL: {get_warning_levels()}")
    #update_warning_levels(low="69.69", normal="69.69", high="69.69", critical="69.69")
    #print(f"NEW LVL: {get_warning_levels()}")


    update_warning_levels(low='low', normal='nor', high='gih', critical='crit')
    
    