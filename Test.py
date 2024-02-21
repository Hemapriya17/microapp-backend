from flask import Flask, request, jsonify, render_template
from auth import verify_token
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE"])



@app.route("/verify-token", methods=["POST"])
def verifytoken():
    return verify_token(request)


if __name__ == '__main__':
    app.run(debug=True)
