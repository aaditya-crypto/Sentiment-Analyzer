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
import re
from flask_cors import CORS
from textblob import TextBlob
from flask import Flask, jsonify, request
import random
from pymongo import MongoClient
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from datetime import datetime
import hashlib
import speech_recognition as sr
import webbrowser
import threading


print("Libraries Imported Successfully !!")

app = Flask(__name__,template_folder="template")
CORS(app)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["PROJECT"]
collection=db['USER_MASTER']
collection1=db['LOGIN_TRACK']
collection2=db['CONTACT_US']
collection3=db['SENTIMENT_TRACK']