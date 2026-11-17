from flask import Flask, jsonify, request
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient("mongodb+srv://careercraft_rag:CareerCraft2026@raghavi.nir5itj.mongodb.net/")
db = client["careercraftDB"]

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

    return jsonify({
        "message": "Data Received",
        "received_data": data
    })

@app.route("/dbtest")
def dbtest():

    try:
        client.admin.command("ping")

        return jsonify({
            "message": "MongoDB Connected Successfully"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
        
if __name__ == "__main__":
    app.run(debug=True)