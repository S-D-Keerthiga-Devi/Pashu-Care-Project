from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
import os
from PIL import Image
import re
from flask_cors import CORS
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin  # Use cross_origin for Blueprints
import groq
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configure GenAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Flask app
app = Flask(__name__)
CORS(app)

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})  # Enable CORS for /chat route

@app.route('/')
def home():
    return render_template('services.html')

@app.route('/AI_assistant')
def get_assistant():
    return render_template('AI_assistant.html')

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')


@app.route('/AI_assistant', methods=['POST'])
def assistant():
    if 'file' not in request.files:
        return jsonify({"response": "No file uploaded"}), 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({"response": "Empty filename"}), 400

    try:
        bot_response = image_analyser(uploaded_file) if uploaded_file else "Invalid file input"
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"response": f"Error processing image: {str(e)}"}), 500

def image_analyser(uploaded_file):
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Open the image for processing
    image = Image.open(uploaded_file)

    prompt = """
    You are a professional veterinarian AI trained to analyze pet injuries from images. When provided with an image of an injured pet, carefully examine the injury type, severity, and affected body part. Determine whether the injury is a minor wound, swelling, fracture, infection, or any other medical condition.

    Provide an instant remedy with step-by-step first-aid treatment that the owner can apply at home before seeking professional veterinary care. If the injury is severe, recommend urgent veterinary attention.

    Key points:
    - Type of injury (cuts, wounds, swelling, burns, fractures, infections, etc.)
    - Severity level (mild, moderate, or severe)
    - Immediate first-aid solutions (cleaning, disinfecting, bandaging, soothing, etc.)
    - Home care tips for pain relief and monitoring the pet's condition
    - When to visit a vet for further medical assistance

    Make sure your response is detailed yet easy to follow, with a friendly and caring tone.
    """

    formatted_prompt = """
        Format the response using proper HTML elements. Structure the content with:
        - <h2> for major headings
        - <h3> for subheadings
        - <p> for general text
        - <ul> and <li> for lists

        Ensure that:
        1. The response does NOT contain Markdown formatting or backticks.
        2. The response is clean, professional, and easy to read.
        3. The response only uses valid HTML elements.

        Example Structure:
        <h2>Veterinary Assessment</h2>
        <p>Based on the image, the dog appears to be in distress...</p>
        <h3>Possible Concerns</h3>
        <ul>
        <li>Dehydration</li>
        <li>Injury</li>
        </ul>

        Provide the response strictly in this format.
    """


    response = model.generate_content([formatted_prompt, image, prompt])

    return response.text  # Returns clean HTML content


