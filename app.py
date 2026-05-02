import os
import uuid
import requests

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

STATIC_FOLDER  = "static"
MAX_PROMPT_LEN = 500
DEBUG_MODE     = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
HF_TOKEN       = os.environ.get("HF_TOKEN", "")

app.config["UPLOAD_FOLDER"] = STATIC_FOLDER

HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

if not HF_TOKEN:
    print("[WARN] HF_TOKEN is not set. /generate-image will fail.")


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

    if not HF_TOKEN:
        return jsonify({
            "success": False,
            "error": "Server is not configured with a HuggingFace token."
        }), 503

    print(f"[INFO] Calling HuggingFace API for prompt: '{prompt[:80]}'")

    try:
        response = requests.post(
            HF_API_URL,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": prompt},
            timeout=120
        )

        if response.status_code == 503:
            return jsonify({
                "success": False,
                "error": "Model is loading, please try again in 20 seconds."
            }), 503

        if response.status_code != 200:
            print(f"[ERROR] HF API returned {response.status_code}: {response.text}")
            return jsonify({"success": False, "error": "Image generation failed. Please try again."}), 500

        filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        with open(save_path, "wb") as f:
            f.write(response.content)

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
