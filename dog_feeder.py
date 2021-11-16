#import RPi.GPIO as GPIO
import time
import tkinter
from datetime import datetime

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(2, GPIO.OUT)

# while True:
#     GPIO.output(2, True)
#     time.sleep(0.01)
#     GPIO.output(2, False)
#     time.sleep(0.01)

TIME_RUN = 10

class Dog_feeder:
    def __init__(self, master):
        self.master = master
        #set de main frame as a white window for the master objetct (root)
        self.mainframe = tkinter.Frame(self.master, bg='#d9d9d9') #d9d9d9
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
        self.time_running = tkinter.IntVar()
        self.time_running.set(TIME_RUN)

        # Hour preset variables
        self.entry1 = tkinter.StringVar()
        self.entry2 = tkinter.StringVar()
        self.entry3 = tkinter.StringVar()


        # calling the methods created below
        self.build_grid()
        self.build_banner()
        self.build_presets()
        self.build_buttons()
        self.build_time()
        self.update_time()
        self.update_message()
        self.check_presets()


    def build_grid(self):
        #build 1 column and 4 lines (top, middle, bottom) + message
        # Weight = 1 autoadjust
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=0) # Banner
        self.mainframe.rowconfigure(1, weight=0) # Time
        self.mainframe.rowconfigure(2, weight=1) # Presets
        self.mainframe.rowconfigure(3, weight=0) # Buttons
        self.mainframe.rowconfigure(4, weight=0) # Message

    def build_banner(self):
        # build a banner in the mainframe
        banner = tkinter.Label(
            self.mainframe,
            bg='#0a1e6e',
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


    def build_time(self, *args):
        time = tkinter.Label(
            self.mainframe,
            text=self.time_now.get(),
            font=('Helvetica', 20),
        )
        time.grid(row=1, column=0, sticky='nsew')

    def build_presets(self):
        presets_frame = tkinter.Frame(self.mainframe)
        presets_frame.grid(row=2, column=0, sticky='we', padx=10, pady=10)
        presets_frame.columnconfigure(0, weight=0)
        presets_frame.columnconfigure(1, weight=0)

        self.preset1 = tkinter.Entry(presets_frame, textvariable=self.entry1, font=('Helvetica',12,'normal'), justify='center', width=10)
        self.preset2 = tkinter.Entry(presets_frame, textvariable=self.entry2, font=('Helvetica',12,'normal'), justify='center', width=10)
        self.preset3 = tkinter.Entry(presets_frame, textvariable=self.entry3, font=('Helvetica',12,'normal'), justify='center', width=10)

        padx = 40
        tkinter.Label(presets_frame, text="Programa 1:", justify='right').grid(row=0, padx=padx)
        tkinter.Label(presets_frame, text="Programa 2:", justify='right').grid(row=1, padx=padx)
        tkinter.Label(presets_frame, text="Programa 3:", justify='right').grid(row=2, padx=padx)
        padx = 0
        pady = 30
        self.preset1.grid(row=0, column=1, sticky='nswe', padx=padx, pady=pady)
        self.preset2.grid(row=1, column=1, sticky='nswe', padx=padx, pady=pady)
        self.preset3.grid(row=2, column=1, sticky='nswe', padx=padx, pady=pady)


    def build_buttons(self):
        #build a new frame inside de mainframe:
        buttuns_frame = tkinter.Frame(self.mainframe)
        # put the buttuns frame into the original grid, line 2
        buttuns_frame.grid(row=3, column=0, sticky='nswe', padx=10, pady=10)
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


    def check_presets(self):
        try:
            now = datetime.now()

            # Check is all 5 digits were typed =>  12 : 00
            if len(self.entry1.get()) == 5:
                # Convert the string from the input for datetime format
                entry1_datetime = datetime.strptime(self.entry1.get(), "%H:%M")
                # Check if the preset is equal to current time (hour and minute), so run start_callback
                if entry1_datetime.hour == now.hour and entry1_datetime.minute == now.minute:
                    self.start_callback()
                    # time_running decreases continuously, so stop_callback when it crosses the zero
                    if self.time_running.get() < 0:
                        self.stop_callback()
                    # When it crosses the next minute, it reset the counter
                    if self.time_running.get() == -60 + TIME_RUN:
                        self.time_running.set(TIME_RUN)

            # Check is all 5 digits were typed =>  12 : 00
            if len(self.entry2.get()) == 5:
                # Convert the string from the input for datetime format
                entry2_datetime = datetime.strptime(self.entry2.get(), "%H:%M")
                # Check if the preset is equal to current time (hour and minute), so run start_callback
                if entry2_datetime.hour == now.hour and entry2_datetime.minute == now.minute:
                    self.start_callback()
                    # time_running decreases continuously, so stop_callback when it crosses the zero
                    if self.time_running.get() < 0:
                        self.stop_callback()
                    # When it crosses the next minute, it reset the counter
                    if self.time_running.get() == -60 + TIME_RUN:
                        self.time_running.set(TIME_RUN)

            # Check is all 5 digits were typed =>  12 : 00
            if len(self.entry3.get()) == 5:
                # Convert the string from the input for datetime format
                entry3_datetime = datetime.strptime(self.entry3.get(), "%H:%M")
                # Check if the preset is equal to current time (hour and minute), so run start_callback
                if entry3_datetime.hour == now.hour and entry3_datetime.minute == now.minute:
                    self.start_callback()
                    # time_running decreases continuously, so stop_callback when it crosses the zero
                    if self.time_running.get() < 0:
                        self.stop_callback()
                    # When it crosses the next minute, it reset the counter
                    if self.time_running.get() == -60 + TIME_RUN:
                        self.time_running.set(TIME_RUN)

        except ValueError:
            pass

        self.master.after(1000, self.check_presets)

    def start_callback(self):
        self.running = True
        time_left = self.time_running.get()
        self.time_running.set(time_left-1)

    def stop_callback(self):
        self.running = False


    def write_message(self, *args):
        message = tkinter.Label(
            self.mainframe,
            text=self.message.get(),
            font=('Helvetica, 12'),
        )
        message.grid(row=4, column=0, sticky='nswe')


    def update_time(self):
        self.time_now.set(datetime.strftime(datetime.now(), '%H:%M:%S'))
        self.master.after(500, self.update_time)

    def update_message(self):
        if self.running:
            self.message.set(f"Alimentando... {self.time_running.get()+1}")
            self.stop_button.config(state=tkinter.ACTIVE)
        else:
            self.message.set("")

        self.master.after(500, self.update_message)

if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry("400x600")
    Dog_feeder(root)
    root.mainloop()
