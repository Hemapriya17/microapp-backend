from flask import Flask, request, jsonify, render_template
from Fmea import generate_fmea
from Fmea import store_fmea
from Fmea import getall_fmea
from Fmea import getone_fmea
from flask_cors import CORS
import pyrebase
import sys

app = Flask(__name__)
CORS(app, origins=["http://fewshotgpt.com"], methods=["GET", "POST", "PUT", "DELETE"])

config = {
  "apiKey": "AIzaSyBLErRf9_uUROpxmyvcmgVYOkcobzkVApk",
  "authDomain": "twinmo-microapp.firebaseapp.com",
  "databaseURL": "https://twinmo-747b2-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "twinmo-microapp",
  "storageBucket": "twinmo-microapp.appspot.com",
  "messagingSenderId": "93415347444",
  "appId": "1:93415347444:web:1278c4ee79ce9a042fbaa1",
  "measurementId": "G-R6L26ESX7Q"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route("/generate-fmea", methods=["POST"])
def handle_post_request1():
    return generate_fmea(request)


@app.route("/store-fmea", methods=["POST"])
def store_request():
    return store_fmea(request)

@app.route("/getall-fmea", methods=["GET"])
def getall_request():
    return getall_fmea(request)


@app.route("/getone-fmea", methods=["POST"])
def getone_request():
    return getone_fmea(request)


@app.route("/verify-token", methods=["POST"])
def verifytoken():
    token = request.json.get('token')
    print(token,file=sys.stderr)
    if not token:
        return jsonify({'error': 'Token is missing'}), 400

    else:
        decoded_token = auth.get_account_info(token)
     
        if(decoded_token):
            return jsonify({'status': "success"}), 200
        else:
            return jsonify({'status': "error"}), 400
   
    


if __name__ == '__main__':
    app.run(debug=True)
