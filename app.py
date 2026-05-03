import os
import uuid

from huggingface_hub import InferenceClient
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

STATIC_FOLDER  = "static"
MAX_PROMPT_LEN = 500
DEBUG_MODE     = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
HF_TOKEN       = os.environ.get("HF_TOKEN", "")

app.config["UPLOAD_FOLDER"] = STATIC_FOLDER

if not HF_TOKEN:
    print("[WARN] HF_TOKEN is not set. /generate-image will fail.")
    hf_client = None
else:
    hf_client = InferenceClient(provider="fal-ai", api_key=HF_TOKEN)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate-image", methods=["POST"])
def generate_image():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid request body."}), 400

    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"success": False, "error": "Prompt is required."}), 400

    if len(prompt) > MAX_PROMPT_LEN:
        return jsonify({
            "success": False,
            "error": f"Prompt must be under {MAX_PROMPT_LEN} characters."
        }), 400

    if not hf_client:
        return jsonify({
            "success": False,
            "error": "Server is not configured with a HuggingFace token."
        }), 503

    print(f"[INFO] Generating image for prompt: '{prompt[:80]}'")

    try:
        image = hf_client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-schnell",
        )

        filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(save_path)

        return jsonify({"success": True, "image_url": f"/static/{filename}"})

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"success": False, "error": "Image generation failed. Please try again."}), 500


@app.route("/gallery")
def gallery():
    image_folder = app.config["UPLOAD_FOLDER"]
    try:
        image_files = [
            f for f in os.listdir(image_folder)
            if f.startswith("generated_") and f.endswith(".png")
        ]
        image_urls = [f"/static/{img}" for img in sorted(image_files, reverse=True)]
    except FileNotFoundError:
        image_urls = []

    return render_template("gallery.html", images=image_urls)


import threading
import webbrowser

if __name__ == "__main__":
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=DEBUG_MODE, host="0.0.0.0", port=5000)
