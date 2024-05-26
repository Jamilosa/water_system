import firebase_admin
from firebase_admin import db, credentials
from tkinter import messagebox
import hashlib

global accounts_list, user_id
user_id = 0
accounts_list = [] #

    
def update_accounts(): ## Returns update database
    """
    If account exists, returns:
        [id, fname, initial, lname, phone, email, password]
    Else returns:
        [] 
    """
    accounts_lis = []

    # Reference to the accounts table
    ref = db.reference('accounts')

    # Fetch data from Firebase Realtime Database
    accounts = ref.get()

    if accounts is None:
        accounts_lis = []
        return accounts_lis

    user_id = 0
    for user_id_key, account_data in accounts.items():
        user_id += 1  # Increment user_id for each account
        account_entry = [
            user_id,
            account_data.get('firstName', ''),
            account_data.get('middleInitial', ''),
            account_data.get('lastName', ''),
            account_data.get('phone', ''),
            account_data.get('email', ''),
            account_data.get('password', '')
        ]
        accounts_lis.append(account_entry)

    return accounts_lis    


def get_account_details(id=None):                           ## Returns account details (type: list)
    """ returns account_id in accounts[0] """
    global accounts_list
    accounts_list = update_accounts()
    for account in accounts_list:
        if account[0] == id:
            return account
    
    return None


def check_credentials(uname, pword):
    """ USED FOR LOGGING IN """
    """ returns account_id or None """
    global accounts_list
    accounts_list = update_accounts()
    ##[[1, "firstname", "initial", "lastname", "09xxxxxxxxx", "email@gmail.com", "HashedPass"]]
    
    sha256 = hashlib.sha256()
    sha256.update(pword.encode('utf-8'))
    pword = sha256.hexdigest()

    # Check if email/phone matches the password.
    for account in accounts_list:
        stored_email = account[-2].lower()
        stored_phone = account[-3]
        stored_hashed_password = account[-1]
        
        if stored_email == uname.lower() or stored_phone == uname:
            if pword == stored_hashed_password:
                return account[0]

    return None


def save_account(fname, initial, lname, email, pword):  ## Returns None
    """ Creates a new (admin) account using the parameters """
    ref = db.reference('accounts')

    sha256 = hashlib.sha256()
    sha256.update(pword.encode('utf-8'))
    pword = sha256.hexdigest()
    email = email.lower()

    # New resident data
    new_user = {
        'firstName': f'{fname}',
        'middleInitial': f'{initial}',
        'lastName': f'{lname}',
        'phone': '',
        'email': f'{email}',
        'password': f'{pword}'
    }

    # Add the new resident to the database
    ref.child("user_id_1").set(new_user) 
    
    messagebox.showinfo("Welcome", "Account created successfully!")

def change_password(id=None, new_password=None):                  ## Returns None
    """ Change the password of user_id_1 (admin) """

    sha256 = hashlib.sha256()
    sha256.update(new_password.encode('utf-8'))
    new_password = sha256.hexdigest()
    
    # Reference to the specific account in the database
    account_ref = db.reference('accounts/user_id_1')

    # Update the password field in the database
    account_ref.update({'password': new_password})


def change_phone(id=None, new_phone=""):                        ## Returns None
    """ Change phone number of the admin """
    # Reference to the specific account in the database
    account_ref = db.reference('accounts/user_id_1')

    # Update the password field in the database
    account_ref.update({'phone': new_phone})
    

def is_email_exists(email):                             ## Returns "ID" or None
    global accounts_list
    accounts_list = update_accounts()

    for account in accounts_list:
        for element in account:
            if str(element).lower() == email.lower():
                return account[1]
    
    messagebox.showerror("Invalid Email", "There is no account connected to {email}.")
    return None

def is_empty():                                         ## Returns True or False
    # Reference to the accounts table
    ref = db.reference('accounts')

    # Fetch data from Firebase Realtime Database
    accounts = ref.get()

    if accounts == None:
        return True
    else:
        return False

if __name__ == '__main__':
    cred = credentials.Certificate("database\\credentials.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://waterlevelmonitoringsystem-db-default-rtdb.asia-southeast1.firebasedatabase.app"})

    #print(update_accounts())           # Returns 2d List

    #print(get_account_details())       # Returns List

    #print(check_credentials(uname="example1@example.com", pword="Bulagg"))  # Returns None or 1
            # [1, 'Admin', 'X', 'Rin', '1234567890', 'example1@example.com', 'Bulaga']

    #save_account(fname="Admin", initial="X", lname="Lilly", email="fls.sequel@gmail.com", pword="Pword")

    #change_password(new_password="Password_ng_inamo")      # Change password

    #change_phone(new_phone="09696969696")

    #print(is_email_exists(email="fls.sequel@gmail.com"))

    #print(is_email_exists(email="xxx.sequel@gmail.com"))

    #print(is_empty())
    print()