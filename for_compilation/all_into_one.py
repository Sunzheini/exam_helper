import openai as openai
import cv2
import pytesseract
import threading
from tkinter import *


class OpenAIGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_text(self, prompt):
        test_prompt = "how much is 4 + 3"

        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=prompt,
          # prompt=test_prompt,
          temperature=0.9,
          max_tokens=150,
          top_p=1,
          frequency_penalty=0.0,
          presence_penalty=0.6,
          stop=[" Human:", " AI:"]
        )

        to_return = self.print_text(response)
        return to_return

    @staticmethod
    def print_text(my_response):
        my_text = my_response.choices[0].text.strip()
        # print('AI:', my_text)
        return my_text


class Camera:
    def __init__(self, generator, key, default_camera_index=0):
        # the openai generator object
        self.generator = generator
        # Use '0' for the default camera, or specify a different camera index if available
        self.default_camera_index = default_camera_index
        # key to be presses to capture the photo
        self.key = key
        # create capture object
        self.capture_object = self.create_capture_object()
        # the result of the OCR
        self.result = None

    def create_capture_object(self):
        cap = cv2.VideoCapture(self.default_camera_index)
        return cap

    def read_frame(self):
        ret, frame = self.capture_object.read()
        return frame

    @staticmethod
    def show_frame(frame):
        cv2.imshow('Camera Feed', frame)

    # Convert the frame to grayscale for better OCR accuracy
    @staticmethod
    def convert_to_gray(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray

    # Perform OCR using Tesseract
    @staticmethod
    def perform_ocr(frame):
        text = pytesseract.image_to_string(frame)
        return text

    # print the extracted text
    @staticmethod
    def print_result(text_to_print):
        print("Extracted Text:", text_to_print)

    # Create a window to display the photo
    @staticmethod
    def create_window():
        cv2.namedWindow('Captured Photo', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Captured Photo', 800, 600)

    # Display the captured photo in the separate window
    @staticmethod
    def display_in_window(frame):
        cv2.imshow('Captured Photo', frame)

    # main loop --------------------------------------------------------------------

    def continuous_read(self):
        # Wait for a specific key press to capture the photo
        while True:
            # Display the camera feed in a window
            frame = self.read_frame()
            self.show_frame(frame)
            # Check for a key press event
            key = cv2.waitKey(1) & 0xFF
            # If 'x' is pressed, exit the loop, release the capture, and destroy all windows
            if key == ord('x'):
                self.capture_object.release()
                cv2.destroyAllWindows()
                break

            # If 'c' is pressed, perform OCR
            if key == ord(self.key):
                self.convert_to_gray(frame)
                self.result = self.perform_ocr(frame)

                # ouput
                # self.print_result(self.result)
                holder = self.generator.generate_text(self.result)
                yield holder

                # display the frame in a window
                self.create_window()
                self.display_in_window(frame)


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


class MainController:
    def __init__(self):
        self.new_gui = ExamHelperGui()

    def run(self):
        self.new_gui.run()


connection = MainController()
connection.run()
