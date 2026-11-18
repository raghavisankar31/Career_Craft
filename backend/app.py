from flask import Flask, jsonify, request
from pymongo import MongoClient
app = Flask(__name__)
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

if __name__ == "__main__":
    app.run(debug=True)