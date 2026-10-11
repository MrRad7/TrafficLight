#!/usr/bin/env python3

""" Read 10 coils and print result on stdout. """

import logging
import queue
import threading
import time
import tkinter as tk

from PIL import Image, ImageTk  # Optional, for PNG/JPG support
from pyModbusTCP.client import ModbusClient

#elements for controller 
RED = 0  #QX0.0
YELLOW = 1  #QX0.1
GREEN = 2  #QX0.2

POLLING_TIME = 1 #time in seconds between reads

LOG_LEVEL = 'DEBUG'

q = queue.Queue(maxsize=10)

def set_logging(level: str):
    '''Change the logging level at runtime.''' 
    # set debug level for pyModbusTCP.client to see frame exchanges
    numeric_level = getattr(logging, LOG_LEVEL.upper(), None)
    logging.basicConfig()
    #logging.getLogger('pyModbusTCP.client').setLevel(logging.DEBUG)
    if isinstance(numeric_level, int):
        logging.getLogger().setLevel(numeric_level)
    else:
        raise TypeError(f"Invalid log level: {level}")


def connect_to_plc(host='localhost', port=502) -> ModbusClient:
    '''Connect to the PLC returning a modbus client'''
    try:
        c = ModbusClient(host='localhost', port=502, timeout=10, auto_open=True, auto_close=False)
    except ValueError:
        raise ValueError("Error with host or port parameters.")
    
    return c


def read_coils(c: ModbusClient) -> list:
    '''Read coils from the PLC returning a list of values.'''
    # read 10 bits (= coils) at address 0, store result in coils list
    try:
        coils_l = c.read_coils(0, 10)
    except TypeError as e:
        raise e("Could not read.")
        
    return coils_l


def process_coils(coils_l: list) -> int:
    '''Process all of the values in the coils list.'''
    if coils_l:
        if LOG_LEVEL == 'DEBUG':
            print(f"coil ad #0 to 9: {coils_l}")
        if coils_l[RED]:
            #print("RED")
            q.put("RED")
        elif coils_l[YELLOW]:
            #print("YELLOW")
            q.put("YELLOW")
        elif coils_l[GREEN]:
            #print("GREEN")
            q.put("GREEN")
    else:
        print('Unable to read coils, retrying.')
        
    return 0


t = None
def gui_thread():
    global t
    
    def show_color(color):
        if color == 'GREEN':
            canvas.itemconfigure(yellow_light_id, state='hidden')
            canvas.itemconfigure(red_light_id, state='hidden')
            canvas.itemconfigure(green_light_id, state='normal')
        elif color == 'YELLOW':
            canvas.itemconfigure(yellow_light_id, state='normal')
            canvas.itemconfigure(red_light_id, state='hidden')
            canvas.itemconfigure(green_light_id, state='hidden')
        else: #RED
            canvas.itemconfigure(yellow_light_id, state='hidden')
            canvas.itemconfigure(red_light_id, state='normal')
            canvas.itemconfigure(green_light_id, state='hidden')
            
        return 0
    
    
    def timertick():
        try:
            value = q.get_nowait()
        except queue.Empty:
            pass
        else:
            value = q.get()
            #print(f"Something in queue: {value}")
            show_color(value)
            
        t.after(500, timertick)
        return 0
    
        
    #setup graphics
    # Initialize the main window
    t = tk.Tk()
    t.title("Tkinter Canvas Example")
    t.geometry("600x500")

    # 1. Create the Canvas widget
    # Coordinates in Canvas start at (0,0) in the top-left corner
    canvas = tk.Canvas(t, width=550, height=400, bg="white")
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
    
    timertick()
    t.mainloop()
    
    


if __name__ == "__main__":
    set_logging(LOG_LEVEL)
    
    # init modbus client - it will auto-reconnect
    c = connect_to_plc()
    
        
    print(f"Ctype: {type(c)}")
    #print(f"open: {c.is_open}")
    
    
    #thread.start_new_thread(gui_thread, ())
    thread1 = threading.Thread(target=gui_thread)
    thread1.daemon = True
    thread1.start()
    
    # main read loop
    while True:
        #print(f"open: {c.is_open}")     
        
        coils_l = read_coils(c)    
        
        process_coils(coils_l)
                
        # sleep 1s before next polling
        time.sleep(POLLING_TIME)

    
    thread1.join()