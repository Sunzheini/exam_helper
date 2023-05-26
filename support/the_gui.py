import threading
from tkinter import *

from support.aopen_ai_controller import OpenAIGenerator
from support.camera_controller import Camera


class ExamHelperGui:
    def __init__(self):
        self.window = Tk()
        self.window.title("Exam Helper GUI")
        self.window.eval("tk::PlaceWindow . center")
        x = self.window.winfo_screenwidth() // 2
        y = int(self.window.winfo_screenheight() * 0.2)
        self.window.geometry('300x300+' + str(x) + '+' + str(y))
        self.window.config(background='#2b2828')

        self.api_key = None
        self.generator = None
        self.camera = None

# Key section -----------------------------------------------------------
        self.label1 = Label(
            self.window, text='Enter your OpenAI API key', width=30, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label1.pack()

        self.entry1 = Entry(
            self.window,
            font=("Arial", 8),
            fg='white',
            bg='black',
            width=33,
        )
        self.entry1.insert(
            0,                  # from th beginning position
            '',     # default text
        )
        self.entry1.pack()

        self.button1 = Button(
            self.window, text='Store key', width=15, height=1,

            command=self.store_key
        )
        self.button1.pack(pady=10)

        canvas = Canvas(self.window, width=300, height=1, bg='#2b2828', borderwidth=0)
        canvas.pack()

# Photo section -----------------------------------------------------------
        self.label2 = Label(
            self.window, text='Press "Cam", then "c" takes a photo, "q" closes cam)',
            width=40, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label2.pack()

        self.button2 = Button(
            self.window, text='Cam', width=15, height=1,
            command=self.open_camera
        )
        self.button2.pack(pady=10)

        canvas2 = Canvas(self.window, width=300, height=1, bg='#2b2828', borderwidth=0)
        canvas2.pack(pady=10)

# Section result -----------------------------------------------------------
        self.label3 = Label(
            self.window, text='OpenAI response is displayed here:',
            width=40, height=1,
            bg='#2b2828', borderwidth=0, relief="ridge", fg='white'
        )
        self.label3.pack()

        self.text_widget = Text(self.window, height=6, width=33)
        self.text_widget.pack()

# ------------------------------------------------------------------

    def store_key(self):
        new_input = self.entry1.get()
        self.api_key = new_input
        self.entry1.config(state=DISABLED)  # disable after submitting

    def open_camera(self):
        if self.api_key is None:
            self.print_text('Please enter the key first!')
            return

        self.generator = OpenAIGenerator(self.api_key)
        self.camera = Camera(self.generator, key='c')

        self.camera_thread = threading.Thread(target=self.start_camera)
        self.camera_thread.start()

    def start_camera(self):
        for result in self.camera.continuous_read():
            # Process the result as needed
            self.handle_camera_result(result)

    def handle_camera_result(self, result):
        # Update the GUI with the result
        self.print_text(result)

    def print_text(self, text):
        self.text_widget.delete('1.0', 'end')  # clear any previous text
        self.text_widget.insert('1.0', text)  # insert new text

    def run(self):
        self.window.mainloop()