@app.route('/currentdiet', methods=['POST'])
def current_diet():
    if 'file' not in request.files:
        return jsonify({"response": "No file uploaded"}), 400

    breed = request.form.get('breed')
    age = request.form.get('age')
    weight = request.form.get('weight')
    health = request.form.get('health')
    uploaded_file = request.files.get('file')

    if not uploaded_file or uploaded_file.filename == '':
        return jsonify({"response": "Empty filename"}), 400

    try:
        bot_response = current_diet_analyser(breed, age, weight, health, uploaded_file)
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"response": f"Error processing image: {str(e)}"}), 500

    
def current_diet_analyser(breed, age, weight, health, uploaded_file):
    model = genai.GenerativeModel("gemini-2.0-flash")
    image = Image.open(uploaded_file)

    prompt = """
    Analyze my pet's current diet based on the provided food image, breed, age, weight, and health conditions. Extract key nutritional details from the food, including ingredient composition, protein and fat content, carbohydrate estimation, and essential vitamins and minerals. Determine if the diet is nutritionally balanced and assess its suitability for my pet's breed, age, and health status. Identify any potential allergens, harmful additives, or deficiencies that may impact health. If the pet has specific conditions (e.g., obesity, allergies, kidney issues), evaluate whether this diet supports or worsens these conditions. Provide a nutritional score, highlight potential risks, and offer science-backed recommendations for improving the diet. Suggest alternative food options considering species-appropriate nutrition and balanced macronutrient ratios. Present the response as a structured, professional pet nutritionist report using clear headings and bullet points where necessary for readability.
    """

    formatted_prompt = """
        Format the response using proper HTML elements. Structure the content with:
        - <h2> for major headings
        - <h3> for subheadings
        - <p> for general text
        - <ul> and <li> for lists

        Ensure that:
        1. The response does NOT contain Markdown formatting or backticks.
        2. The response is clean, professional, and easy to read.
        3. The response only uses valid HTML elements.
        4. The response should be written from the perspective of a professional pet nutritionist.

        Example Structure:
        <h2>Pet Nutrition Analysis</h2>
        <p>Based on the provided food image and pet details, here is a comprehensive breakdown of the current diet.</p>
        
        <h3>Ingredient Composition</h3>
        <p>The food contains the following key ingredients:</p>
        <ul>
        <li>Protein source: Chicken (high-quality animal protein)</li>
        <li>Fats: Salmon oil (rich in omega-3 fatty acids)</li>
        <li>Carbohydrates: Rice (may be excessive for some breeds)</li>
        </ul>
        
        <h3>Nutritional Breakdown</h3>
        <ul>
        <li>Protein: 30% (Good for muscle development)</li>
        <li>Fat: 18% (Provides essential energy and supports coat health)</li>
        <li>Carbohydrates: Estimated at 35% (May be high for carnivorous diets)</li>
        <li>Vitamins & Minerals: Includes vitamin A, calcium, and taurine</li>
        </ul>

        <h3>Diet Classification</h3>
        <p>This diet is classified as <strong>balanced</strong>/<strong>unbalanced</strong> based on its nutritional profile.</p>

        <h3>Suitability for Breed, Age, and Health Status</h3>
        <p>Considering the pet's breed, age, and health conditions, this diet may be...</p>

        <h3>Potential Concerns</h3>
        <ul>
        <li>Contains potential allergens such as wheat and soy</li>
        <li>May have an imbalanced protein-to-fat ratio for this breed</li>
        <li>High carbohydrate content, which may not be ideal for certain pets</li>
        </ul>

        <h3>Recommendations for Improvement</h3>
        <p>To enhance this diet for optimal pet health, consider:</p>
        <ul>
        <li>Ensuring a higher quality protein source</li>
        <li>Reducing unnecessary carbohydrates</li>
        <li>Adding fresh whole foods like lean meat or vegetables</li>
        </ul>

        <h3>Alternative Food Options</h3>
        <p>Based on species-appropriate nutrition, consider the following alternatives:</p>
        <ul>
        <li>High-protein kibble with limited fillers</li>
        <li>Raw or homemade diets with balanced macronutrients</li>
        <li>Vet-recommended therapeutic diets for specific health conditions</li>
        </ul>

        <h3>Final Assessment</h3>
        <p><strong>Nutritional Score:</strong> 7.5/10</p>
        <p>Overall, this diet is <strong>suitable/needs improvement</strong> for your pet based on the analysis.</p>

        Provide the response strictly in this format, ensuring that it maintains a professional pet nutritionist perspective.
    """
    
    response = model.generate_content([formatted_prompt, breed, age, weight, health, image, prompt])

    return clean_html_response(response.text)

