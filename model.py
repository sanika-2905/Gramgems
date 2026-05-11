import google.generativeai as genai
from PIL import Image
import random

# Keep your key here just in case it works!
genai.configure(api_key="ENTER YOUR  API KEY HERE")

# --- EMERGENCY CAPTION BANK (If AI Fails) ---
OFFLINE_CAPTIONS = [
    "Perspective is everything. Finding beauty in the details.",
    "A moment frozen in time, a memory kept forever.",
    "Elegance in every pixel. Simplicity is the ultimate sophistication.",
    "Chasing light and capturing stories. ✨",
    "The art of being present in this very frame.",
    "Focus on what matters; let the rest be a blur.",
    "Standard of excellence in every shot. 🎞️",
    "Savoring this view and the peace it brings.",
    "A symphony of colors and quiet moments.",
    "Minimalism at its finest. Less is more."
    
]

def generate_caption(image_path, custom_link=""):
    try:
        # 1. TRY THE AI FIRST
        model = genai.GenerativeModel('gemini-1.5-flash')
        img = Image.open(image_path)
        response = model.generate_content(["Write a 1-sentence Instagram caption for this.", img])
        
        if response and response.text:
            caption = response.text.strip()
        else:
            # 2. FALLBACK TO RANDOM BANK
            caption = random.choice(OFFLINE_CAPTIONS)
            
    except Exception as e:
        print(f"API Error (Using Fallback): {e}")
        # 3. EMERGENCY FALLBACK
        caption = random.choice(OFFLINE_CAPTIONS)

    if custom_link:
        caption += f"\n\n🔗 {custom_link}"
    return caption

def generate_hashtags(caption, custom_tags=""):
    tags = ["#aesthetic", "#minimalism", "#visuals", "#explore", "#photography", "#picoftheday"]
    selected = random.sample(tags, 3)
    return f"{' '.join(selected)} {custom_tags}".strip()