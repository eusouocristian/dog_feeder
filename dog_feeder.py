#import RPi.GPIO as GPIO
import time
import tkinter
from tkinter import messagebox
from datetime import datetime

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(2, GPIO.OUT)

# while True:
#     GPIO.output(2, True)
#     time.sleep(0.01)
#     GPIO.output(2, False)
#     time.sleep(0.01)


class Dog_feeder:
    def __init__(self, master):
        self.master = master
        #set de main frame as a white window for the master objetct (root)
        self.mainframe = tkinter.Frame(self.master, bg='white')
        self.mainframe.pack(fill=tkinter.BOTH, expand=True)
        self.mainframe.winfo_toplevel().title("Alimentador canino automático")

        self.message = tkinter.StringVar()
        self.message.trace('w', self.write_message)

        # create a string variable tu be used inside the Label of build_timer()
        self.time_now = tkinter.StringVar()
        #reconstroi o timer na janela sempre que a variavel for alterada
        self.time_now.trace('w', self.build_time)

        # create a flag to check if the clock is running or not, default is False
        self.running = False

        # calling the methods created below
        self.build_grid()
        self.build_banner()
        self.build_buttons()
        self.build_time()
        self.update()

    def build_grid(self):
        #build 1 column and 4 lines (top, middle, bottom) + message
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=0) # top line
        self.mainframe.rowconfigure(1, weight=1) # middle line
        self.mainframe.rowconfigure(2, weight=0) # bottom line
        self.mainframe.rowconfigure(3, weight=1) # message line

    def build_banner(self):
        # build a banner in the mainframe
        banner = tkinter.Label(
            self.mainframe,
            bg='red',
            fg='white',
            text='Alimentador Automático',
            font=('Helvetica', 24)
        )
        # put the banner on the grid
        banner.grid(
            row=0, column=0, # set the position on the created grid
            sticky='we', # 'we' -> west-east, or 'ns' -> north-south, 'nsew' -> north-shouth/east-west
            padx=10, pady=10
        )

    def build_buttons(self):
        #build a new frame inside de mainframe:
        buttuns_frame = tkinter.Frame(self.mainframe)
        # put the buttuns frame into the original grid, line 2
        buttuns_frame.grid(row=2, column=0, sticky='nswe', padx=10, pady=10)
        # create two columns to put each button
        buttuns_frame.columnconfigure(0, weight=1)
        buttuns_frame.columnconfigure(1, weight=1)

        # create buttons itself
        self.start_button = tkinter.Button(
            buttuns_frame, text='Start',
            command=self.start_callback
        )
        self.stop_button = tkinter.Button(
            buttuns_frame, text='Stop',
            command=self.stop_callback
        )

        # set the buttons position
        self.start_button.grid(row=0, column=0, sticky='ew')
        self.stop_button.grid(row=0, column=1, sticky='ew')
        #set the inicial condicion for stop button as DISABLED
        self.stop_button.config(state=tkinter.DISABLED)

    def build_time(self, *args):
        time = tkinter.Label(
            self.mainframe,
            text=self.time_now.get(),
            font=('Helvetica', 36),
        )
        time.grid(row=1, column=0, sticky='nsew')

    def start_callback(self):
        self.running = True
        return True

    def stop_callback(self):
        self.running = False
        return True

    def write_message(self, *args):
        message = tkinter.Label(
            self.mainframe,
            text=self.message.get(),
            font=('Helvetica, 22'),
        )
        message.grid(row=3, column=0, sticky='nsew')

    def update(self):
        self.time_now.set(datetime.strftime(datetime.now(), '%H:%M:%S'))
        if self.running:
            self.message.set("Alimentando... ")
            self.stop_button.config(state=tkinter.ACTIVE)
        else:
            self.message.set("")

        # method to run self.update after 1000ms
        self.master.after(500, self.update)



if __name__ == '__main__':
    root = tkinter.Tk()
    Dog_feeder(root)
    root.mainloop()
