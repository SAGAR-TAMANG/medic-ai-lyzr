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
from dotenv import load_dotenv
from gtts import gTTS

# Set up OpenAI API key
load_dotenv()

# import cloudinary
# import cloudinary.uploader
# from cloudinary.utils import cloudinary_url
# # Configuration       
# cloudinary.config( 
#     cloud_name = "dz8ajbuaa", 
#     api_key = "567339758213947", 
#     api_secret = os.getenv("CLOUDINARY_SECRET"),
#     secure=True
# )

def index_poster(request):
    context = {}
    if request.method == 'POST' and 'file' in request.FILES:
        print("INSIDE THE POST")
        uploaded_file = request.FILES['file']
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
            # upload_result = cloudinary.uploader.upload()
            # public_id = upload_result['public_id']
            # transformed_url, _ = cloudinary_url(public_id, transformation=["media_lib_thumb"])
            extracted_text = extract_text_from_imageandpdf(url)
        elif file_extension == '.pdf':
            extracted_text = extract_text_from_imageandpdf(url)
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
            health_suggestions = generate_health_suggestions_lyzr(extracted_text)
            audio = generate_audio(health_suggestions, "en")
            context['audio'] = audio
        except Exception as e:
            print("Exception at Lang", e)
            print("English Language Selected (Default) - 2")
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

import requests

api_ocr = os.getenv("OCR_API_KEY")

def extract_text_from_imageandpdf(url):
    # print("URL:", f"https://medic-ai-lyzr.feynmanpi.com/media/{image_path}")
    print("URL:", url)
    response = requests.get(f"https://api.ocr.space/parse/imageurl?apikey={api_ocr}&url={url}")
    print("RESPONSE", response)
    content = response.json()
    # Extract text details
    try:
        parsed_results = content.get("ParsedResults", [])
        if not parsed_results:
            return "No text found in the image."
        
        # Extract text from ParsedResults
        text = "\n".join(result.get("ParsedText", "") for result in parsed_results)
        return text
    except KeyError as e:
        return f"Error in parsing OCR response: {str(e)}"

def generate_health_suggestions_lyzr(extracted_text):
    url = 'https://agent-prod.studio.lyzr.ai/v3/inference/chat/'
    
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': os.getenv("LYZR_API_KEY"),
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
