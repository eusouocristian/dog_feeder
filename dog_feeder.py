import RPi.GPIO as GPIO
import sqlite3
import tkinter
from tkinter import messagebox
from datetime import datetime
import manage_db

PWM_FREQ = 1000
STEP_PIN = 18
EN_PIN = 15
TIME_RUN = 10

BANNER_LINE = 0
CLOCK_LINE = 1
FREQ_LINE = 2
RT_LINE = 3
PRESETS_LINE = 4
SAVE_LINE = 5
BUTTONS_LINE = 6
MESSAGE_LINE = 7

DATABASE = 'programas.db'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(STEP_PIN, GPIO.OUT) # step
GPIO.setup(EN_PIN, GPIO.OUT) # Enable
GPIO.output(EN_PIN, 1) # Disable with 1

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
        self.time_now.trace('w', self.build_clock)

        # create a flag to check if the clock is running or not, default is False
        self.running = False
        self.time_running = tkinter.IntVar()
        self.time_running.set(TIME_RUN)

        # Hour preset variables
        self.entry1 = tkinter.StringVar()
        self.entry2 = tkinter.StringVar()
        self.entry3 = tkinter.StringVar()

        self.pwm = GPIO.PWM(STEP_PIN, PWM_FREQ) # Create PWM
        self.pwm.start(50) # Duty 50%
        self.freq_entry = tkinter.StringVar()
        
        # Value in sec for driving the motor when active
        self.rt_value = tkinter.StringVar()

        # calling the methods created below
        self.build_grid()
        self.build_banner()
        self.build_presets()
        self.build_buttons()
        self.build_save_button()
        self.build_clock()
        self.update_clock()
        self.update_message()
        self.check_presets()
        self.build_freq()
        self.build_running_time()

    def build_grid(self):
        #build 1 column and 4 lines (top, middle, bottom) + message
        # Weight = 1 autoadjust
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(BANNER_LINE, weight=0) # Banner
        self.mainframe.rowconfigure(CLOCK_LINE, weight=0) # Clock
        self.mainframe.rowconfigure(PRESETS_LINE, weight=1) # Presets
        self.mainframe.rowconfigure(BUTTONS_LINE, weight=0) # Start/Stop Buttons
        self.mainframe.rowconfigure(SAVE_LINE, weight=0) # Save prog Button
        self.mainframe.rowconfigure(MESSAGE_LINE, weight=0) # Message

    def build_banner(self):
        # build a banner in the mainframe
        banner = tkinter.Label(
            self.mainframe,
            bg='#0a1e6e',
            fg='white',
            text='Alimentador Automático',
            font=('Calibre', 20),
        )
        # put the banner on the grid
        banner.grid(
            row=BANNER_LINE, column=0, # set the position on the created grid
            sticky='we', # 'we' -> west-east, or 'ns' -> north-south, 'nsew' -> north-shouth/east-west
            padx=10, pady=10
        )

    def build_freq(self):
        freq_frame = tkinter.Frame(self.mainframe)
        freq_frame.grid(row=FREQ_LINE, column=0, sticky='we', padx=10, pady=10)
        freq_frame.columnconfigure(0, weight=0)
        freq_frame.columnconfigure(1, weight=0)

        self.preset_freq = tkinter.Entry(freq_frame, textvariable=self.freq_entry, font=('Monospace',12,'normal'), justify='center', width=10)

        padx = 42
        tkinter.Label(freq_frame, text="Pulsos/seg:", justify='right').grid(row=0, padx=padx)

        padx = 0
        pady = 10
        self.preset_freq.grid(row=0, column=1, sticky='nswe', padx=padx, pady=pady)

        prog_from_db = self.get_prog()
        freq_from_db = prog_from_db[0][5]
        self.preset_freq.insert(-1, freq_from_db)


    def build_running_time(self):
        rt_frame = tkinter.Frame(self.mainframe)
        rt_frame.grid(row=RT_LINE, column=0, sticky='we', padx=10, pady=10)
        rt_frame.columnconfigure(0, weight=0)
        rt_frame.columnconfigure(1, weight=0)

        self.rt_entry = tkinter.Entry(rt_frame, textvariable=self.rt_value, font=('Monospace',12,'normal'), justify='center', width=10)

        padx = 33
        tkinter.Label(rt_frame, text="Tempo acion.:", justify='right').grid(row=0, padx=padx)

        padx = 0
        pady = 0
        self.rt_entry.grid(row=0, column=1, sticky='nswe', padx=padx, pady=pady)

        prog_from_db = self.get_prog()
        rt_from_db = prog_from_db[0][6]
        self.rt_entry.insert(-1, rt_from_db)


    def build_clock(self, *args):
        time = tkinter.Label(
            self.mainframe,
            text=self.time_now.get(),
            font=('Calibre', 20),
        )
        time.grid(row=CLOCK_LINE, column=0, sticky='nsew')

    def build_presets(self):
        presets_frame = tkinter.Frame(self.mainframe)
        presets_frame.grid(row=PRESETS_LINE, column=0, sticky='we', padx=10, pady=10)
        presets_frame.columnconfigure(0, weight=0)
        presets_frame.columnconfigure(1, weight=0)

        self.preset1 = tkinter.Entry(presets_frame, textvariable=self.entry1, font=('Monospace',12,'normal'), justify='center', width=10)
        self.preset2 = tkinter.Entry(presets_frame, textvariable=self.entry2, font=('Monospace',12,'normal'), justify='center', width=10)
        self.preset3 = tkinter.Entry(presets_frame, textvariable=self.entry3, font=('Monospace',12,'normal'), justify='center', width=10)

        padx = 40
        tkinter.Label(presets_frame, text="Programa 1:", justify='right').grid(row=0, padx=padx)
        tkinter.Label(presets_frame, text="Programa 2:", justify='right').grid(row=1, padx=padx)
        tkinter.Label(presets_frame, text="Programa 3:", justify='right').grid(row=2, padx=padx)
        padx = 0
        pady = 30
        self.preset1.grid(row=0, column=1, sticky='nswe', padx=padx, pady=pady)
        self.preset2.grid(row=1, column=1, sticky='nswe', padx=padx, pady=pady)
        self.preset3.grid(row=2, column=1, sticky='nswe', padx=padx, pady=pady)

        prog_from_db = self.get_prog()
        p1_from_db = prog_from_db[0][2]
        p2_from_db = prog_from_db[0][3]
        p3_from_db = prog_from_db[0][4]
        self.preset1.insert(-1, p1_from_db)
        self.preset2.insert(-1, p2_from_db)
        self.preset3.insert(-1, p3_from_db)

    def build_save_button(self):
        save_frame = tkinter.Frame(self.mainframe)
        save_frame.grid(row=SAVE_LINE, column=0, sticky='nswe', padx=10, pady=30)
        save_frame.columnconfigure(0, weight=1)
        self.save_button = tkinter.Button(save_frame, text='Salvar Programas', command=self.save_prog)
        self.save_button.grid(row=0, column=0)

    def build_buttons(self):
        #build a new frame inside de mainframe:
        buttuns_frame = tkinter.Frame(self.mainframe)
        # put the buttuns frame into the original grid, line 2
        buttuns_frame.grid(row=BUTTONS_LINE, column=0, sticky='nswe', padx=10, pady=10)
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
                    time_left = self.time_running.get()
                    self.time_running.set(time_left-1)
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
                    time_left = self.time_running.get()
                    self.time_running.set(time_left-1)
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
                    time_left = self.time_running.get()
                    self.time_running.set(time_left-1)
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

    def stop_callback(self):
        self.running = False


    def write_message(self, *args):
        message = tkinter.Label(
            self.mainframe,
            text=self.message.get(),
            font=('Calibre, 12'),
        )
        message.grid(row=MESSAGE_LINE, column=0, sticky='nswe')


    def update_clock(self):
        self.time_now.set(datetime.strftime(datetime.now(), '%H:%M:%S'))
        self.master.after(500, self.update_clock)

    def update_message(self):
        if self.running:
            self.message.set(f"Alimentando... {self.time_running.get()+1}")
            self.drive_motor(enable=True)
            self.stop_button.config(state=tkinter.ACTIVE)
        else:
            self.message.set("")
            self.drive_motor(enable=False)

        self.master.after(500, self.update_message)


    def save_prog(self):
        conn = manage_db.create_connection(DATABASE)
        data_to_insert = [datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S'),
                          self.entry1.get(),
                          self.entry2.get(),
                          self.entry3.get(),
                          self.freq_entry.get(),
                          self.rt_entry.get(),
                          ]
        ids = manage_db.insert_prog(conn, data_to_insert)
        print(ids)
        if ids:
            messagebox.showinfo('Sucesso', 'Dados de programação salvos com sucesso!')
        return ids


    def get_prog(self):
        conn = manage_db.create_connection(DATABASE)
        return manage_db.get_last_prog(conn)
    
    
    def drive_motor(self, enable=False):
        if enable:
            GPIO.output(EN_PIN, 0) # Disable with 1
            self.pwm.ChangeFrequency(int(self.freq_entry.get()))
        else:
            GPIO.output(EN_PIN, 1) # Disable with 1

if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry("400x700")
    Dog_feeder(root)
    root.mainloop()
