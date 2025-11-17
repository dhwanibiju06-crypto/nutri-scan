# Import Flask for creating the server and handling requests
from flask import Flask, request, jsonify

# Import OpenAI client
import google.generativeai as genai

# Import os so we can read environment variables (like the API key)
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Create a Flask app
app = Flask(__name__)
# Initialize Gemini with the API key from environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the vision model
model = genai.GenerativeModel("gemini-2.5-flash")

# Define a route for the home page
@app.route('/')
def home():
    return app.send_static_file('nutriscan_home.html')


# Define a route to handle image uploads and process them with Gemini's API
@app.route('/upload', methods=['POST'])
def upload_image():

    # Get the uploaded image from the request
    image = request.files['image']

    #Gemimi expects image in bytes
    image_bytes = image.read()

    # Send image + prompt to Gemini model for analysis
    response = model.generate_content(
        [
            "Provide nutritional information about the food item in the image.",
            {"mime_type": image.mimetype, "data": image_bytes}
        ]
       
    )
    # Return the analysis results as JSON
    return jsonify({"analysis": response.text})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)