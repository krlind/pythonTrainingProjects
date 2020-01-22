from flask import Flask, escape, request, jsonify
import main

app = Flask(__name__)

@app.route('/')
def hello():
    response = main.callSearchApi()
    print(response)
    return jsonify(response)

#