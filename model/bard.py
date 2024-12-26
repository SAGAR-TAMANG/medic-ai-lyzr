from dotenv import load_dotenv
import os

key = os.getenv("GOOGLE_API_KEY")

import pathlib
import textwrap

import google.generativeai as genai

genai.configure(api_key=key)

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

model = genai.GenerativeModel('gemini-1.0-pro-latest')

# response = model.generate_content("What is the meaning of life?")

# print("response:", response)
# print("\ntext:",response.text)

chat = model.start_chat(history=[])

# response = chat.send_message("Considering the following report can you please do the following? (z) Can you break down each result and explain its significance as if you are explaining it to a naive person (a) Explain what is this medical test about as if your target audience is not a medical person at all (b) Explain what is the significance of the test result, what is the meaning of each test value as if you are explaining to naive person having no medical knowledge(c) Explain what kind of foods he/she should take to improve this test result values, explain how these food suggestions will help (d) is there any yoga postures that might be helpful for improving these test results? (e) is there any exercise that he or she can do? (f) What would be the overall lifestyle that he or she needs to maintain to improve the test results (g) What would be the effect of smoking and alcohol intake as per his present health parameters? (h) What is the remark if these statistics are compared with general Indians of the same age group? (i) Please comment in non medical way for a naive person, if any abnormality or ambiguous results are detected in the report ")

# prompt = 'The is the report: DRLOGY PATHOLOGY LAB X. otzzase7as 0912345678 D Accurate | Caring | Instant drlogypathlab@drlogy.com 105-108 MART VISION COMPLEX HEALTHCARE RORD, OPPOSITE HEALTHCARE COMPLEX. MLMAAI-809578 Yash M. Patel Sample Collected At: WL LU ‘Age: 21 Years Me on Bungalow, § G Road, Repintecad on: 97:57 PMO? Dee, 7% Sex : Male urna Colt on: 3:11 PM G2 One, 2k PID: 585 ji Ref, By: Dr. Hiren Shah epated os 04:95PM 2 Dee 2 ABSOLUTE LYMPHOCYTE COUNT (ALC) Investigation Reault Reference Value Unit Primary Sample Type Blood ABSOLUTE LYMPHOCYTE COUNT (ALG) 2000 1300-3500 cellsémeL. calpain eS Cammenta «+ Lymphocytes are a type of white blood cell that plays an important role in the immune system by recognizing and attacking foreign substances, auch as bacteria, vituses, and cancer cella, Low ALC Causes + Vical infections - Some viral infections, such as HIV, can lead to a decrease in ymphocytes. + Cancer treatment - Chemotherapy or radiation therapy can decrease lymphocyte counts + Autoimmune disorders Certain auioimmune disorders, such 08 lupus or cheumatoid arthii, can cause ‘ymphopenia 4+ Malnutrition - Severe malnutrition can lead to a decrease in phocytes. «+ Genetic disorders - Some genetic disorders, suck as DiGeorge ayndrome or WiskotL-Aldkich syndrome, can cause ‘ymphopenia. High ALC Causes : «infections - Bactesial, viral, fungal or parasitic infections can lead to an increase in lymphocytes, + Autoimmune disorders - Gonditions like lupos, sheumatold arthritis, and multiple sclerosis can cause ymphosytosis. + Cancer Lymphocytosis can be a symptom of certain types of cancers, such as leukemia, lymphoma, or myeloma «+ Stress - Physical or emotional stress can cause temporary mphoeytosia + Exercise Strenuous exercize can cause temporary lymphocytosis. «Smoking - Chronic smoking can increase lymphocyte counts, Thank or Raterence ssn of Raper" Bed a ae Medical Lab Technician Dr. Payal Shah Dr. Vimal Shaty (OMLT. BML) (60, Paotogst (0, Pathologst) p ‘penetated am. D2 Dee, 209X DS:00 PA pagel ot!'

# for chunk in response:
#   print(chunk.text)
#   print("_"*80)
# print(response.text)

# response = chat.send_message(prompt)

response = chat.send_message("Translate this text to tamil: I am eating food")

# print(response.text)

for chunk in response:
  print(chunk.text)
  print("_"*80)
