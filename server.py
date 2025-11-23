# Import Flask for creating the server and handling requests
from flask import Flask, json, request, jsonify

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

@app.route('/camerapage')
def camera():
    return app.send_static_file('nutriscan_camerapage.html')


# Define a route to handle image uploads and process them with Gemini's API
@app.route('/upload', methods=['POST'])
def upload_image():

    # Get the uploaded image from the request
    image = request.files['image']

    #Gemimi expects image in bytes
    image_bytes = image.read()

    prompt = """
            TASK: Critically analyze the food label ingredients. Return a strictly formatted JSON array.

            CONSTRAINTS:
             1. No Decomposition: Treat compound ingredients (text in parentheses) as a single item. Do not list sub-ingredients like vitamins separately.
             2. No Markdown: STRICTLY DO NOT use markdown code blocks (```json). The output must start directly with `[` and end with `]`.
             3. Structure: For each ingredient, provide: `ingredient`, `concerns` (nuanced scientific debates), `classification` ('safe', 'caution', 'allergen'), and `category`.
             4. Ordering: Order it from most to least concerning based on current scientific consensus.

            OUTPUT: Return ONLY the raw JSON array.
        """
    # Send image + prompt to Gemini model for analysis
    response = model.generate_content(
        [
            prompt,
            {"mime_type": image.mimetype, "data": image_bytes}
        ]
    )

    # clean data before sending back to frontend
    try: 
        response_text = response.text.strip()

        # Remove markdown code fences if the model ignored the prompt
        if response_text.startswith("```") and response_text.endswith("```"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        # Convert the string into a real Python list/object
        structured_data = json.loads(response_text)
        
    except: 
        response_text = "Error: Could not process the image. Please try again with a clearer image of the ingredients list."


    # Return the analysis results as JSON
    return jsonify({"structured_data": structured_data})
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)