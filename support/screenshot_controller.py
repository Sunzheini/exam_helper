import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab
from screeninfo import get_monitors


class ScreenShotOCR:
    def __init__(self, generator):
        self.result = None
        # the openai generator object
        self.generator = generator

    @staticmethod
    def take_screenshot():
        monitor = get_monitors()[0]
        width = monitor.width
        height = monitor.height

        # central left half of the screen
        left = 0
        right = width // 2
        top = height // 4
        bottom = 3 * height // 4

        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Convert the screenshot to grayscale for better OCR accuracy
    @staticmethod
    def convert_to_gray(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    # Perform OCR using Tesseract
    @staticmethod
    def perform_ocr(image):
        text = pytesseract.image_to_string(image)
        return text

    # Print the extracted text
    @staticmethod
    def print_result(text_to_print):
        print(text_to_print)

    # Take a screenshot and perform OCR on it
    def screenshot_and_ocr(self):
        screenshot = self.take_screenshot()
        gray_screenshot = self.convert_to_gray(screenshot)
        self.result = self.perform_ocr(gray_screenshot)
        holder = self.generator.generate_text(self.result)
        return holder
