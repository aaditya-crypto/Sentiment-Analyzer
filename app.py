from flask import (
    Flask,
    g,
    redirect,
    render_template,
    flash,
    request,
    session,
    url_for,
    send_file,
    Response
)
import pymongo
import json
from flask_cors import CORS
from textblob import TextBlob
from flask import Flask, jsonify, request
import boto3
import random
from pymongo import MongoClient
from datetime import datetime
import hashlib

app = Flask(__name__,template_folder="template")
CORS(app)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["PROJECT"]
collection=db['USER_MASTER']
collection1=db['LOGIN_TRACK']

@app.route('/')
def page():
    return render_template('index.html')

@app.route('/success')
def ful():
    return render_template('successfulmsg.html')

@app.route('/registration', methods=['POST'])
def registration():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    date = datetime.now()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    existing_user = collection.find_one({'EMAIL_ID': email})
    if existing_user:
        error_message = 'User with the same email already exists!!'
        return render_template('index.html', error_message=error_message)
    else:
        user_data = {
            "USERNAME": name,
            "EMAIL_ID": email,
            "CREATED_DATE": date,
            "PASSWORD": hashed_password
        }
        collection.insert_one(user_data)
        print(user_data)
        return render_template('successfulmsg.html',name=name)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        date = datetime.now()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = collection.find_one({'EMAIL_ID': email, 'PASSWORD': hashed_password})
        if user:
            data = collection1.insert_one({
                'USER_ID': user['_id'],
                'USERNAME': user['USERNAME'],
                'EMAIL_ID': user['EMAIL_ID'],
                'LOGINDATE_TIME': date
            })
            return str(data.inserted_id)
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render_template('index.html', error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
