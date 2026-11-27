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
try:
    ai_client = genai.Client()
except:
    ai_client = None
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
You are an expert Human Resources professional, resume writer, and ATS optimization specialist.

Your task is to transform raw user information into a highly professional resume.

Instructions:

1. Correct grammar, spelling mistakes, and sentence structure.
2. Rewrite informal language into professional resume language.
3. Remove unnecessary, personal, casual, repetitive, or irrelevant information.
4. Use strong action-oriented resume wording.
5. Organize the content into:
   - Professional Summary
   - Skills
   - Experience
   - Education
   - Projects
6. Make the resume ATS-friendly.
7. Never invent qualifications, skills, jobs, or certifications.
8. Return only valid HTML with inline CSS styling.

Selected Template:
{template_style}

Raw User Information:
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