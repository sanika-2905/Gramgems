import os, random
from flask import Flask, render_template, request, jsonify
from model import get_ai_description

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

def generate_social_captions(raw_desc):
    raw = raw_desc.lower()
    
    # --- 1. KIDS & BABIES (Top Priority) ---
    if any(word in raw for word in ['child', 'baby', 'boy', 'girl', 'kid', 'toddler', 'son', 'daughter', 'infant']):
        pool = [
            "Little moments, big memories.",
            "Pure joy in a small package.",
            "Stay wild, brave, and free.",
            "The world is your playground.",
            "Small steps, giant heart.",
            "Sweetest little soul."
        ]
        cat = "Little Wonders"

    # --- 2. SEA / BEACH VIEW ---
    elif any(word in raw for word in ['water', 'sea', 'beach', 'ocean', 'wave', 'sand', 'shore']):
        pool = [
            "High tides and good vibes.",
            "Ocean breeze, putting us at ease.",
            "Salt in the air, love in our hair.",
            "Blue water, better together.",
            "Just us and the big blue.",
            "Shoreline serenity."
        ]
        cat = "Sea Views & Salty Air"

    # --- 3. SUNSET & NATURE ---
    elif any(word in raw for word in ['sun', 'sunset', 'sky', 'evening', 'nature', 'glow', 'mountain']):
        pool = [
            "Chasing sunbeams with you.",
            "Golden days and better ways.",
            "Sunsets are better when shared.",
            "Nature’s paint, our love story.",
            "Everything glows when I’m with you.",
            "Watching the day turn into us."
        ]
        cat = "Sunshine & Nature Magic"

    # --- 4. COUPLES (Only if specifically man/woman or couple detected) ---
    elif any(word in raw for word in ['couple', 'man and woman', 'man and a woman', 'husband', 'wife']):
        pool = [
            "Style on point, love on top.",
            "He’s the vibe, she’s the soul.",
            "Fashionably late, but always together.",
            "Main character energy with my favorite person.",
            "The blueprint for a perfect pair.",
            "Suit & sweet."
        ]
        cat = "Stylish & Sweet Duo"

    # --- 5. DEFAULT (For Solo or general photos) ---
    else:
        pool = [
            "Vibing and thriving.",
            "Living my best life.",
            "Focus on the good.",
            "Creating my own sunshine.",
            "Confidence level: Selfie with no filter.",
            "Life is better when you're laughing."
        ]
        cat = "Daily Vibes"

    # Selection only 2 captions
    return {"category": cat, "captions": random.sample(pool, 2)}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, "temp.png")
    file.save(path)
    description = get_ai_description(path)
    return jsonify(generate_social_captions(description))

if __name__ == '__main__':
    app.run(debug=True, port=5000)