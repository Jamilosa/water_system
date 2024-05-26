import tkinter as tk
from PIL import Image, ImageTk

# Initialize the main window
root = tk.Tk()
root.title("Tkinter Image Example")

# Load and resize the image using PIL
image_path = "assets/logo_detailed.png"
image = Image.open(image_path)
new_width, new_height = 200, 200  # New dimensions
image = image.resize((new_width, new_height), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

# Create a Label widget to display the image
label = tk.Label(root, image=photo)
label.pack()

# Run the application
root.mainloop()