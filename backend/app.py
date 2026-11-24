import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests from your frontend pages

# MongoDB Setup
client = MongoClient("mongodb+srv://careercraft_rag:CareerCraftDB2026@raghavi.nir5itj.mongodb.net/")
db = client["careercraftDB"]
users_collection = db["users"]

# Initialize Google GenAI Client
# (Make sure your GEMINI_API_KEY environment variable is set in your terminal)
ai_client = genai.Client()

@app.route("/")
def home():
    return "Backend Running Successfully"

@app.route("/student")
def student():
    return jsonify({
        "name": "Raghavi",
        "department": "Biology",
        "project": "Career Craft"
    })

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    existing_user = users_collection.find_one({
        "email": data["email"]
    })

    if existing_user:
        return jsonify({
            "message": "Email already exists"
        })

    users_collection.insert_one({
        "email": data["email"],
        "username": data["username"],
        "password": data["password"]
    })

    return jsonify({
        "message": "User Registered Successfully"
    })

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = users_collection.find_one({
        "email": data["email"]
    })

    if not user:
        return jsonify({
            "message": "User Not Found"
        })

    if user["password"] == data["password"]:
        return jsonify({
            "message": "Login Successful"
        })

    return jsonify({
        "message": "Invalid Password"
    })

@app.route("/dbtest")
def dbtest():
    try:
        client.server_info()
        return jsonify({
            "message": "MongoDB Connected Successfully"
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    try:
        req_data = request.get_json()
        template_style = req_data.get("template", "ats-classic")
        linkedin_text = req_data.get("linkedin_data", "")

        if not linkedin_text:
            return jsonify({"success": False, "message": "No LinkedIn data provided."}), 400

        # System prompt instructing Gemini to format the resume with clean inline design styles
        prompt = f"""
        You are an expert professional CV writer and web designer. 
        Convert the raw LinkedIn data below into a fully styled, beautifully designed HTML resume snippet.
        
        Selected Template Theme: {template_style}
        
        Formatting & Design Rules:
        1. Return ONLY valid HTML elements (like <h2>, <h3>, <p>, <ul>, <li>, <strong>) wrapped inside a clean container div.
        2. Apply inline CSS styles (such as matching color themes, proper padding, clean font families, and subtle borders) so it looks like a professional, print-ready document immediately.
        3. Organize into clear sections: Contact/Header, Summary, Experience, Skills, and Education.
        4. Do NOT include markdown code blocks (like ```html) in your response; return raw HTML string content directly.
        
        Raw LinkedIn Data:
        {linkedin_text}
        """

        # Using gemini-3.8-flash for rapid response generation
        response = ai_client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )

        # Clean up any accidental markdown code markers from the output string
        html_output = response.text.replace("```html", "").replace("```", "").strip()

        return jsonify({
            "success": True,
            "resume_html": html_output
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)