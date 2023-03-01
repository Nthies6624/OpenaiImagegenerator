import requests
from PIL import Image
from flask import Flask, render_template, request, send_from_directory
from flask import send_file
import openai
import os
my_secret = os.environ['Openai key']



app = Flask(__name__, template_folder='templates')

# Set up OpenAI API key
openai.api_key = my_secret

# Create route to serve index.html
@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/generated-images/<path:filename>')
def serve_generated_image(filename):
    return send_file(f'images/{filename}.png', mimetype='image/png')

@app.route('/script.js')
def serve_script():
    return send_from_directory('static', 'script.js')

# Create route to handle form submission
@app.route('/generate-image', methods=['POST'])
def generate_image():
    # Get user input from the form
    image_size = request.form.get('image-size')
    bg_color = request.form.get('background-color')
    image_style = request.form.get('image-style')

    # Call OpenAI API to generate image
    response = openai.Image.create(
        prompt=f"Generate an image of size {image_size} with a {bg_color} background in the style of {image_style}.",
        n=1,
        model='image-alpha-001'
    )

    # Save the generated image to the images directory as a PNG file
    img_url = response['data'][0]['url']
    img_filename = img_url.split('/')[-1]
    img_path = f"images/{img_filename.split('.')[0]}.png"
    with open(img_path, 'wb') as f:
        f.write(requests.get(img_url).content)

    # Serve the generated image to the front-end
    return send_from_directory('images', f"{img_filename.split('.')[0]}.png")


  
    # Return path to generated image
    return render_template('index.html', image=img_path)
    return

image = Image.open("the.png")# Display the image
image.show()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='60', debug=True)
