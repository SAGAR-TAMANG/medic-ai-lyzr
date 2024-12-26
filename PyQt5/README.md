# Introduce
Optical Character Recognition (OCR) is the process that converts an image of text into a machine-readable text format. For example, if you scan a form or a receipt, your computer saves the scan as an image file. You cannot use a text editor to edit, search, or count the words in the image file. However, you can use OCR to convert the image into a text document with its contents stored as text data.

[![Super Linter](https://img.shields.io/github/workflow/status/NvChad/NvChad/Super-Linter/main?style=flat-square&logo=github&label=Build&color=8DBBE9)](https://github.com/khanhnguyentuann/recognize-text-from-image-using-ocr)

![Customized Card](https://github-readme-stats.vercel.app/api/pin?username=khanhnguyentuann&repo=recognize-text-from-image-using-ocr&title_color=fff&icon_color=f9f9f9&text_color=9f9f9f&bg_color=151515)

# Tech Stack 🛠
The project is built on

**Language:** 
- [Python](https://www.python.org/)

**Library:** 
- [OpenCV](https://opencv.org/)

**Framework**
- [PyQt5](https://pypi.org/project/PyQt5/)


# Getting Started 👩‍💻

## I. Set Up ⚙️

Before beginning to work the project make sure you have [git downloaded](https://git-scm.com/downloads) on your computer

Then, you must open _git_ and _git clone_ the repo to your computer: 
```
git clone https://github.com/khanhnguyentuann/recognize-text-from-image-using-ocr.git
cd recognize-text-from-image-using-ocr
```
## II. Installing

**1. Python**
 
 ```
 You can download the latest version here: https://www.python.org/
 ```

**2. pytesseract**
```
Steps of Installation:
1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki
2. Note the tesseract path from the installation. At the time of this edit, the default installation path was: "C:\Users\USER\AppData\Local\Tesseract-OCR" It may change, so please check the installation path.
3. pip install pytesseract
4. Set the tesseract path in the script (in the file image_processing.py)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
```
**3. Opencv**

```
pip install opencv-python
```
**4. PyQt5**

```
pip install PyQt5
```

## III. Run 🔥

```
python main.py
```
## IV. Note 📝

a. File 'main.py': Contains the code to run the application, it will import the controller package and call the function that creates the main window.

b. Package 'model': Contains all the code related to the application's data model.
  - file '__init__.py': This file is empty and the model directory containing it will be treated as a package by python.
  - file 'image_processing.py': Contains all the code related to image processing and text extraction using pytesseract.

c. Package 'view': Contains all the code related to the application's user interface.
- file '__init__.py': This file is empty and the model directory containing it will be treated as a package by python.
- file 'main_window.py': Contains codes related to creating and setting up the main window of the application.

d. Package 'controller': Contains all the code involved in handling user interaction and updates the model and view accordingly.
- file '__init__.py': This file is empty and the model directory containing it will be treated as a package by python.
- file 'text_extractor.py': Contains code to connect controller and view together and handle user interaction

e. Directory: 'resources': Contains all resources such as icons used by the application, images used to extract text.
- folder: 'icons': Contains icons used by the application such as uploading, extracting and copying icons.
- folder: 'images': Contains images used to extract text

