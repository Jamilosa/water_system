## GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from customtkinter import (CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, CTkScrollableFrame, CTkTextbox, CTkInputDialog, CTkToplevel)

## CUSTOM
import Account
from Widgets import *
import Forgot_Window

class LoginWindow(CTkToplevel):
    def __init__(self, parent):
        super().__init__()

        self.parent=parent
        self.title("Login Window")
        self.iconbitmap("assets/logo.ico")
        self.geometry('600x400')
        self.resizable(width=False, height=False)

        self.login_frame = Frame_Ng_Inamo(self,
                                          border_width=parent._outer_border_width, 
                                          border_color=parent._outer_border_color, 
                                          corner_radius=parent._outer_corner_radius, 
                                          )
        self.login_frame.configure(fg_color=parent._outer_border_fill)
        self.login_frame.pack(padx=5, pady=5, fill='both', expand=True)

        # FORM TITLE
        self.login_frame_title = Frame_Ng_Inamo(self.login_frame)
        self.login_frame_title.pack(padx=5, pady=5, fill='x', expand=True)

        self.title_label = Label_Ng_Inamo(self.login_frame_title, text="LOG IN")
        self.title_label.configure(font=parent.title_font)
        self.title_label.pack(padx=10, pady=10)

        # FORM CONTENT
        self.login_frame_form = Frame_Ng_Inamo(self.login_frame)
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
        self.login_frame_button = Frame_Ng_Inamo(self.login_frame)
        self.login_frame_button.pack(padx=10, pady=10)

        self.forgot_button = Button_Ng_Inamo(self.login_frame_button, command=self.forgot_password, text="Forgot Password").grid(row=0, column=0, columnspan=1, padx=10, pady=10)
        self.login_button = Button_Ng_Inamo(self.login_frame_button, command= lambda pr=parent: self.login(pr), text="Login").grid(row=0, column=1, columnspan=1, padx=10, pady=10)
        self.mainloop()

    def login(self, parent):
        username = self.username_entry.get()
        password = self.password_entry.get()

        id = Account.check_credentials(uname=username, pword=password)
        # Returns Id or none
        if id is not None:
            self.destroy()
            parent.logged_in_accound_id = id
            messagebox.showinfo("Login Successful", f"Welcome to the water level system manager.")
            self.parent.show_main_window()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")    

    def forgot_password(self):
        # Destroy the Log in window and open a Forgot Password Window
        self.destroy()

        forgot_window = Forgot_Window.ForgotWindow(self.parent)
        forgot_window.mainloop()