@app.route('/plandiet', methods=['POST'])
def plan_diet():
    if 'file' not in request.files:
        return jsonify({"response": "No file uploaded"}), 400

    breed = request.form.get('breed')
    age = request.form.get('age')
    weight = request.form.get('weight')
    health = request.form.get('health')
    uploaded_file = request.files.get('file')

    if not uploaded_file or uploaded_file.filename == '':
        return jsonify({"response": "Empty filename"}), 400

    try:
        bot_response = plan_your_diet(breed, age, weight, health, uploaded_file)
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"response": f"Error processing image: {str(e)}"}), 500

    
def plan_your_diet(breed, age, weight, health, uploaded_file):
    model = genai.GenerativeModel("gemini-2.0-flash")
    image = Image.open(uploaded_file)

    prompt = """
    Generate a structured pet diet plan based on the provided details (breed, age, weight, and health conditions). The plan should be balanced, scientifically backed, and tailored to meet the pet's specific nutritional needs. The plan should include:

    - Macronutrient Composition (Protein, Fats, Carbohydrates)
    - Essential Vitamins & Minerals (Calcium, Omega-3, Taurine, etc.)
    - Ideal Feeding Schedule (Meal frequency and portion sizes)
    - Recommended Food Sources (High-quality proteins, healthy fats,  and digestible carbs)
    - Specific Diet Adjustments based on health conditions (e.g., low-fat diet for pancreatitis, hypoallergenic diet for allergies, high-protein for active breeds)
    - Avoidable Ingredients (Harmful additives, toxic foods, and known allergens)
    - Hydration & Supplements (If required, such as probiotics, omega oils, or joint support)
    - Alternative Diet Options (Kibble, raw, homemade, or vet-prescribed diets)
    Final Assessment & Nutritionist's Advice
    Ensure the response is well-structured in HTML format using:

        <h2> for main headings
        <h3> for subheadings
        <p> for paragraphs
        <ul> and <li> for lists
    The output should be professional, readable, and resemble a real nutritionist's report. Avoid Markdown or backticks.

    Present the response as a structured, professional pet nutritionist report using clear headings and bullet points where necessary for readability with no backticks.
    """

    formatted_prompt = """
        Format the response using proper HTML elements. Structure the content with:
        - <h2> for major headings
        - <h3> for subheadings
        - <p> for general text
        - <ul> and <li> for lists

        Ensure that:
        1. The response does NOT contain Markdown formatting or backticks.
        2. The response is clean, professional, and easy to read.
        3. The response only uses valid HTML elements.
        4. The response should be written from the perspective of a professional pet nutritionist.

        Example Structure:
        <h2>Customized Pet Diet Plan</h2>
        <p>Based on the details provided, here is a scientifically formulated diet plan for your pet.</p>

        <h3>Macronutrient Composition</h3>
        <ul>
        <li><strong>Protein:</strong> 30-35% (Essential for muscle maintenance and overall health)</li>
        <li><strong>Fats:</strong> 15-20% (Supports energy levels and coat health)</li>
        <li><strong>Carbohydrates:</strong> Limited to 10-15% (For digestive ease and steady energy)</li>
        </ul>

        <h3>Recommended Food Sources</h3>
        <ul>
        <li><strong>High-Quality Proteins:</strong> Chicken, turkey, salmon, or lean beef</li>
        <li><strong>Healthy Fats:</strong> Fish oil, flaxseed, coconut oil</li>
        <li><strong>Digestible Carbs:</strong> Sweet potatoes, brown rice, quinoa</li>
        </ul>

        <h3>Ideal Feeding Schedule</h3>
        <ul>
        <li>Puppies: 3-4 small meals per day</li>
        <li>Adult Dogs: 2 balanced meals per day</li>
        <li>Seniors: 2 meals with added joint supplements</li>
        </ul>

        <h3>Diet Adjustments for Health Conditions</h3>
        <ul>
        <li><strong>For Obesity:</strong> Increase protein, reduce carbs, add fiber</li>
        <li><strong>For Allergies:</strong> Avoid grains, opt for hydrolyzed proteins</li>
        <li><strong>For Kidney Issues:</strong> Low-protein, low-phosphorus diet</li>
        </ul>

        <h3>Avoidable Ingredients</h3>
        <ul>
        <li>Artificial preservatives and food colorings</li>
        <li>Excessive salt, sugar, and corn-based fillers</li>
        <li>Toxic foods like chocolate, onions, and grapes</li>
        </ul>

        <h3>Hydration & Supplements</h3>
        <p>Ensure fresh water is always available. Consider adding probiotics for gut health and omega-3 for a shiny coat.</p>

        <h3>Alternative Diet Options</h3>
        <ul>
        <li>High-protein kibble with minimal fillers</li>
        <li>Raw diet with vet supervision</li>
        <li>Home-cooked meals with balanced nutrients</li>
        </ul>

        <h3>Final Assessment</h3>
        <p><strong>Overall Diet Score:</strong> 9/10</p>
        <p>This diet is highly suitable for your pet's breed and health condition. Ensure regular vet check-ups for optimal health.</p>

        Provide the response strictly in this format, ensuring that it maintains a professional pet nutritionist perspective.
    """
    
    response = model.generate_content([formatted_prompt, breed, age, weight, health, image, prompt])

    return clean_html_response(response.text)

def clean_html_response(response_text):
    """Remove unwanted Markdown formatting from AI-generated responses."""
    # Remove triple backticks and "html" tags around the content
    response_text = re.sub(r'```html', '', response_text)
    response_text = re.sub(r'```', '', response_text)

    return response_text.strip()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY is missing from environment variables.")

# Initialize Groq Client
groq_client = groq.Client(api_key=api_key)

def get_helpline_response(user_query):
    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": user_query}],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"🔥 ERROR: {e}")
        return f"Error: {str(e)}"

# Chatbot route inside chatbot_bp
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Invalid or missing 'message' field"}), 400

        user_query = data["message"].strip()
        bot_response = get_helpline_response(user_query)

        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"🔥 ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)