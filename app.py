from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import model 

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    # Get optional fields from the form
    custom_tags = request.form.get("custom_tags", "")
    custom_link = request.form.get("custom_link", "")
    
    if file.filename == "":
        return jsonify({"error": "Empty file name"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Call the new API-powered functions
        caption = model.generate_caption(filepath, custom_link)
        hashtags = model.generate_hashtags(caption, custom_tags)

        return jsonify({
            "caption": caption,
            "hashtags": hashtags
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)