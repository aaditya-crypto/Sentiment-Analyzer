from dependency import *

login_manager = LoginManager(app)
app.secret_key = 'Sentiment@Analyzer@2023!!'

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@app.route('/')
def page():
    return render_template('dashboard.html')

@app.route('/success')
def ful():
    return render_template('successfulmsg.html')

@app.route('/wordcloud')
def wordcloud():
    return render_template('wordcloud.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('reglog')) 

@app.route('/reglog')
def logreg():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('about_us.html')

@app.route('/homepage')
def homepage():
    return render_template('dashboard.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')


@login_manager.user_loader
def load_user(user_id):
    user_data = collection.find_one({'_id': user_id})
    return User(user_id)

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
            session['email'] = email
            user_obj = User(str(user['_id']))
            login_user(user_obj)
            data = collection1.insert_one({
                'USER_ID': user['_id'],
                'USERNAME': user['USERNAME'],
                'EMAIL_ID': user['EMAIL_ID'],
                'LOGINDATE_TIME': date
            })
            return render_template('wordcloud.html')
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render_template('index.html', error_message=error_message)
        
@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['msg']
    date=datetime.now()
    data1 = collection2.insert_one({
                'USERNAME': name,
                'MESSAGE': message,
                'EMAIL_ID':email,
                'LOGINDATE_TIME': date
            })
    print(data1)
    response = {'status': 'success', 'message': 'Form submitted successfully'}
    return render_template('formsubmission.html',name=name)


@app.route('/predictsentimenttext', methods=["POST"])
@login_required
def textsentiment():
    if 'email' not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "Text parameter is missing."}), 400
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
    analysis = TextBlob(text)
    score = round(analysis.sentiment.polarity, 2)
    sentiment = 'Positive' if score > 0 else 'Negative'
    email = session['email']
    user = collection.find_one({'EMAIL_ID': email})
    sentiment_data = {
        "USER_ID": user['_id'],
        "TEXT": text,
        "SENTIMENT_SCORE": score,
        "SENTIMENT_RESPONSE": sentiment,
        "SENTIMENT_DATETIME": datetime.now()
    }
    collection3.insert_one(sentiment_data)
    response = {
        "Score": score,
        "Sentiment": sentiment,
        "Text": text,
        "message": "Data Inserted Successfully"
    }

    return jsonify(response), 200

def process_command(command):
    if "website" in command:
        webbrowser.open_new_tab('http://127.0.0.1:5000/')
    elif "home" in command:
        webbrowser.open_new_tab('http://127.0.0.1:5000/homepage')
    elif "about" in command:
        webbrowser.open_new_tab('http://127.0.0.1:5000/aboutus')
    elif "contact" in command:
        webbrowser.open_new_tab('http://127.0.0.1:5000/contact')
    elif "login" in command:
        webbrowser.open_new_tab('http://127.0.0.1:5000/reglog')
    elif "signup" in command:
        webbrowser.open_new_tab('http://127.0.0.1:5000/reglog')

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source) 
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        process_command(command)

    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print("Error with the recognition service; {0}".format(e))

if __name__ == "__main__":
    recognize_speech()
    app.run(debug=True)


