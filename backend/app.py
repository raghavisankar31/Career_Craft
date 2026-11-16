from flask import Flask, jsonify, request

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)