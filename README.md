# exam_helper (tested on Windows)
 
1. You need to install pytesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki.
2. Note the folder where pytesseract is installed and add it into the system variable 'Path'.
3. Running the program is done by:
   a) running the main.py file using python interpreter
   b) running the .exe file in dist/

4. In both cases you will need an OpenAI API key, so go get one. Paste the key inside the top-most entry field and click the button below to store it inside the program.
5. Then choose whether you want to take a screnshot of your query or take a photo of it.
6. The query you want to screenshot must be located in the central left half of your screen. The program is tested by opening a blank notepad, which takes the left half of the screen and writing a query in the central part.
7. If you wish to take a photo, you must press the button to open the cam and then hold an image containing your query in front of it. In the best case this should be a clean background with the letters of the query seen clearly. When you press 'c' the query is send and also the captured image is displayed in a separate window.
