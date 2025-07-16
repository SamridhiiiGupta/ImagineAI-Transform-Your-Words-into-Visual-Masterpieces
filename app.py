from flask import Flask, render_template, request, jsonify, send_from_directory
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import os
import uuid
import webbrowser
import threading
import glob

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'  # Folder for generated images

# Load model once when the server starts
print("[INFO] Loading Stable Diffusion model...")
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    revision="fp16" if device == "cuda" else None,
)
pipe = pipe.to(device)
pipe.safety_checker = None  # Optional: disable NSFW checker

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate-image", methods=["POST"])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"success": False, "error": "Prompt is required."}), 400

        print(f"[INFO] Generating image for prompt: '{prompt}'")

        if device == "cuda":
            with torch.autocast("cuda"):
                result = pipe(prompt, guidance_scale=7.5, num_inference_steps=30)
        else:
            with torch.no_grad():
                result = pipe(prompt, guidance_scale=7.5, num_inference_steps=30)

        image = result.images[0]

        filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(output_path)

        image_url = f"/static/{filename}"
        return jsonify({"success": True, "image_url": image_url})

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
    
app.config["UPLOAD_FOLDER"] = "static"

@app.route("/gallery")
def gallery():
    image_folder = app.config['UPLOAD_FOLDER']
    image_files = [f for f in os.listdir(image_folder) if f.startswith("generated_") and f.endswith(".png")]
    image_urls = [f"/static/{img}" for img in sorted(image_files, reverse=True)]
    return render_template("gallery.html", images=image_urls)


@app.route("/static/<path:filename>")
def serve_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Auto-open browser function
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True, use_reloader=False)
