from django.shortcuts import render
from django.core.files.storage import FileSystemStorage 
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import requests
from django.http import JsonResponse
import time
import os
import re
import fitz # PyMuPDF
import pytesseract
import cv2
from dotenv import load_dotenv
from gtts import gTTS

# Set up OpenAI API key
load_dotenv()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def index_poster(request):
    context = {}
    if request.method == 'POST' and 'file' in request.FILES:
        print("INSIDE THE POST")
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        file_extension = get_file_extension(name)

        # os.chmod(os.path.join(settings.MEDIA_ROOT, name), 0o777)
        
        request.session['url'] = url
        request.session['name'] = name

        context['url'] = url
        context['name'] = uploaded_file.name
        context['extension'] = file_extension
        print("\n Contexts \n", context, "\n")

        if file_extension in ('.png', '.jpg', '.jpeg', '.heic', '.webp'):
            extracted_text = extract_text_from_image(os.path.join(settings.MEDIA_ROOT, name))
        elif file_extension == '.pdf':
            extracted_text = extract_text_from_pdf(os.path.join(settings.MEDIA_ROOT, name))
        else:
            extracted_text = 'Not a correct extension'

        print("\n Extracted Text:", extracted_text, '\n')
        
        try:
            print("English Language Selected")
            context['language'] = "en"
            # health_suggestions = generate_health_suggestions_gemini(extracted_text)
            health_suggestions = generate_health_suggestions_lyzr(extracted_text)
            audio = generate_audio(health_suggestions, "en")
            context['audio'] = audio
        except Exception as e:
            print("Exception at Lang", e)
            print("English Language Selected (Default) - 2")
            # health_suggestions = generate_health_suggestions_gemini(extracted_text)
            health_suggestions = generate_health_suggestions_lyzr(extracted_text)

        context['extracted_text'] = extracted_text
        context['health_suggestions'] = health_suggestions

        list_of_output = text_division_gemini(health_suggestions)
        
        context['list_outputs'] = list_of_output
        
        if isinstance(health_suggestions, str):
            print("TRUE IT's A TEXT")
            return render(request, 'output.html', context)
        else:
            print("Not a text")
        
        return render(request, 'index.html', context)

    if request.method == 'POST':
        extracted_text = request.POST.get("search_space")
        print("INPUT: ", extracted_text)
        try:
            print("English Language Selected")
            context['language'] = "en"
            # health_suggestions = generate_health_suggestions_gemini(extracted_text)
            health_suggestions = generate_health_suggestions_lyzr(extracted_text)
            audio = generate_audio(health_suggestions, "en")
            context['audio'] = audio
        except Exception as e:
            print("Exception at Lang", e)
            print("English Language Selected (Default) - 2")
            # health_suggestions = generate_health_suggestions_gemini(extracted_text)
            health_suggestions = generate_health_suggestions_lyzr(extracted_text)

        context['extracted_text'] = extracted_text
        context['health_suggestions'] = health_suggestions

        list_of_output = text_division_gemini(health_suggestions)
        
        context['list_outputs'] = list_of_output
        
        if isinstance(health_suggestions, str):
            print("TRUE IT's A TEXT")
            return render(request, 'output.html', context)
        else:
            print("Not a text")
        
        return render(request, 'index.html', context)

    return render(request, 'index.html')

# Audio Extraction

def generate_audio(input_text, language, user='guest'):    
    print("\n INSIDE AUDIO GENERATION \n")
    max_attempts = 100
    for i in range(max_attempts):
        try:
            audio_name = f"{user}_{language}_{i}.mp3"
            audio_obj = gTTS(text=input_text, lang=language, slow=False)
            audio_obj.save(os.path.join(settings.MEDIA_ROOT, audio_name))
            print("\nAUDIO SUCCESSFULLY GENERATED:", audio_name, '\n\n')
            return audio_name
        except Exception as e:
            print(f"\n\nEXCEPTION OCCURRED IN AUDIO (attempt {i+1}/{max_attempts}): {e}")
    print("\n\nFailed to generate audio after multiple attempts.")
    return None  # Or handle the failure scenario as needed

def text_division_gemini(text):
    sections = re.split(r'[a-j]\)', text)

    print("----------------------------\nSECTIONS BEFORE SPLIT: \n\n", sections, "\n\n----------------------------")
    

    # For the subsequent sections, adjust the index by 1
    try: 
        text_a = sections[0]
        print("text a:", text_a)
        text_b = sections[1]
        print("text b:", text_b)
        text_c = sections[2]
        print(text_c)
        text_d = sections[3]
        print(text_d)
        text_e = sections[4]
        print(text_e)
        text_f = sections[5]
        print(text_f)
        text_g = sections[6]
        print(text_g)
        text_h = sections[7]
        print(text_h)
        text_i = sections[8]
        print(text_i)

        return [text_a, text_b, text_c, text_d, text_e, text_f, text_g, text_h, text_i]
    except Exception as e:
        print("Exception occured at:", e)
        return ''
    
def get_file_extension(file_name):
    return os.path.splitext(file_name)[1].lower()

## Image Processing 

def extract_text_from_image(image_path):
        image = cv2.imread(image_path)
        image = remove_line(image)

        threshold_img = pre_processing(image)
        
        tesseract_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(threshold_img, config=tesseract_config, lang='eng')

        return text

def extract_text_from_pdf(pdf_path):

    pdf_document = fitz.open(pdf_path)
    output = ""

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        
        text = page.get_text()
        
        output += text
    
    if (output.strip() == ""):
            for page_number in range(pdf_document.page_count):
                page = pdf_document.load_page(page_number)

                image_list = page.get_pixmap()

                # Generate a unique image path
                image_path = f"{pdf_path}_page_{page_number + 1}_img_.png"

                # Save the image
                image_list.save(image_path)

                # Extract text from the image and append it to the output
                text = extract_text_from_image(image_path)
                output += text + "\n"

    pdf_document.close()
    
    return output

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

def generate_health_suggestions_lyzr(extracted_text):
    url = 'https://agent-prod.studio.lyzr.ai/v3/inference/chat/'
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'sk-default-QisHUr8meLmfZdghTUD33VMKxvUiMOvZ',
    }

    data = {
        "user_id": "sagar.bdr0000@gmail.com",
        "agent_id": "676d025fdec1ba012db54753",
        "session_id": "676d025fdec1ba012db54753",
        "message": extracted_text,
    }

    # Send POST request
    response = requests.post(url, json=data, headers=headers)
    print("LYZR RESPONSE", response)

    response_data = response.json()
    response_text = response_data.get('response', '')

    # If the response status is OK, return the response as JSON
    if response.status_code == 200:
        return response_text
    else:
        return JsonResponse({'error': 'Request failed', 'status_code': response.status_code}, status=500)
