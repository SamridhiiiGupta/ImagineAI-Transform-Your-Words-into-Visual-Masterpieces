# AI Image Generator

A web application that generates images based on text prompts using Stability AI's SDXL model through Replicate.

## Features

- Simple and intuitive user interface
- Real-time image generation
- Powered by Stability AI's SDXL model
- Responsive design

## Requirements

- Python 3.7+
- Replicate API token

## Setup

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your Replicate API token in the `.env` file:
   ```
   REPLICATE_API_TOKEN=your_replicate_api_token_here
   ```
   You can get an API token from [Replicate](https://replicate.com/) by creating an account.
4. Run the application:
   ```
   python app.py
   ```
5. Open your web browser and go to `http://localhost:5000`

## Usage

1. Enter a detailed text prompt in the text area
2. Click the "Generate Image" button
3. Wait for the image to be generated
4. The generated image will be displayed below

## Notes

- More detailed and specific prompts tend to yield better results
- Image generation may take 10-30 seconds depending on the complexity of the prompt
- The application uses Stability AI's SDXL model with a 1024x1024 resolution
- A negative prompt is automatically applied to reduce common issues like poor quality and bad anatomy

## Troubleshooting

If you encounter any issues:

1. Ensure your Replicate API token is valid and has sufficient credits
2. Check the console for any error messages
3. Make sure all dependencies are installed correctly 