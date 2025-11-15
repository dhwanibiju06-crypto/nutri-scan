# Import Flask for creating the server and handling requests
from flask import Flask, request, jsonify

# Import OpenAI client
from openai import OpenAI

# Import os so we can read environment variables (like the API key)
import os

# Create a Flask app
app = Flask(__name__)
# Initialize OpenAI client with the API key from environment variables
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define a route for the home page
@app.route('/')
def home():
    return app.send_static_file('nutriscan_home.html')


# Define a route to handle image uploads and process them with OpenAI's API
@app.route('/upload', methods=['POST'])
def upload_image():
    # Get the uploaded image from the request
    image = request.files['image']
    # Call OpenAI's API to analyze the image
    response = openai.images.analyze(
        model="vision-001",
        image=image,
        prompt="Provide nutritional information about the food item in the image."
    )
    # Return the analysis results as JSON
    return jsonify(response)
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)