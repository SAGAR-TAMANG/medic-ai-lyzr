from django.shortcuts import render
from django.core.files.storage import FileSystemStorage 
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
import os

from django.http import HttpResponseRedirect

import pytesseract
import cv2

from openai import OpenAI
from dotenv import load_dotenv

# Set up OpenAI API key
load_dotenv()
key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key = key)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def index(request):
  context = {}
  if request.method == 'POST' and 'file' in request.FILES:
    print("INSIDE THE POST IF")
    uploaded_file = request.FILES['file']
    fs = FileSystemStorage()
    name = fs.save(uploaded_file.name, uploaded_file)
    url = fs.url(name)

    file_extension = get_file_extension(name)

    # os.chmod(os.path.join(settings.MEDIA_ROOT, name), 0o777)
    
    request.session['url'] = url
    request.session['name'] = name

    extracted_text = extract_text_from_image(os.path.join(settings.MEDIA_ROOT, name))

    context['url'] = url
    context['name'] = uploaded_file.name
    context['extension'] = file_extension
    context['extracted_text'] = extracted_text

    health_suggestions = generate_health_suggestions(extracted_text)

    context['health_suggestions'] = health_suggestions
    
    if isinstance(health_suggestions, str):
        print("TRUE IT's A TEXT")
        return render(request, 'chat.html', context )
    else:
        print("Not a text")
    
    return render(request, 'index.html', context)

  return render(request, 'index.html')

def chat(request):  
  if request.method =='POST':
    search_space = request.POST.get("search_space")
    
    health_suggestions = generate_health_suggestions(search_space)
    
    print(health_suggestions)

    context = {
        'health_suggestions' : health_suggestions
    }

    if isinstance(health_suggestions, str):
        print("TRUE IT's A TEXT")
        return render(request, 'chat.html', context)
    else:
        print("Not a text")

  
  return render(request, 'chat.html')

def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].lower()

# OpenAI

def generate_health_suggestions(report_text):
    prompt = f'This is a medical report, generate a report on this for a novice: \n\n"""\n{report_text}"""\n\nHealth suggestions:'
    print("Prompt: ", prompt)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert doctor who can analyze reports of patients. Go through the report provided by the user and generate an output what the report is about and what are the best actions the user can take. Explain it in a way that you would to a novice. Make sure that it is not too lengthy, but should not lack in important details. You go through the report then only try to give an accurate assesment."},
                {"role": "user", "content": prompt}
            ]
        )
        health_suggestions = response.choices[0].message

        print("This is Health Suggestions: ", health_suggestions)
        return health_suggestions.content
    except Exception as e:
        print(f"Error generating health suggestions: {e}")
        return False;

## Image Processing 

def extract_text_from_image(image_path):
        image = cv2.imread(image_path)
        image = remove_line(image)

        threshold_img = pre_processing(image)
        
        tesseract_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(threshold_img, config=tesseract_config, lang='eng')

        # text_split = text.split()

        # file_path = os.path.join(os.path.dirname(__file__), 'eng_words.txt')

        # with open(file_path) as word_file:
        #     english_words = set(word.strip().lower() for word in word_file)

        # def is_english_word(word):
        #     return word.lower() in english_words

        # real_words = ""

        # for text in text_split:
        #     if is_english_word(text):
        #         real_words += text + " "

        return text

def check_image_ratio(image):
    height, width, _ = image.shape
    if height > width:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return image

def remove_line(image):
        removed = image.copy()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Remove vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
        remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(removed, [c], -1, (255,255,255), 15)

        # Remove horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(removed, [c], -1, (255,255,255), 5)

        # Repair kernel
        repair_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        removed = 255 - removed
        dilate = cv2.dilate(removed, repair_kernel, iterations=5)
        dilate = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)
        pre_result = cv2.bitwise_and(dilate, thresh)

        result = cv2.morphologyEx(pre_result, cv2.MORPH_CLOSE, repair_kernel, iterations=5)
        final = cv2.bitwise_and(result, thresh)

        invert_final = 255 - final
        
        normal_image = cv2.cvtColor(invert_final,cv2.COLOR_GRAY2BGR)
        return normal_image

def pre_processing(image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[-1]
        return threshold_img

