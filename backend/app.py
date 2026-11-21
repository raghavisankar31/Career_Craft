from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://careercraft_rag:CareerCraftDB2026@raghavi.nir5itj.mongodb.net/")
db = client["careercraftDB"]

users_collection = db["users"]

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)