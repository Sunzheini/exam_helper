# exam_helper (tested on Windows)
 
1. You need to install pytesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki
2. Note the folder where pytesseract is installed and add it into the system variable 'Path'
3. Running the program is done by running the main.py file using python interpreter

(optional)
4. You have the option to covert to .exe by using pyinstaller:
   a) install it with pip install pyinstaller
   b) go to main project dir and run in the terminal: pyinstaller --onefile --noconsole for_compilation\all_into_one.py   (all_into_one.py is a file containing all the code from the other files but in one place in order to ease the compilation with pyinstaller)
    run the    
   c) the .exe will be in the /dist directory, run it as an administrator
