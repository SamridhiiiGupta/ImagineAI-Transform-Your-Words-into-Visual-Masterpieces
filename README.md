# 🧠 ImagineAI — Transform Your Words into Visual Masterpieces 🎨

Welcome to the **AI Image Generator**, a Flask-based web application that uses **Stable Diffusion** via Hugging Face 🤗 Diffusers to create stunning images from simple text prompts.

<p align="center">
  <img src="screencapture-127-0-0-1-5000-2025-07-17-01_37_59.png" alt="Homepage" width="100%"/>
</p>

---

## ✨ Features

- 🔤 Generate images from any creative prompt using Stable Diffusion
- 🖼️ Interactive web interface with prompt input and image output
- 🗂️ Gallery view to browse all generated images
- 💾 Option to download images locally
- ⚡ Fast, local image generation using PyTorch + Hugging Face + Diffusers
- 🎨 Clean, responsive UI using Bootstrap

---

## 🛠️ Tech Stack

| Component       | Tech Used                      |
|----------------|--------------------------------|
| Backend         | Python, Flask                  |
| Image Generation| Hugging Face Diffusers, Torch |
| Frontend        | HTML, CSS, Bootstrap           |
| Templating      | Jinja2                         |
| Hosting         | Localhost (optional: deploy on Render, Heroku, etc.) |

---

## 🖼️ Screenshots

### 🔹 Homepage  
Prompt input with clear interface and CTA.

<p align="center">
  <img src="screencapture-127-0-0-1-5000-2025-07-17-02_13_10.png" alt="Homepage Screenshot" width="80%">
</p>

### 🔹 Gallery  
View previously generated images.

<p align="center">
  <img src="screencapture-127-0-0-1-5000-gallery-2025-07-17-01_38_12.png" alt="Gallery Screenshot" width="80%">
</p>

---

## ⚙️ How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/ai-image-generator.git
cd ai-image-generator
````

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> Requirements include:
>
> * `flask`
> * `torch`
> * `transformers`
> * `diffusers`
> * `accelerate`
> * `safetensors`

### 4️⃣ Run the App

```bash
python app.py
```

You browser will automatically open at:
👉 `http://127.0.0.1:5000`

---

## 🧪 Example Prompts

| Prompt                                     | Output |
| ------------------------------------------ | ------ |
| "A futuristic city in the sky"             | 🏙️    |
| "A mystical forest with glowing mushrooms" | 🌳     |
| "A cyberpunk woman riding a dragon"        | 🐉     |

---

## 📁 Project Structure

```
ai-image-generator/
│
├── app.py
├── static/
│   ├── css/
│   └── images/
├── templates/
│   ├── index.html
│   └── gallery.html
├── generated_images/
├── README.md
└── requirements.txt
```

---

## 📌 Future Enhancements

* [ ] Image upscaling (via ESRGAN or Real-ESRGAN)
* [ ] Prompt history with tags
* [ ] User login and save images to profile
* [ ] Deploy to Hugging Face Spaces / Streamlit / Render

---

## 🙌 Acknowledgments

* 🤗 [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/index)
* 🔥 [PyTorch](https://pytorch.org/)
* 🎨 [Bootstrap](https://getbootstrap.com/)

---

## 👩‍💻 Developed By

**Samridhi Gupta**

📧 [guptasamridhi1432@gmail.com](mailto:guptasamridhi1432@gmail.com)
🔗 [LinkedIn]([https://www.linkedin.com/in/samridhi-gupta](https://www.linkedin.com/in/samridhiii-gupta/)) | [GitHub]([https://github.com/samridhi-07](https://github.com/SamridhiiiGupta))

---

## 📜 License

This project is licensed under the **MIT License** – feel free to use, share, and improve.

---

🖤 *Made with Python, Passion & Pixels.*

```
