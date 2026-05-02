import os
import uuid
import requests

import replicate
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

STATIC_FOLDER   = "static"
MAX_PROMPT_LEN  = 500
DEBUG_MODE      = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
REPLICATE_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")

app.config["UPLOAD_FOLDER"] = STATIC_FOLDER

SD_MODEL = "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4"

if not REPLICATE_TOKEN:
    print("[WARN] REPLICATE_API_TOKEN is not set. /generate-image will fail.")


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

    if not REPLICATE_TOKEN:
        return jsonify({
            "success": False,
            "error": "Server is not configured with a Replicate API token."
        }), 503

    print(f"[INFO] Calling Replicate API for prompt: '{prompt[:80]}'")

    try:
        output = replicate.run(
            SD_MODEL,
            input={
                "prompt": prompt,
                "guidance_scale": 7.5,
                "num_inference_steps": 30,
                "width": 512,
                "height": 512,
            }
        )

        image_url_remote = output[0] if output else None
        if not image_url_remote:
            raise ValueError("No image returned from Replicate.")

        filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        img_response = requests.get(image_url_remote, timeout=30)
        img_response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(img_response.content)

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
