## GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import DateEntry
from tkinter import filedialog
#from customtkinter import (set_appearance_mode, set_default_color_theme, CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, CTkScrollableFrame, CTkTextbox, CTkInputDialog, CTkToplevel, CTkImage)
from customtkinter import *



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
import Input_Validation

import Login_Window
import Register_Window

cred = credentials.Certificate("database\\credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://waterlevelmonitoringsystem-db-default-rtdb.asia-southeast1.firebasedatabase.app"})

deactivate_automatic_dpi_awareness()

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        ctk.set_widget_scaling(1.0)
        
        self.title("System Manager")
        self.geometry("1000x700")
        self.iconbitmap('assets/logo.ico')
        self.minsize(800, 500)
        self.title_font = ('Segoe UI', 20)
        self.logged_in_accound_id = 0
        
        """ OUTER BORDER """
        self._outer_border_fill = '#E6E8E6'
        self._outer_corner_radius = 5
        self._outer_border_width = 2
        self._outer_border_color = '#212121'
        
        """ INNER BORDER """
        self._inner_border_fill = 'white'
        self._inner_corner_radius = 5
        self._inner_border_width = 1
        self._inner_border_color = '#212121'

        """ ENTRY/TEXTBOX PADDING """
        self.sms_template_height = 100
        self.sms_expanded_height = 200
        self.texbox_pady = 10
        self.texbox_padx = 5

        """ LABEL """
        self.hover_in_fill = 'dark grey'
        self.settings_label_width = 80
        self.settings_label_justify = 'left'
        self.settings_label_anchor = 'w'

        self.initialize_widgets()

    """ MAIN WIDGET """
    def initialize_widgets(self):
        # MAIN FRAME
        self.outer_frame = Frame_Ng_Inamo(self, 
                                          border_width=self._outer_border_width, 
                                          border_color=self._outer_border_color, 
                                          corner_radius=self._outer_corner_radius, 
                                          )
        self.outer_frame.configure(fg_color=self._outer_border_fill)
        self.outer_frame.pack(padx=5, pady=5, fill='both', expand=True)

        # MAIN TITLE FRAME
        self.outer_title_frame = Frame_Ng_Inamo(self.outer_frame)
        self.outer_title_frame.pack(padx=10, pady=10, fill='x')

        # CONTENT FRAME
        self.inner_frame = Frame_Ng_Inamo(self.outer_frame, 
                                          border_width=self._inner_border_width, 
                                          border_color=self._inner_border_color, 
                                          corner_radius=self._inner_corner_radius, 
                                          bg_color=self._inner_border_fill
                                          )
        self.inner_frame.configure(fg_color=self._inner_border_fill)
        self.inner_frame.pack(padx=5, pady=5, fill='both', expand=True)
        
        self.content_frame = CTkScrollableFrame(self.inner_frame, 
                                                bg_color=self._inner_border_fill,
                                                scrollbar_button_color=self._inner_border_fill, 
                                                scrollbar_button_hover_color=self._inner_border_fill, 
                                                fg_color=self._inner_border_fill,
                                                )
        self.content_frame.pack(padx=5, pady=5, fill='both', expand=True)

        # WINDOW BUTTON FRAME
        self.bot_frame = Frame_Ng_Inamo(self, height=20)
        self.bot_frame.pack(padx=20, pady=10, side='right')

        ## INITIALIZE LABELS
        self.content_title = Label_Ng_Inamo(self.outer_title_frame, text=' ')
        self.content_title.configure(font=self.title_font)
        self.content_title.pack(padx=10, pady=10)

        self.content_content = Label_Ng_Inamo(self.content_frame, text=' ')
        self.content_content.pack(padx=10, pady=10) 

        
        menu_app = tk.Menu(self, borderwidth=0, fg = 'black', activeborderwidth = 0, activebackground = 'light blue', activeforeground='grey', background='white', relief='flat', selectcolor='green')
        
        # Create menu labels
        menu_resident = tk.Menu(menu_app, tearoff=0, borderwidth=0, fg = 'black', activeborderwidth = 0, activebackground = 'light blue', activeforeground='grey', background='white', relief='flat', selectcolor='green')
        menu_system = tk.Menu(menu_app, tearoff=0, borderwidth = 0, fg = 'black', activeborderwidth = 0, activebackground = 'light blue', activeforeground='grey', background='white', relief='flat', selectcolor='green')
        menu_report = tk.Menu(menu_app, tearoff=0, borderwidth = 0, fg = 'black', activeborderwidth = 0, activebackground = 'light blue', activeforeground='grey', background='white', relief='flat', selectcolor='green')
        menu_account = tk.Menu(menu_app, tearoff=0, borderwidth = 0, fg = 'black', activeborderwidth = 0, activebackground = 'light blue', activeforeground='grey', background='white', relief='flat', selectcolor='green')
        menu_help = tk.Menu(menu_app, tearoff=0, borderwidth = 0, fg = 'black', activeborderwidth = 0, activebackground = 'light blue', activeforeground='grey', background='white', relief='flat', selectcolor='green')
        
        # Resident menu options
        menu_resident.add_command(label='Add Resident', command=self.resident_add_resident)
        menu_resident.add_command(label='View Residents', command=self.resident_view_residents)
        menu_app.add_cascade(label="Resident", menu=menu_resident)

        # System menu options
        menu_system.add_command(label='SMS Templates', command=self.system_sms_template)
        menu_system.add_command(label='Warning Levels', command=self.system_warning_levels)
        menu_app.add_cascade(label="System", menu=menu_system)

        # Report menu options
        menu_report.add_command(label='Today', command=lambda: self.check_records_existance("today"))
        menu_report.add_command(label='Past Dates', command=self.choose_date)
        menu_app.add_cascade(label="Report", menu=menu_report)

        # Account menu options
        menu_account.add_command(label='My account', command=self.account_my_account)
        menu_account.add_command(label='Log out', command=self.account_logout)
        menu_app.add_cascade(label="Account", menu=menu_account)

        # Help menu options
        menu_help.add_command(label='It\'s a prank')
        menu_help.add_command(label='I don\'t need help')
        menu_app.add_cascade(label="Help", menu=menu_help)

        self.configure(menu=menu_app)  


    """ DASHBOARD """
    def display_graph(self):
        self.content_title.configure(text='WATER LEVEL')
        self.clear_contents()

        # _Diagram
        self.frame_graph_plot = Frame_Ng_Inamo(self.content_frame)
        self.frame_graph_plot.pack(padx=10, pady=10, fill='both', expand=True)

        self.fig, self.ax = plt.subplots()
        self.ax.grid(True, color='lightblue', linewidth=1)
        self.line, = self.ax.plot([], [], marker='', color='b')

        self.fig.subplots_adjust(top=1)
        self.fig.patch.set_facecolor(self._inner_border_fill)  # Main window background color #
        self.ax.set_facecolor(self._inner_border_fill)  # Plot background color

        self.ax.set_xlim(0, 7)
        self.ax.set_ylim(0, 100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_graph_plot)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.points = []
        self.update_plot()  # Start the update loop
        self.after_id = self.after(120000, self.update_plot)  # Store the after id

    def update_plot(self):
    # Fetch data from Firebase Realtime Database
        ref = db.reference('waterLevels')
        data = ref.order_by_key().limit_to_last(15).get()

        if data:
            self.points = [float(record['value']) for record in data.values()]
            timestamps = [record['timestamp'] for record in data.values()]
            new_time = []
            for mytime in timestamps:
                outt = mytime.split(' ')[1].split(':')[:2]  # HH:MM
                outt = f"{outt[0]}:{outt[1]}"
                new_time.append(outt)
            
            # Update the plot
            self.line.set_xdata(range(len(new_time)))  # Use numerical index for x-axis
            self.line.set_ydata(self.points)

            # Adjust x-axis ticks and labels
            self.ax.set_xticks(range(len(new_time)))
            self.ax.set_xticklabels(new_time)  # Rotate labels for better visibility

            # Adjust y-axis limits dynamically based on the maximum value of the data
            max_y = max(self.points) + 10  # Add some padding for better visualization
            self.ax.set_ylim(0, max_y)
            self.ax.set_xlim(-0.5, max(6.5, len(self.points) - 0.5))  # Adjust x-axis limit

            # Set Labels
            def format_yticks(value, _):
                return f'{value} cm'
            self.ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(format_yticks))

            self.canvas.draw()
            
            self.after_id = self.after(1000, self.update_plot)


    """ RESIDENT METHODS """
    def resident_add_resident(self):
        self.content_title.configure(text='NEW RESIDENT FORM')
        self.clear_contents()

        left_frame = Frame_Ng_Inamo(self.content_frame)
        left_frame.pack(side='left', fill='both', expand=True)

        Frame1 = Frame_Ng_Inamo(left_frame)
        Frame1.pack(fill='x')
        Label_Ng_Inamo(Frame1, text='\nFirstname' ).pack(padx=20, pady=5, side='left')
        fname_entry = Entry_Ng_inamo(left_frame)
        fname_entry.pack(padx=20, pady=5, fill='x')

        Frame2 = Frame_Ng_Inamo(left_frame)
        Frame2.pack(fill='x')
        Label_Ng_Inamo(Frame2, text='\nMiddle Initial' ).pack(padx=20, pady=5, side='left')

        initial_entry = Entry_Ng_inamo(left_frame)
        initial_entry.pack(padx=20, pady=5, fill='x')

        Frame3 = Frame_Ng_Inamo(left_frame)
        Frame3.pack(fill='x')
        Label_Ng_Inamo(Frame3, text='\nLast Name' ).pack(padx=20, pady=5, side='left')
        lname_entry = Entry_Ng_inamo(left_frame)
        lname_entry.pack(padx=20, pady=5, fill='x')

        right_frame = Frame_Ng_Inamo(self.content_frame)
        right_frame.pack(side='right', fill='both', expand=True)

        Frame4 = Frame_Ng_Inamo(right_frame)
        Frame4.pack(fill='x')
        Label_Ng_Inamo(Frame4, text='\nPhone Number' ).pack(padx=20, pady=5, side='left')
        phone_num = Entry_Ng_inamo(right_frame)
        phone_num.pack(padx=20, pady=5, fill='x')

        Frame5 = Frame_Ng_Inamo(right_frame)
        Frame5.pack(fill='x')
        Label_Ng_Inamo(Frame5, text='\nHome Number' ).pack(padx=20, pady=5, side='left')
        home_num = Entry_Ng_inamo(right_frame)
        home_num.pack(padx=20, pady=5, fill='x')

        Frame6 = Frame_Ng_Inamo(right_frame)
        Frame6.pack(fill='x')
        Label_Ng_Inamo(Frame6, text='\nStreet' ).pack(padx=20, pady=5, side='left')
        street_entry = Entry_Ng_inamo(right_frame)
        street_entry.pack(padx=20, pady=5, fill='x')
    
        def save_res():
            fname = fname_entry.get()
            initial = initial_entry.get()
            lname = lname_entry.get()
            phone = phone_num.get()
            house = home_num.get()
            street = street_entry.get()
            
            if not Input_Validation.validate_name(fname): return
            if not Input_Validation.validate_name(initial): return 
            if not Input_Validation.validate_name(lname): return
            if not Input_Validation.validate_phone(phone): return
            if not Input_Validation.validate_house_number(house): return 
            if not Input_Validation.validate_street(street): return

            wanna_add = Resident_Management.add_resident(first_name=fname, middle_initial=initial, last_name=lname, house_number=house, street=street, phone_number=phone)
            if wanna_add == True:
                self.resident_add_resident()
            
            self.resident_view_residents()
        
        Button_Ng_Inamo(self.bot_frame, text="Cancel", command=self.home_dashboard).pack(padx=10, side='left')
        Button_Ng_Inamo(self.bot_frame, text="Save", command=save_res).pack(padx=0, side='right')

    def resident_view_residents(self):
        self.content_title.configure(text='RESIDENTS')
        self.clear_contents()

        header_frame = Frame_Ng_Inamo(self.content_frame)
        header_frame.configure(fg_color='black')
        header_frame.pack(fill='x')


        resident_list = Resident_Management.get_residents()

        if resident_list == None:
            Label_Ng_Inamo(header_frame, text="No Residents").pack()
            header_frame.configure(fg_color='transparent')
            return

        Label_Ng_Inamo(header_frame, text="ID", width=50, text_color='white', justify='left', anchor='w').grid(row=0, column=0, padx=10)
        Label_Ng_Inamo(header_frame, text="Last name", width=200, text_color='white', justify='left', anchor='w').grid(row=0, column=1)
        Label_Ng_Inamo(header_frame, text="First name", width=200, text_color='white', justify='left', anchor='w').grid(row=0, column=2)
        Label_Ng_Inamo(header_frame, text="Street", width=100, text_color='white', justify='left', anchor='w').grid(row=0, column=3)
        Label_Ng_Inamo(header_frame, text="House", width=90, text_color='white', justify='left', anchor='w').grid(row=0, column=4)
        Label_Ng_Inamo(header_frame, text="Phone", width=220, text_color='white', justify='left', anchor='w').grid(row=0, column=5)

        for index, record in enumerate(resident_list, start=1):
            id, first_name, middle_initial, last_name, house_number, street, phone = record

            record_frame = Frame_Ng_Inamo(self.content_frame)
            record_frame.pack(pady=1, fill='both', expand=True)

            lb1 = Label_Ng_Inamo(record_frame, text=id, width=50, justify='left', anchor='w')
            lb1.grid(row=index, column=0, padx=10)
            lb1.bind("<Button-1>", lambda event, rec=record: self.resident_display_resident(event, rec))
            lb1.bind("<Enter>", lambda event, fr=record_frame: self.resident_on_enter(event, fr))
            lb1.bind("<Leave>", lambda event, fr=record_frame: self.resident_on_leave(event, fr))

            lb2 = Label_Ng_Inamo(record_frame, text=last_name, width=200, justify='left', anchor='w')
            lb2.grid(row=index, column=1)
            lb2.bind("<Button-1>", lambda event, rec=record: self.resident_display_resident(event, rec))
            lb2.bind("<Enter>", lambda event, fr=record_frame: self.resident_on_enter(event, fr))
            lb2.bind("<Leave>", lambda event, fr=record_frame: self.resident_on_leave(event, fr))

            lb3 = Label_Ng_Inamo(record_frame, text=f"{first_name} {middle_initial}.", width=200, justify='left', anchor='w')
            lb3.grid(row=index, column=2)
            lb3.bind("<Button-1>", lambda event, rec=record: self.resident_display_resident(event, rec))
            lb3.bind("<Enter>", lambda event, fr=record_frame: self.resident_on_enter(event, fr))
            lb3.bind("<Leave>", lambda event, fr=record_frame: self.resident_on_leave(event, fr))

            lb4 = Label_Ng_Inamo(record_frame, text=street, width=100, justify='left', anchor='w')
            lb4.grid(row=index, column=3)
            lb4.bind("<Button-1>", lambda event, rec=record: self.resident_display_resident(event, rec))
            lb4.bind("<Enter>", lambda event, fr=record_frame: self.resident_on_enter(event, fr))
            lb4.bind("<Leave>", lambda event, fr=record_frame: self.resident_on_leave(event, fr))

            lb5 = Label_Ng_Inamo(record_frame, text=house_number, width=90, justify='left', anchor='w')
            lb5.grid(row=index, column=4)
            lb5.bind("<Button-1>", lambda event, rec=record: self.resident_display_resident(event, rec))
            lb5.bind("<Enter>", lambda event, fr=record_frame: self.resident_on_enter(event, fr))
            lb5.bind("<Leave>", lambda event, fr=record_frame: self.resident_on_leave(event, fr))

            lb6 = Label_Ng_Inamo(record_frame, text=phone, width=220, justify='left', anchor='w')
            lb6.grid(row=index, column=5)
            lb6.bind("<Button-1>", lambda event, rec=record: self.resident_display_resident(event, rec))
            lb6.bind("<Enter>", lambda event, fr=record_frame: self.resident_on_enter(event, fr))
            lb6.bind("<Leave>", lambda event, fr=record_frame: self.resident_on_leave(event, fr))

        # BUTTONS
        Button_Ng_Inamo(self.bot_frame, text="Back", command=self.home_dashboard).pack(padx=10, side='left')
        Button_Ng_Inamo(self.bot_frame, text="Search", command=self.resident_search_resident).pack(padx=0, side='right')

    def resident_display_resident(self, event, record):
        self.content_title.configure(text='RESIDENT DETAILS')
        self.clear_contents()

        left_frame = Frame_Ng_Inamo(self.content_frame)
        left_frame.pack(side='left', fill='both', expand=True)

        Frame1 = Frame_Ng_Inamo(left_frame)
        Frame1.pack(fill='x')
        Label_Ng_Inamo(Frame1, text='\nFirstname').pack(padx=20, pady=5, side='left')
        fname_entry = Entry_Ng_inamo(left_frame)
        fname_entry.pack(padx=20, pady=5, fill='x')

        Frame2 = Frame_Ng_Inamo(left_frame)
        Frame2.pack(fill='x')
        Label_Ng_Inamo(Frame2, text='\nMiddle Initial').pack(padx=20, pady=5, side='left')
        initial_entry = Entry_Ng_inamo(left_frame)
        initial_entry.pack(padx=20, pady=5, fill='x')

        Frame3 = Frame_Ng_Inamo(left_frame)
        Frame3.pack(fill='x')
        Label_Ng_Inamo(Frame3, text='\nLast Name').pack(padx=20, pady=5, side='left')
        lname_entry = Entry_Ng_inamo(left_frame)
        lname_entry.pack(padx=20, pady=5, fill='x')



        right_frame = Frame_Ng_Inamo(self.content_frame)
        right_frame.pack(side='right', fill='both', expand=True)

        Frame4 = Frame_Ng_Inamo(right_frame)
        Frame4.pack(fill='x')
        Label_Ng_Inamo(Frame4, text='\nPhone Number').pack(padx=20, pady=5, side='left')
        phone_num_entry = Entry_Ng_inamo(right_frame)
        phone_num_entry.pack(padx=20, pady=5, fill='x')

        Frame5 = Frame_Ng_Inamo(right_frame )
        Frame5.pack(fill='x')
        Label_Ng_Inamo(Frame5, text='\nHome Number').pack(padx=20, pady=5, side='left')
        home_num_entry = Entry_Ng_inamo(right_frame)
        home_num_entry.pack(padx=20, pady=5, fill='x')

        Frame6 = Frame_Ng_Inamo(right_frame )
        Frame6.pack(fill='x')
        Label_Ng_Inamo(Frame6, text='\nStreet').pack(padx=20, pady=5, side='left')
        street_entry = Entry_Ng_inamo(right_frame)
        street_entry.pack(padx=20, pady=5, fill='x')

        fname_entry.insert('0', record[1])
        initial_entry.insert('0', record[2])
        lname_entry.insert('0', record[3])
        phone_num_entry.insert('0', record[6])
        home_num_entry.insert('0', record[5])
        street_entry.insert('0', record[4])

        # BUTTONS
        Button_Ng_Inamo(self.bot_frame, text="Back", command=self.resident_view_residents).pack(padx=10, side='left')
        Button_Ng_Inamo(self.bot_frame, text="Delete", command= lambda rec=record: self.resident_delete_resident(rec)).pack(padx=0, side='right')

    def resident_delete_resident(self, record):
        if Resident_Management.delete_resident(record[0]):
            self.resident_view_residents()
        else:
            self.resident_display_resident("event", record)

    def resident_search_resident(self):
        self.content_title.configure(text='RESIDENTS')
        self.clear_contents()
        
        search_dialog = Dialog_Ng_Inamo(title="Resident Search", text="Type a keyword to search for", icon_logo="assets/logo.png")
        keyword = search_dialog.get_input()

        wanna_search = True
        while wanna_search:
            # IF CANCEL WAS CLICKED
            if keyword is None:
                self.resident_view_residents()
                return

            search_result = Resident_Management.search_resident(keyword)
            if len(search_result) == 0:
                wanna_search = messagebox.askyesno(f"No result for {keyword}", "Do you want to search again?")
                if not wanna_search:
                    self.clear_contents()
                    self.resident_view_residents()
                else:
                    self.resident_search_resident()
                    break
            else:
                self.resident_display_search_results(search_result)
                break
        
        Button_Ng_Inamo(self.bot_frame, text="Return", command=self.resident_view_residents).pack(padx=10, side='left')
        Button_Ng_Inamo(self.bot_frame, text="Search", command=self.resident_search_resident).pack(padx=0, side='right')

    def resident_display_search_results(self, search_result):
        header_frame = Frame_Ng_Inamo(self.content_frame)
        header_frame.configure(fg_color='black')
        header_frame.pack(fill='x')

        Label_Ng_Inamo(header_frame, text="ID", width=50, text_color='white', justify='left', anchor='w').grid(row=0, column=0, padx=10)
        Label_Ng_Inamo(header_frame, text="Last name", width=200, text_color='white', justify='left', anchor='w').grid(row=0, column=1)
        Label_Ng_Inamo(header_frame, text="First name", width=200, text_color='white', justify='left', anchor='w').grid(row=0, column=2)
        Label_Ng_Inamo(header_frame, text="Street", width=100, text_color='white', justify='left', anchor='w').grid(row=0, column=3)
        Label_Ng_Inamo(header_frame, text="House", width=90, text_color='white', justify='left', anchor='w').grid(row=0, column=4)
        Label_Ng_Inamo(header_frame, text="Phone", width=220, text_color='white', justify='left', anchor='w').grid(row=0, column=5)

        for index, record in enumerate(search_result, start=1):
            id, first_name, middle_initial, last_name, house_number, street, phone = record

            record_frame = Frame_Ng_Inamo(self.content_frame)
            record_frame.pack(pady=1, fill='both', expand=True)

            labels = [id, last_name, f"{first_name} {middle_initial}.", street, house_number, phone]

            for col, text in enumerate(labels):
                lb = Label_Ng_Inamo(record_frame, text=text, width=[50, 200, 200, 100, 90, 220][col], justify='left', anchor='w')
                lb.grid(row=index, column=col, padx=10 if col == 0 else 0)
                lb.bind("<Button-1>", lambda event, rec=record: self.resident_display_resident(event, rec))
                lb.bind("<Enter>", lambda event, fr=record_frame: self.resident_on_enter(event, fr))
                lb.bind("<Leave>", lambda event, fr=record_frame: self.resident_on_leave(event, fr))

    """ REPORT """
    def choose_date(self):
        self.chosen_date = Dialog_Ng_Inamo(text='Please choose the date for the report. Date should follow "YYYY/MM/DD" format', title='Choose Report Date', icon_logo='assets/logo.ico')
        date = self.chosen_date.get_input()

        if date == None:
            messagebox.showinfo(title="Invalid Date", message="Report generation was cancelled.")
            return

        #self.date_entry.bind("<<DateEntrySelected>>", self.on_date_change)
        self.check_records_existance(date)

        
    def check_records_existance(self, selected_date):
        # global top
        # Check if records exists
        ref = db.reference('waterLevels')

        if selected_date == "today":
            selected_date = datetime.now().strftime("%Y/%m/%d")

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

        if len(records) == 0:
            messagebox.showinfo("Invalid Date", f"There is no record for {selected_date}.")
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not file_path:
                messagebox.showinfo("Report Generation Cancelled", "Invalid path.")
                return
            
            Generate_Report.generate_report(records, selected_date, file_path)

        # Delay the destruction of the Toplevel window by 100 milliseconds
        #self.top_id = top.after(100, top.destroy)

    """ SYSTEM METHODS """
    def system_sms_template(self):
        self.content_title.configure(text="SMS TEMPLATE")
        self.clear_contents()

        rowframe = Frame_Ng_Inamo(self.content_frame)
        rowframe.pack(fill='x', expand=True, pady=0)
        low_label = Label_Ng_Inamo(rowframe, text="LOW", width=self.settings_label_width, justify=self.settings_label_justify, anchor=self.settings_label_anchor)
        low_label.pack(padx=10, side='left')
        low_entry = Textbox_Ng_Inamo(rowframe, height=self.sms_template_height)
        low_entry.pack(pady=self.texbox_pady, padx=self.texbox_padx, fill='x', expand=True, side='left')
        low_entry.bind("<Enter>", lambda event, wd=low_entry: self.textbox_on_enter(event, wd))
        low_entry.bind("<Leave>", lambda event, wd=low_entry: self.textbox_on_leave(event, wd))


        rowframe1 = Frame_Ng_Inamo(self.content_frame)
        rowframe1.pack(fill='x', expand=True, pady=5)
        normal_label = Label_Ng_Inamo(rowframe1, text="NORMAL", width=self.settings_label_width, justify=self.settings_label_justify, anchor=self.settings_label_anchor)
        normal_label.pack(padx=10, side='left')
        normal_entry = Textbox_Ng_Inamo(rowframe1, height=self.sms_template_height)
        normal_entry.pack(pady=self.texbox_pady, padx=self.texbox_padx, fill='x', expand=True, side='right')
        normal_entry.bind("<Enter>", lambda event, wd=normal_entry: self.textbox_on_enter(event, wd))
        normal_entry.bind("<Leave>", lambda event, wd=normal_entry: self.textbox_on_leave(event, wd))


        rowframe2 = Frame_Ng_Inamo(self.content_frame)
        rowframe2.pack(fill='x', expand=True, pady=0)
        high_label = Label_Ng_Inamo(rowframe2, text="HIGH", width=self.settings_label_width, justify=self.settings_label_justify, anchor=self.settings_label_anchor)
        high_label.pack(padx=10, side='left')
        high_entry = Textbox_Ng_Inamo(rowframe2, height=self.sms_template_height)
        high_entry.pack(pady=self.texbox_pady, padx=self.texbox_padx, fill='x', expand=True, side='left')
        high_entry.bind("<Enter>", lambda event, wd=high_entry: self.textbox_on_enter(event, wd))
        high_entry.bind("<Leave>", lambda event, wd=high_entry: self.textbox_on_leave(event, wd))


        rowframe3 = Frame_Ng_Inamo(self.content_frame)
        rowframe3.pack(fill='x', expand=True, pady=5)
        critical_label = Label_Ng_Inamo(rowframe3, text="CRITICAL", width=self.settings_label_width, justify=self.settings_label_justify, anchor=self.settings_label_anchor)
        critical_label.pack(padx=10, side='left')
        critical_entry = Textbox_Ng_Inamo(rowframe3, height=self.sms_template_height)
        critical_entry.pack(pady=self.texbox_pady, padx=self.texbox_padx, fill='x', expand=True, side='left')
        critical_entry.bind("<Enter>", lambda event, wd=critical_entry: self.textbox_on_enter(event, wd))
        critical_entry.bind("<Leave>", lambda event, wd=critical_entry: self.textbox_on_leave(event, wd))


        templates = System_Information.get_sms_templates()
        low_entry.insert('0.0', templates[0][1])
        normal_entry.insert('0.0', templates[1][1])
        high_entry.insert('0.0', templates[2][1])
        critical_entry.insert('0.0', templates[3][1])

        def system_save_sms():
            new_low = low_entry.get('0.0', 'end')
            new_normal = normal_entry.get('0.0', 'end')
            new_high = high_entry.get('0.0', 'end')
            new_critical = critical_entry.get('0.0', 'end')

            if (len(new_low) > 1) and (len(new_normal) > 1) and (len(new_high) > 1) and (len(new_critical) > 1):
                System_Information.update_sms_template(low=new_low, normal=new_normal, high=new_high, critical=new_critical)
            else:
                return

        Button_Ng_Inamo(self.bot_frame, text="Return", command=self.home_dashboard).pack(padx=10, side='left')
        Button_Ng_Inamo(self.bot_frame, text="Save", command=system_save_sms).pack(padx=0, side='right')

    def system_warning_levels(self):
        self.content_title.configure(text="WARNING LEVELS")
        self.clear_contents()
        
        rowframe = Frame_Ng_Inamo(self.content_frame)
        rowframe.pack(fill='x', expand=True, pady=0)
        low_label = Label_Ng_Inamo(rowframe, text="LOW", width=self.settings_label_width, justify=self.settings_label_justify, anchor=self.settings_label_anchor)
        low_label.pack(padx=10, side='left')
        low_entry = Entry_Ng_inamo(rowframe)
        low_entry.pack(pady=self.texbox_pady, padx=self.texbox_padx, fill='x', expand=True, side='left')


        rowframe1 = Frame_Ng_Inamo(self.content_frame)
        rowframe1.pack(fill='x', expand=True, pady=5)
        normal_label = Label_Ng_Inamo(rowframe1, text="NORMAL", width=self.settings_label_width, justify=self.settings_label_justify, anchor=self.settings_label_anchor)
        normal_label.pack(padx=10, side='left')
        normal_entry = Entry_Ng_inamo(rowframe1)
        normal_entry.pack(pady=self.texbox_pady, padx=self.texbox_padx, fill='x', expand=True, side='right')


        rowframe2 = Frame_Ng_Inamo(self.content_frame)
        rowframe2.pack(fill='x', expand=True, pady=0)
        high_label = Label_Ng_Inamo(rowframe2, text="HIGH", width=self.settings_label_width, justify=self.settings_label_justify, anchor=self.settings_label_anchor)
        high_label.pack(padx=10, side='left')
        high_entry = Entry_Ng_inamo(rowframe2)
        high_entry.pack(pady=self.texbox_pady, padx=self.texbox_padx, fill='x', expand=True, side='left')


        rowframe3 = Frame_Ng_Inamo(self.content_frame)
        rowframe3.pack(fill='x', expand=True, pady=5)
        critical_label = Label_Ng_Inamo(rowframe3, text="CRITICAL", width=self.settings_label_width, justify=self.settings_label_justify, anchor=self.settings_label_anchor)
        critical_label.pack(padx=10, side='left')
        critical_entry = Entry_Ng_inamo(rowframe3)
        critical_entry.pack(pady=self.texbox_pady, padx=self.texbox_padx, fill='x', expand=True, side='left')

        
        warning_levels = System_Information.get_warning_levels()
        low_entry.insert('0', warning_levels[0][1])
        normal_entry.insert('0', warning_levels[1][1])
        high_entry.insert('0', warning_levels[2][1])
        critical_entry.insert('0', warning_levels[3][1])

        def system_save_warning():
            new_low = low_entry.get()
            new_normal = normal_entry.get()
            new_high = high_entry.get()
            new_critical = critical_entry.get()

            if Input_Validation.validate_water_level(new_low) == False: return
            if Input_Validation.validate_water_level(new_normal) == False: return
            if Input_Validation.validate_water_level(new_high) == False: return
            if Input_Validation.validate_water_level(new_critical) == False: return

            System_Information.update_warning_levels(low=new_low, normal=new_normal, high=new_high, critical=new_critical)

        Button_Ng_Inamo(self.bot_frame, text="Return", command=self.home_dashboard).pack(padx=10, side='left')
        Button_Ng_Inamo(self.bot_frame, text="Save", command=system_save_warning).pack(padx=0, side='right')

    """ MY ACCOUNT """
    def account_my_account(self):
        self.content_title.configure(text="ACCOUNT INFO")
        self.clear_contents()
        
        self.acc = Account.get_account_details(id=self.logged_in_accound_id)

        left_frame = Frame_Ng_Inamo(self.content_frame)
        left_frame.pack(side='left', fill='both', expand=True)

        Frame1 = Frame_Ng_Inamo(left_frame, fg_color='transparent')
        Frame1.pack(fill='x')
        Label_Ng_Inamo(Frame1, text='\nFirstname').pack(padx=20, pady=5, side='left')
        fname_entry = Entry_Ng_inamo(left_frame)
        fname_entry.pack(padx=20, pady=5, fill='x')

        Frame2 = Frame_Ng_Inamo(left_frame)
        Frame2.pack(fill='x')
        Label_Ng_Inamo(Frame2, text='\nMiddle Initial').pack(padx=20, pady=5, side='left')
        initial_entry = Entry_Ng_inamo(left_frame)
        initial_entry.pack(padx=20, pady=5, fill='x')

        Frame3 = Frame_Ng_Inamo(left_frame)
        Frame3.pack(fill='x')
        Label_Ng_Inamo(Frame3, text='\nLast Name').pack(padx=20, pady=5, side='left')
        lname_entry = Entry_Ng_inamo(left_frame)
        lname_entry.pack(padx=20, pady=5, fill='x')



        right_frame = Frame_Ng_Inamo(self.content_frame)
        right_frame.pack(side='right', fill='both', expand=True)

        Frame4 = Frame_Ng_Inamo(right_frame)
        Frame4.pack(fill='x')
        Label_Ng_Inamo(Frame4, text='\nEmail').pack(padx=20, pady=5, side='left')
        self.email_entry = Entry_Ng_inamo(right_frame)
        self.email_entry.pack(padx=20, pady=5, fill='x')

        Frame5 = Frame_Ng_Inamo(right_frame)
        Frame5.pack(fill='x')
        Label_Ng_Inamo(Frame5, text='\nPhone').pack(padx=20, pady=5, side='left')
        self.phone_entry = Entry_Ng_inamo(right_frame)
        self.phone_entry.pack(padx=20, pady=5, fill='x')
        
        Frame6 = Frame_Ng_Inamo(right_frame)
        Frame6.pack(fill='x')
        Label_Ng_Inamo(Frame6, text='\nPassword').pack(padx=20, pady=5, side='left')
        self.new_pass_entry = Entry_Ng_inamo(right_frame)
        self.new_pass_entry.pack(padx=20, pady=5, fill='x')

        fname_entry.insert("0", self.acc[1])
        initial_entry.insert("0", self.acc[2])
        lname_entry.insert("0", self.acc[3])
        self.phone_entry.insert("0", self.acc[4])
        self.email_entry.insert("0", self.acc[5])

        # BUTTONS
        Button_Ng_Inamo(self.bot_frame, text="Change Phone", command=self.account_change_phone).pack(padx=10, side='left')
        Button_Ng_Inamo(self.bot_frame, text="Change Password", command=self.account_change_password).pack(padx=0, side='right')

    def account_logout(self):
        self.logged_in_accound_id = 0
        self.destroy()
        new = MainWindow()
        new.show_login_window()

    def account_change_phone(self):
        if Input_Validation.validate_phone(self.phone_entry.get()):
            wanna_change_phone = messagebox.askyesno(title="Change Phone", message="Do you want to change your phone number?")
            if wanna_change_phone:
                Account.change_phone(id=self.logged_in_accound_id, new_phone=self.phone_entry.get())
                messagebox.showinfo(title="Phone Change", message="Recovery phone was changed successfully.")
            else:
                messagebox.showinfo(title="Phone Change Cancelled", message="Recovery phone was not changed.")

    def account_change_password(self):
        pass_input = Dialog_Ng_Inamo(title="Confirm Password", text="Enter your old password", icon_logo="assets/logo.png")
        my_password = pass_input.get_input()

        if my_password is None:
            messagebox.showinfo(title='Password Change Cancelled', message='Password change was cancelled.')
            return

        curr_pword = my_password
        checker = Account.check_credentials(uname=self.acc[5], pword=curr_pword) # str(ID) / None
        
        if checker is not None:
            Account.change_password(id=checker, new_password=self.new_pass_entry.get())
            self.new_pass_entry.delete('0', 'end')
            messagebox.showinfo("Password Change", "Password changed successfully.")
        else:
            messagebox.showerror("Password Error", "Current password is not correct.")

    """ SECRET """
    def show_login_window(self):
        """" Show register window if account is empty,
        Else, Show log in window """
        if Account.is_empty():
            self.register_window = Register_Window.RegisterWindow(self)
            self.register_window.mainloop()

        self.login_window = Login_Window.LoginWindow(self)
        self.login_window.mainloop()

    def show_main_window(self):
        #try:
        self.home_dashboard()
        #except:
        #    self.clear_contents()
        #    Label_Ng_Inamo(self.content_frame, text="Cannot connect to the database...").pack()

        self.mainloop()

    def home_dashboard(self):
        self.clear_contents()

        #self.display_graph()
        self.display_logo()
        pass

    def display_logo(self):
        from PIL import Image
        from PIL import ImageTk

        self.content_title.configure(text="Home")
        self.clear_contents()

        self.icon_frame = Frame_Ng_Inamo(self.content_frame)
        self.icon_frame.pack(padx=20, pady=10, fill='both', expand=True)


        self.image = CTkImage(light_image=Image.open('assets/logo_detailed.png'), size=(200, 200))

        self.image_widget = Label_Ng_Inamo(self.icon_frame, image=self.image, text=" ")
        self.image_widget.pack(fill='both', expand=True)

        self.image_description_label = Label_Ng_Inamo(self.icon_frame, text="DI KAYA I PROMT KAY CHATGPT")
        self.image_description_label.pack()


    def clear_contents(self):
        try:
            self.after_cancel(self.after_id)
        except:
            pass
            
        try:
            self.after_cancel(self.top_id)
        except:
            pass

        for child in self.bot_frame.winfo_children() + self.content_frame.winfo_children(): child.destroy()
            
    def resident_on_enter(self, event, frame):
        frame.configure(fg_color=self.hover_in_fill)

    def resident_on_leave(self, event, frame):
        frame.configure(fg_color='transparent')

    def textbox_on_enter(self, event, widget):
        # No
        #widget.configure(height=self.sms_expanded_height)
        return
        
    def textbox_on_leave(self, event, widget):
        # No
        #widget.configure(height=self.sms_template_height)
        return
if __name__ == "__main__":
    print()
    try:
        root = MainWindow()
        root.show_login_window()
    except KeyboardInterrupt:
        exit(1)
    except:
        exit(1)