import os
import time

import markdown
from flask import Flask, render_template, request, jsonify,render_template_string
import google.generativeai as genai
import base64
import io
from PIL import Image
from markdown import Markdown

# Configure the API
api_key = "AIzaSyDoPY7uXdjGOke9G3KBD0U5vnoFlXvuS5A"  # Replace with your actual API key
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    start_time = time.time()

    data = request.json
    image_data = data.get('image')

    # Process the image data
    image = process_image(image_data)

    # Upload the image and generate a response
    response = meow(image)

    print(f"Total time for submit: {time.time() - start_time:.2f} seconds")
    return jsonify(response=response)

def process_image(image_data):
    start_time = time.time()

    # Convert base64 string to a PIL Image
    image_data = image_data.split(",")[1]  # Remove the prefix
    image_bytes = base64.b64decode(image_data)

    # Load the image using PIL
    image = Image.open(io.BytesIO(image_bytes))
    return image

def meow(image):
    start_time = time.time()

    # Resize image before saving
    max_size = (1024, 1024)  # Set a maximum size for the image
    image.thumbnail(max_size)

    # Save the image to a temporary file if needed
    image_path = "temp_image.png"
    image.save(image_path)
    uploaded_file = genai.upload_file(image_path)
    prompt = "\n\nYou are now integrated into an application that functions like an ai  based paint app. anytime a user draws something, it usually is a problem. the image u recieved contains all details and values , using the details please deduce an answer and print the answerin markdown. let the answer invove complete explanation"
    result = model.generate_content([uploaded_file, prompt])
    os.remove(image_path)
    md = markdown.Markdown()
    html = md.convert(result.text)
    return html
if __name__ == '__main__':
    app.run(debug=True)
