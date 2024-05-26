import tkinter as tk
from tkinter import *
from tkinter import simpledialog
import customtkinter as ctk


_title_font = ('Segoe UI', 20)
_normal_font = ('Segoe UI', 15)


""" LABEL AND BUTTON """
_entry_border_color = '#212121'
_entry_border_width = 2
_entry_border_radius = 5
_entry_box_color = '#efefef'

_button_border_width = 0
_button_border_radius = 5


ctk.set_appearance_mode('light')

""" FRAME """
class Frame_Ng_Inamo(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent'
                       )


""" ENTRY """
class Entry_Ng_inamo(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(border_color = _entry_border_color,
                       border_width= _entry_border_width,
                       corner_radius=_entry_border_radius,
                       fg_color = _entry_box_color,
                       font = _normal_font
                       )
        
class Textbox_Ng_Inamo(ctk.CTkTextbox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(border_color = _entry_border_color,
                       border_width = _entry_border_width,
                       corner_radius = _entry_border_radius, 
                       fg_color = _entry_box_color,
                       font = _normal_font
                       )


""" LABEL AND BUTTON """
class Label_Ng_Inamo(ctk.CTkLabel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent',
                       bg_color='transparent',
                       font = _normal_font
                       )
        
class Button_Ng_Inamo(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(border_color = 'black',
                       border_width=_button_border_width,
                       corner_radius=_button_border_radius,
                       font = _normal_font
                       )


class Dialog_Ng_Inamo(ctk.CTkInputDialog):
    def __init__(self, master=None, icon_logo=None, **kwargs):
        super().__init__(master, **kwargs)
        if not icon_logo:
            self.iconbitmap(icon_logo)


    

if __name__ == '__main__':
    root = ctk.CTk()
    
    Button_Ng_Inamo(root, text='Button ng INAMO').pack(padx=10, pady=10)

    entry = Entry_Ng_inamo(root)
    entry.pack(padx=10, pady=10)
    entry.insert('0', 'Entry ng INAMO')

    textbox = Textbox_Ng_Inamo(root)
    textbox.pack(padx=10, pady=10)
    textbox.insert('0.0', 'Textbox ng INAMO')

    label = Label_Ng_Inamo(root, text='Label ng INAMO')
    label.pack(padx=10, pady=10)
    
    root.mainloop()