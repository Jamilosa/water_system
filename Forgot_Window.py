## GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from customtkinter import (set_appearance_mode, set_default_color_theme, CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, CTkScrollableFrame, CTkTextbox, CTkInputDialog, CTkToplevel)

# SECRET
import threading

## CUSTOM
import Account
from Widgets import *
import Email_Smtp
import Input_Validation


class ForgotWindow(CTk):
    def __init__(self, parent):
        super().__init__()

        self.parent=parent
        self.title("Forgot Password")
        self.iconbitmap("assets/logo.ico")
        self.geometry('600x400')
        self.resizable(width=False, height=False)
        self.secret_code = 0
        self.forgot_account_id = '0'


        # CREATE MAIN FRAME
        self.forgot_frame = Frame_Ng_Inamo(self,
                                          border_width=parent._outer_border_width, 
                                          border_color=parent._outer_border_color, 
                                          corner_radius=parent._outer_corner_radius, 
                                          )
        self.forgot_frame.configure(fg_color=parent._outer_border_fill)
        self.forgot_frame.pack(padx=5, pady=5, fill='both', expand=True)

        # FORM TITLE
        self.forgot_frame_title = Frame_Ng_Inamo(self.forgot_frame)
        self.forgot_frame_title.pack(padx=5, pady=5, fill='x', expand=True)

        self.title_label = Label_Ng_Inamo(self.forgot_frame_title, text="FORGOT PASSWORD")
        self.title_label.configure(font=parent.title_font)
        self.title_label.pack(padx=10, pady=10)

        # FORM CONTENT
        self.forgot_frame_form = Frame_Ng_Inamo(self.forgot_frame)
        self.forgot_frame_form.pack(padx=5, pady=5, expand=True)

        # _Button Frame
        self.forgot_frame_button = Frame_Ng_Inamo(self.forgot_frame)
        self.forgot_frame_button.pack(padx=10, pady=10)

        self.display_forgot_form()
        self.mainloop()

    def display_forgot_form(self):
        self.clear_contents()
        self.username_label = Label_Ng_Inamo(self.forgot_frame_form, text="Email:")
        self.username_label.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        self.username_entry = Entry_Ng_inamo(self.forgot_frame_form, width=500)
        self.username_entry.grid(row=1, column=0, padx=10, pady=10)

        self.back_button = Button_Ng_Inamo(self.forgot_frame_button, command=self.return_to_login, text="Back").grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.next_button = Button_Ng_Inamo(self.forgot_frame_button, command=self.send_verification_code, text="Next").grid(row=0, column=1, columnspan=1, padx=10, pady=10)


    def return_to_login(self):
        # If the user clicked "Back" button
        self.destroy()
        self.parent.show_login_window()

    def send_verification_code(self):
        # Ask for their username/email/phone
        email = self.username_entry.get()
        email = email.lower()

        # Validate the email
        if Input_Validation.validate_email(email) == False:
            return
        else:
            self.valid_email = email

        # Check if email exist in the database
        self.forgot_account_id = Account.is_email_exists(email) # ID/None (show error)
        if self.forgot_account_id == None:
            return

        # Nested functions
        def start_on_thread():
            # Start another thread to send the email
            thread = threading.Thread(target=send_email_and_confirm)
            thread.start()

        def send_email_and_confirm():
            self.secret_code = Email_Smtp.send_email_code(self.valid_email, subject="RESET PASSWORD")
        
        start_on_thread()

        self.confirm_verification_code()
        
    def confirm_verification_code(self):
        self.clear_contents()
        self.code_label = Label_Ng_Inamo(self.forgot_frame_form, text="Enter Code")
        self.code_label.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        self.code_entry = Entry_Ng_inamo(self.forgot_frame_form, width=500)
        self.code_entry.grid(row=1, column=0, padx=10, pady=10)

        def check_code():
            if self.code_entry.get() == self.secret_code:
                self.accept_new_password()
            else:
                messagebox.showerror("Invalid Code", "The verification code did not match.")

        Button_Ng_Inamo(self.forgot_frame_button, command=self.display_forgot_form, text="Back").grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        Button_Ng_Inamo(self.forgot_frame_button, command=check_code, text="Next").grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        
    def accept_new_password(self):
        self.clear_contents()
        self.new_password_label = Label_Ng_Inamo(self.forgot_frame_form, text="New Password")
        self.new_password_label.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        self.new_password_entry = Entry_Ng_inamo(self.forgot_frame_form, show="*", width=500)
        self.new_password_entry.grid(row=1, column=0, padx=10, pady=10)

        self.new_password_confirm_label = Label_Ng_Inamo(self.forgot_frame_form, text="Confirm New Password")
        self.new_password_confirm_label.grid(row=2, column=0, padx=10, pady=0, sticky='w')
        self.new_password_confirm_entry = Entry_Ng_inamo(self.forgot_frame_form, show="*", width=500)
        self.new_password_confirm_entry.grid(row=3, column=0, padx=10, pady=10)

        def check_password():
            if self.new_password_entry.get() == self.new_password_confirm_entry.get():
                Account.change_password(id=self.forgot_account_id, new_password=self.new_password_entry.get())
                messagebox.showinfo("Password Reset Success", "Password reset was successful.")
                self.destroy()
                self.parent.show_login_window()
            else:
                messagebox.showinfo("Password Reset Failed", "Password did not match.")

        Button_Ng_Inamo(self.forgot_frame_button, command=self.display_forgot_form, text="Back").grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        Button_Ng_Inamo(self.forgot_frame_button, command=check_password, text="Next").grid(row=0, column=1, columnspan=1, padx=10, pady=10)

    def clear_contents(self):
        for child in self.forgot_frame_form.winfo_children() + self.forgot_frame_button.winfo_children(): child.destroy()
