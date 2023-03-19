import os
import requests
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import openai
my_secret = os.environ['SECRET']

# Set up OpenAI API key
openai.api_key = my_secret

app = Flask(__name__)

# Set up the uploads folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    prompt = request.form["prompt"]
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response["data"][0]["url"]

    # Download and save the image
    response = requests.get(image_url)
    image_filename = f"{prompt.replace(' ', '_')}.png"
    with open(os.path.join(UPLOAD_FOLDER, image_filename), "wb") as f:
      f.write(response.content)

    return redirect(url_for("uploaded_file", filename=image_filename))

  return render_template("index.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
  return send_from_directory(app.config["UPLOAD_FOLDER"], os.path.basename(filename))



if __name__ == '__main__':
  app.run(host='0.0.0.0', port='40', debug=True)
