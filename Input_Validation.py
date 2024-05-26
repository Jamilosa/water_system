from tkinter import messagebox
from re import match
from Resident_Management import resident_phone_available

##############################################
##             INPUT VALIDATION             ##
##   RETURNS:                               ##
##      True   - Valid                      ##
##      False  - Invalid                    ##
##############################################

def validate_name(name): # ALPHABET + SPACE (1-15 CHAR)
    if match(r'^[a-zA-Z\s]{1,15}$', name):
        return True
    messagebox.showerror("Invalid Name", "Name must only contain alphabet.")
    return False


def validate_water_level(water_level): # FLOAT + 1 DEIMAL ( 1.0 to 999.0 )
    if match(r'^([1-9]\d{0,2}(\.\d)?|1000)$', water_level):
        return True
    
    messagebox.showerror("Invalid Water Level", "Water level must be a float (1.0 - 999.0).")
    return True
    


def validate_street(street):
    if match(r'^[a-zA-Z0-9\s]{1,15}$', street): # ALPHANUMERIC + SPACE (1-15 CHAR)
        return True
        
    messagebox.showerror("Invalid Street", "Street name is must only contain alphanumeric characters.")
    return False
    

def validate_house_number(house_number):
    if match(r'^\d{1,4}$', house_number): # INT ONLY (1-4 CHAR)
        return True
    messagebox.showerror("Invalid House Number", "House number must only contain numbers (1-9999).")
    return False


def validate_phone(phone):
    if match(r'^\d{11}$', phone): # INT (11 CHAR)
        if not resident_phone_available(phone):
            messagebox.showerror(f"Invalid Phone Number", "Phone number {phone} is already used.")
            return False
        else:
            return True
        
    messagebox.showerror("Invalid Phone Number", "Phone number must follow 09xxxxxxxxx format.")
    return False


def validate_email(email):
    if match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email): # MAGIC
        return True
    
    messagebox.showerror("Invalid Email", f"{email} is not a valid email.")
    return False


if __name__ == '__main__':
    messagebox.showinfo("RUNNING ON EXTERNAL MODULE", "You are on INPUT VALIDATION.")