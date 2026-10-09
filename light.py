import tkinter as tk
from PIL import Image, ImageTk  # Optional, for PNG/JPG support
import time

# Initialize the main window
root = tk.Tk()
root.title("Tkinter Canvas Example")
root.geometry("600x500")

# 1. Create the Canvas widget
# Coordinates in Canvas start at (0,0) in the top-left corner
canvas = tk.Canvas(root, width=550, height=400, bg="white")
canvas.pack(pady=20)

# Load the image (keep a reference to prevent garbage collection!)
# Use tk.PhotoImage(file="image.png") for GIF/PNG natively
red_light = ImageTk.PhotoImage(Image.open("red_light.jpg"))
canvas.image = red_light  # Critical reference

# Add image to canvas (x=200, y=150)
red_light_id = canvas.create_image(275, 200, anchor="center", image=red_light)


yellow_light = ImageTk.PhotoImage(Image.open("yellow_light.jpg"))
canvas.image = red_light  # Critical reference

# Add image to canvas (x=200, y=150)
yellow_light_id = canvas.create_image(275, 200, anchor="center", image=yellow_light)

green_light = ImageTk.PhotoImage(Image.open("green_light.jpg"))
canvas.image = green_light  # Critical reference

# Add image to canvas (x=200, y=150)
green_light_id = canvas.create_image(275, 200, anchor="center", image=green_light)


canvas.itemconfigure(green_light_id, state='hidden')
canvas.itemconfigure(yellow_light_id, state='hidden')



'''
# 2. Draw basic shapes on the Canvas

# Draw a blue line: create_line(x0, y0, x1, y1, options)
canvas.create_line(50, 50, 200, 50, fill="blue", width=3)

# Draw a red rectangle: create_rectangle(x0, y0, x1, y1, options)
canvas.create_rectangle(50, 100, 200, 200, fill="red", outline="black", width=2)

# Draw a yellow circle/oval: create_oval(x0, y0, x1, y1, options)
# (Coordinates define the bounding box that encloses the oval)
canvas.create_oval(300, 50, 450, 200, fill="yellow", outline="orange", width=4)

# Draw a polygon (Triangle): create_polygon(x0, y0, x1, y1, x2, y2, options)
canvas.create_polygon(125, 250, 50, 350, 200, 350, fill="green", outline="black")

# Add text: create_text(x, y, options)
canvas.create_text(375, 250, text="Hello Tkinter!", font=("Arial", 16, "bold"), fill="purple")

# 3. Add simple interactivity
# Define a callback function for a mouse click event
def on_canvas_click(event):
    # event.x and event.y give the precise pixel coordinates of the click
    canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="black")
    print(f"Clicked at coordinates: X={event.x}, Y={event.y}")

# Bind the left mouse click (<Button-1>) to the canvas
canvas.bind("<Button-1>", on_canvas_click)
'''


# Start the application event loop
root.mainloop()