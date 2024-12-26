import re

# Define the text
text = """
(a) This medical test is an eye examination report that assesses the health and function of your eyes. It includes various tests, such as vision measurement, cornea examination, lens examination, and optic nerve evaluation. The report provides information about the overall condition of your eyes and any potential abnormalities.

(b) The significance of the test result is as follows:

- Vision: Your vision is generally good, with both eyes having 6/6 vision. However, the "P" notation next to your left eye's near vision indicates possible problems with nearsightedness (myopia).

- Conjunctiva and Cornea: These are the clear, protective layers covering your eyes. The report shows that both your conjunctiva and cornea are clear, indicating no signs of inflammation or infection.

- Optic Nerve: The optic nerve carries visual information from your eyes to your brain. The report mentions "CDR 0.7" and "CDR 0.8" for your right and left eyes, respectively. CDR stands for cup-to-disc ratio, which measures the size of the optic nerve head relative to the entire optic nerve. Slightly elevated CDR values might need to be monitored to rule out any potential glaucoma risks.

- Lens: The report mentions "Phacodonesis" for your lens, which refers to the trembling or shaking of the lens when your eye moves. This is typically a normal finding and does not usually require treatment.

- AP (24-2): This test evaluates the peripheral vision (side vision). The result shows "EARLY SCOTOMA IN SUPERIOR AND INFERIOR ARCUATE AREA" for your right eye and "SCATTERED DEPRESSED SPOTS" for your left eye. These findings indicate areas of reduced sensitivity in your peripheral vision, possibly due to retinal abnormalities. Further evaluation and monitoring may be needed to determine the cause and extent of these visual field defects.

- CCT: CCT stands for central corneal thickness, which measures the thickness of the cornea at its center. Your corneal thickness is 575 microns in the right eye and 564 microns in the left eye, which are within normal ranges.

- OCT-RNFL: OCT-RNFL measures the thickness of the retinal nerve fiber layer (RNFL), which is a layer of nerve fibers that transmits visual information from the retina to the brain. The report shows "BORDERLINE THINNING" in your right eye and "BIPOLAR THINNING" in your left eye. These findings indicate a possible thinning of the RNFL, which can be associated with glaucoma or other retinal conditions. Further evaluation and monitoring may be needed to determine the cause and extent of this thinning.

(c) To improve the test result values, consider incorporating the following foods into your diet:

- Leafy Green Vegetables: Foods rich in lutein and zeaxanthin, such as spinach, kale, collard greens, and broccoli, may help protect the retina from damage.

- Citrus Fruits: Vitamin C found in citrus fruits like oranges, grapefruits, and lemons can contribute to overall eye health.

- Omega-3 Fatty Acids: Foods high in omega-3 fatty acids, such as salmon, tuna, mackerel, walnuts, and flaxseeds, may support retinal health and reduce inflammation.

- Berries: Berries, particularly blueberries, are rich in antioxidants and may help protect the eyes from oxidative stress.

- Whole Grains: Whole grains provide essential nutrients, including vitamin E and zinc, which are important for eye health.

(d) Certain yoga postures that might be helpful in improving eye health include:

- Eye Rolls: Gently roll your eyes in clockwise and counterclockwise directions to improve eye muscle coordination and flexibility.

- Palming: Close your eyes gently and cover them with your palms, creating a warm and dark environment. This can help relax the eye muscles and reduce stress.

- Trataka (Gazing): Focus your gaze on a single object, such as a candle flame or a dot on the wall, for a few minutes at a time. This practice can help improve concentration and eye coordination.

(e) Some exercises that might be beneficial for improving eye health include:

- Eye Blinking: Consciously blink your eyes more often throughout the day to keep your eyes moist and reduce dryness.

- Near-Far Focusing: Shift your focus between a nearby object and a distant object several times. This exercise helps strengthen the eye muscles and improve focusing ability.

- Figure-Eight Exercise: Trace a figure-eight pattern with your eyes, following the pattern with your gaze. This exercise helps improve eye movement and coordination.

(f) To maintain an overall healthy lifestyle that supports eye health:

- Get Regular Eye Exams: Schedule regular eye exams with your eye doctor to detect any potential problems early and receive appropriate treatment if needed.

- Protect Your Eyes from UV Rays: Wear sunglasses that block 100% of UV rays when outdoors to protect your eyes from sun damage.

- Maintain a Healthy Diet: Consume a balanced diet rich in fruits, vegetables, whole grains, and lean protein to support overall eye health.

- Avoid Smoking and Excessive Alcohol Consumption: Smoking and excessive alcohol intake can negatively impact eye health. Quitting smoking and limiting alcohol consumption is beneficial for your overall well-being, including eye health.

- Manage Chronic Conditions: If you have chronic conditions like diabetes or high blood pressure, work closely with your healthcare provider to manage them effectively, as these conditions can affect eye health.

(g) Smoking and excessive alcohol intake can have detrimental effects on your overall health, including your eye health. Smoking can increase your risk of developing cataracts, macular degeneration, and other eye problems. Excessive alcohol consumption can also harm the optic nerve and lead to vision problems. It's essential to avoid smoking and limit alcohol intake to protect your eyes and overall well-being.

(h) If these statistics are compared with general Indians of the same age group, it's difficult to make a direct comparison without having access to relevant population data. However, based on the information provided in the report, there appear to be some areas that warrant further evaluation and monitoring. The slightly elevated CDR values, borderline RNFL thinning, and visual field defects require additional investigation to determine their significance and potential impact on your eye health.

(i) There are no abnormalities or ambiguous results detected in the report. However, the findings of early scotoma, scattered depressed spots, borderline RNFL thinning, and bipolar RNFL thinning require further evaluation and monitoring to assess their potential impact on your vision and overall eye health. It's important to follow up with your eye doctor as recommended for a comprehensive assessment and management plan.
"""

# Split the text into sections using "(a)" as the delimiter
sections = re.split(r'\([a-i]\)', text)

# Extract each section into a variable
text_a = "(before)" + sections[0][4:0]

# For the subsequent sections, adjust the index by 1
text_b =sections[1][4:]
text_c =sections[2]
text_d = "(c)" + sections[3]
text_e = "(d)" + sections[4]
text_f = "(e)" + sections[5]
text_g = "(f)" + sections[6]
text_h = "(g)" + sections[7]
text_i = "(h)" + sections[8]
text_i = "(i)" + sections[9]

# Print the variables to verify
print(text_a)
print(text_b)
print(text_c)
print(text_d)
print(text_e)
print(text_f)
print(text_g)
print(text_h)
print(text_i)

print("Length: ", len(sections))

string = "(a) This medical test is a Complete Blood Count (CBC) with Absolute Count, which measures the levels of various components in your blood, such as red blood cells, white blood cells, and platelets."

print(string[4:])