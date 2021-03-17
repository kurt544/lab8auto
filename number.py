from flask import Flask, Response, jsonify
import math
import json

app = Flask(__name__)

#the main root URL route
@app.route('/')
def index():
    return "Welcome to the project API"

@app.route('/is-prime/<int:n>')
def prime_check(n):
    number = isinstance(n, int)
    if number == 1:
        return jsonify(input=n, output=False)
    elif (number==2):
        return jsonify(input=n, output=True)
    else:
        for i in range(2,n):
            if(number % i==0):
               return jsonify(input=n, output=False)
        return jsonify(input=n, output=True)