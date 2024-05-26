## GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import filedialog
from customtkinter import (set_appearance_mode, set_default_color_theme, CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, CTkScrollableFrame, CTkTextbox, CTkInputDialog, CTkToplevel)

## GRAPH
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker
import mysql.connector

## DATABASE
import firebase_admin
from firebase_admin import db, credentials

# SECRET
from datetime import datetime
import threading

## CUSTOM
import Resident_Management
import Generate_Report
import System_Information
import Account
from Widgets import *
import Email_Smtp
import Input_Validation

class RegisterWindow(CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent=parent
        self.title("Registration")
        self.iconbitmap("assets/logo.ico")
        self.geometry('600x400')
        self.resizable(width=False, height=False)

        self.is_pass_visible = False
        self.secret_code = 0
        
        self.register_frame = Frame_Ng_Inamo(self,
                                          border_width=parent._outer_border_width, 
                                          border_color=parent._outer_border_color, 
                                          corner_radius=parent._outer_corner_radius, 
                                          )
        self.register_frame.configure(fg_color=parent._outer_border_fill)
        self.register_frame.pack(padx=5, pady=5, fill='both', expand=True)

        # FORM TITLE
        self.register_frame_title = Frame_Ng_Inamo(self.register_frame)
        self.register_frame_title.pack(padx=5, pady=5, fill='x', expand=True)

        self.title_label = Label_Ng_Inamo(self.register_frame_title, text="Register")
        self.title_label.configure(font=parent.title_font)
        self.title_label.pack(padx=10, pady=10)

        # FORM CONTENT
        self.login_frame_form = Frame_Ng_Inamo(self.register_frame)
        self.login_frame_form.pack(padx=5, pady=5, expand=True)

        self.username_label = Label_Ng_Inamo(self.login_frame_form, text="Email/Phone:")
        self.username_label.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        self.username_entry = Entry_Ng_inamo(self.login_frame_form, width=500)
        self.username_entry.grid(row=1, column=0, padx=10, pady=10)

        self.password_label = Label_Ng_Inamo(self.login_frame_form, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=0, sticky='w')
        self.password_entry = Entry_Ng_inamo(self.login_frame_form, show="*", width=500)
        self.password_entry.grid(row=3, column=0, padx=10, pady=10)

        # _Button Frame
        self.register_frame_button = Frame_Ng_Inamo(self.register_frame)
        self.register_frame_button.pack(padx=10, pady=10)

        self.register_button = Button_Ng_Inamo(self.register_frame_button, command=self.display_password, text="Show Password")
        self.register_button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        
        self.next_button = Button_Ng_Inamo(self.register_frame_button, command=self.send_verification_code, text="Next")
        self.next_button.grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        self.mainloop()

    def send_verification_code(self):
        def start_on_thread():
            thread = threading.Thread(target=send_email_and_confirm)
            thread.start()

        def send_email_and_confirm():
            self.secret_code = Email_Smtp.send_email_code(self.valid_email)

        self.email = self.username_entry.get()
        self.pword = self.password_entry.get()

        if len(self.pword) < 4:
            messagebox.showerror("Password Insecure", "Please use a strong password.")
            return
        else:
            self.valid_pword = self.pword
        
        if Email_Smtp.validate_email(self.email) == False:
            return
        else:
            self.valid_email = self.email
            start_on_thread()
            self.confirm_verification_code()
    
    def confirm_verification_code(self):
        self.clear_contents()
        self.code_label = Label_Ng_Inamo(self.login_frame_form, text="Enter Code")
        self.code_label.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        self.code_entry = Entry_Ng_inamo(self.login_frame_form, width=500)
        self.code_entry.grid(row=1, column=0, padx=10, pady=10)

        def check_code():
            if self.code_entry.get() == self.secret_code:
                self.accept_admin_name()
            else:
                messagebox.showerror("Invalid Code", "The verification code did not match.")

        Button_Ng_Inamo(self.register_frame_button, command=check_code, text="Next").grid(row=0, column=1, columnspan=2, padx=10, pady=10)


    def accept_admin_name(self):
        self.clear_contents()
        self.firstname_label = Label_Ng_Inamo(self.login_frame_form, text="First Name")
        self.firstname_label.grid(row=0, column=0, padx=10, pady=0, sticky='w')
        self.firstname_entry = Entry_Ng_inamo(self.login_frame_form, width=500)
        self.firstname_entry.grid(row=1, column=0, padx=10, pady=10)

        self.initial_label = Label_Ng_Inamo(self.login_frame_form, text="Middle Initial")
        self.initial_label.grid(row=2, column=0, padx=10, pady=0, sticky='w')
        self.initial_entry = Entry_Ng_inamo(self.login_frame_form, width=500)
        self.initial_entry.grid(row=3, column=0, padx=10, pady=10)

        self.lastname_label = Label_Ng_Inamo(self.login_frame_form, text="Last Name")
        self.lastname_label.grid(row=4, column=0, padx=10, pady=0, sticky='w')
        self.lastname_entry = Entry_Ng_inamo(self.login_frame_form, width=500)
        self.lastname_entry.grid(row=5, column=0, padx=10, pady=10)

        def validate_names():
            self.fname = self.firstname_entry.get()
            self.initial = self.initial_entry.get()
            self.lname = self.lastname_entry.get()

            if Input_Validation.validate_name(self.fname):
                if Input_Validation.validate_name(self.initial):
                    if Input_Validation.validate_name(self.lname):
                        self.valid_fname = self.fname
                        self.valid_initial = self.initial
                        self.valid_lname = self.lname

                        Account.save_account(fname=f"{self.valid_fname}", initial=f"{self.valid_initial}", lname=f"{self.valid_lname}", email=f"{self.valid_email}", pword=f"{self.valid_pword}")
                        self.destroy()
                        self.parent.show_login_window()

        Button_Ng_Inamo(self.register_frame_button, command=validate_names, text="Next").grid(row=0, column=1, columnspan=2, padx=10, pady=10)

    def display_password(self):
        if self.is_pass_visible:
            self.is_pass_visible = False
            self.password_entry.configure(show="*")
            self.register_button.configure(text="Show Password")
        else:
            self.is_pass_visible = True
            self.password_entry.configure(show="")
            self.register_button.configure(text="Hide Password")

    def clear_contents(self):
        for child in self.login_frame_form.winfo_children() + self.register_frame_button.winfo_children(): child.destroy()