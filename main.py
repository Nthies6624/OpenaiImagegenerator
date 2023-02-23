from flask import Flask, render_template, request, send_from_directory
import openai
import os

app = Flask(__name__, template_folder='templates')

# Set up OpenAI API key
openai.api_key = "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"

# Create route to serve index.html
@app.route('/')
def index():
    return render_template('index.html')

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
        n=1
    )

    # Save the generated image to the images directory
    img_url = response['data'][0]['url']
    img_filename = img_url.split('/')[-1]
    img_path = f"images/{img_filename}"
    with open(img_path, 'wb') as f:
        f.write(requests.get(img_url).content)

    # Serve the generated image to the front-end
    return send_from_directory('images', img_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='60', debug=True)