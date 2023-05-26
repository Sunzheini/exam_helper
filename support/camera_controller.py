import cv2
import pytesseract


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


# ------------------------------------------------------------------------------

"""
Here's how you can run the code on your phone:

Install a Python distribution: Start by installing a Python distribution on your phone. 
One popular option is the Termux app for Android, which provides a terminal emulator and 
package manager to run Python on your phone. You can install Termux from the Google Play Store.

Install required packages: Once you have Termux installed, open the app and run the 
following commands to install Python and OpenCV:
pkg install python
pip install opencv-python

Run the Python code: Using a text editor on your phone, create a new Python file (e.g., 
camera_chatbot.py) and paste the code provided in the previous response. Save the file.

Execute the Python script: In Termux, navigate to the directory where you saved the 
Python file using the cd command. For example:
cd /path/to/your/file

Run the Python script:
python camera_chatbot.py

This will start the execution of the Python script, accessing the camera and displaying 
the frames on your phone.

Keep in mind that running resource-intensive tasks like camera processing on a phone may 
vary depending on the device's hardware capabilities. Some older or low-end phones might experience performance limitations. Additionally, ensure that you have the necessary permissions set up for the app to access your phone's camera.

Please note that the steps provided above are specific to running Python and OpenCV on an 
Android phone using the Termux app. If you're using a different phone operating system or 
development environment, the steps may differ.

"""
