from dependency import *

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user_data = collection.find_one({'_id': user_id})
    return User(user_id)

app.secret_key = 'Sentiment@Analyzer@2023!!'

class User(UserMixin):
    def __init__(self, user_id):

        self.id = user_id

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

@app.route('/')
def page():
    return render_template('about_us.html')

@app.route('/userpage')
def userpage():
    return render_template('userpage.html')

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
    return render_template('about_us.html') 

@app.route('/LoginSingUp')
def logreg():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('about_us.html')


@app.route('/contact')
def contact():
    return render_template('contactus.html')


@app.route('/textsentiment')
def sentimenttext():
    return render_template('textsentiment.html')


@app.route('/filesentiment')
def sentimentfile():
    return render_template('file.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        # Registration process
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        date = datetime.now()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        existing_user = collection.find_one({'EMAIL_ID': email})
        if existing_user:
            error_message = 'User with the same email already exists!!'
            return render_template('index.html', error_message=error_message)

        user_data = {
            "USERNAME": name,
            "EMAIL_ID": email,
            "CREATED_DATE": date,
            "PASSWORD": hashed_password
        }
        collection.insert_one(user_data)
        print(user_data)

        return redirect(url_for('registration_success', name=name))
    return render_template('index.html')


@app.route('/registration_success')
def registration_success():
    name = request.args.get('name')
    return render_template('registration_success.html', name=name)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        date = datetime.now()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = collection.find_one({'EMAIL_ID': email, 'PASSWORD': hashed_password})
        if user:
            name=user['USERNAME']
            session['email'] = email
            user_obj = User(str(user['_id']))
            login_user(user_obj)
            data = collection1.insert_one({
                'USER_ID': user['_id'],
                'USERNAME': user['USERNAME'],
                'EMAIL_ID': user['EMAIL_ID'],
                'LOGINDATE_TIME': date
            })
            return render_template('userpage.html',name=name)
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
def textsentiment():
    if 'email' not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401
    text = request.form.get('text')
    file_upload_time = datetime.now()
    if not text:
        return jsonify({"error": "Text parameter is missing."}), 400
    if len(text) > 500:
        return jsonify({"error": "Text exceeds the maximum limit of 500 characters."}), 400
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
    text = text.lower()
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    text = ' '.join(filtered_words)
    tx = TextBlob(text)
    correct_sentence = tx.correct().raw
    analysis = TextBlob(correct_sentence)
    score = round(analysis.sentiment.polarity, 2)

    if score > 0:
        sentiment = 'Positive'
    elif score < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    email = session['email']
    user = collection.find_one({'EMAIL_ID': email})
    sentiment_data = {
        "USER_ID": user['_id'],
        "TEXT": correct_sentence,
        "FILTERED TEXT":filtered_words,
        "FILE_NAME": text,
        "SENTIMENT_SCORE": score*100,
        "SENTIMENT_RESPONSE": sentiment,
        "FILE_TYPE": "TEXT",
        "FILE_UPLOAD_DATETIME": file_upload_time,
        "SENTIMENT_DATETIME": datetime.now()
    }
    collection3.insert_one(sentiment_data)
    score_percentage = score * 100

    response = {
        "yourtext": text,
        "Score": str(score_percentage) + " " + "Out Of 100",
        "Sentiment": sentiment,
        "Text": correct_sentence,
        "FILE_TYPE": "TEXT",
        "Result_date_time": datetime.now()
    }

    return jsonify(response), 200

WORD = "WORD"
CSV_EXCEL = "CSV/EXCEL"

@app.route('/predictsentimentfile', methods=["POST","GET"])
def filesentiment():
    if 'email' not in session:
        return jsonify({"error": "Unauthorized. Please log in."}), 401

    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    file_upload_time = datetime.now()
    file_name = file.filename.split('.')[-1].lower()

    if file.filename == '':
        return "No file selected", 400

    if file_name in ['doc', 'docx']:
        type = WORD
        doc = docx.Document(file)
        full_text = ""
        for paragraph in doc.paragraphs:
            full_text += paragraph.text + "\n"
        full_text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", full_text)
        analysis = TextBlob(full_text)
        score = round(analysis.sentiment.polarity, 2)
        if score>0:
            sentiment='Positive'
        elif score<0:
            sentiment='Negative'
        else:
            sentiment='Neutral'
        text_tokens = nltk.tokenize.word_tokenize(full_text) 
        st_word = set(stopwords.words('english')) 
        tokens_without_sw = [word for word in text_tokens if not word.lower() in st_word]
        words4 = [w.replace('liked', 'like').replace('relaxed', 'relax').replace('relaxing', 'relax').replace('excitinging', 'excited') for w in tokens_without_sw]
        zxc = ' '.join(word for word in words4 if len(word) > 3)
        zxcc = re.sub(r"[^a-zA-Z ]", "", zxc)
        email = session['email']
        user = collection.find_one({'EMAIL_ID': email})
        sentiment_data = {
            "USER_ID": user['_id'],
            "FILE_NAME": file.filename,
            "FILE_TYPE": type,
            "SENTIMENT_SCORE": score*100,
            "SENTIMENT_RESPONSE": sentiment,
            "FILE_UPLOAD_DATETIME": file_upload_time,
            "WORDCLOUD": zxcc,
            "SENTIMENT_DATETIME": datetime.now()
        }
        print(sentiment_data)
        collection3.insert_one(sentiment_data)
        temp = {"FILE_TYPE":type,"SENTIMENT_SCORE":score*100,"SENTIMENT_RESPONSE": sentiment,"WORDCLOUD": zxcc,"SENTIMENT_DATETIME": datetime.now()}
    elif file_name in ['xls', 'xlsx', 'csv']:
        type = CSV_EXCEL
        col_name = request.form.get('column_name')
        data = pd.read_excel(file) if file_name in ['xls', 'xlsx'] else pd.read_csv(file)
        df = pd.DataFrame(data)
        if col_name not in df.columns:
            temp="Column name not found in the file."
            return temp
        comment_list=df[col_name].values.tolist()
        newtexttoken=[]
        for i in comment_list:
            text_tokens = nltk.tokenize.word_tokenize(i)
            newtexttoken.append(text_tokens)
        newlist=[]
        for i in newtexttoken:
            for z in i:
                newlist.append(z.lower())
        st_word=stopwords.words('english')
        tokens_without_sw= [word for word in newlist if not word in st_word]
        token5=[]
        for sentence in tokens_without_sw:
            text3 = sentence.split('ing')    
            for i in text3:
                token5.append(i)
        words = [w.replace('liked', 'like') for w in token5]
        words2 = [w.replace('relaxed', 'relax') for w in words]
        words3 = [w.replace('relaxing', 'relax') for w in words2]
        words4 = [w.replace('excitinging', 'excited') for w in words3]
        zxc=""
        xcvv=[x for x in words4 if len(x)>3]
        zxc=' '.join(word for word in xcvv)
        zxcc=re.sub(r"[^a-zA-Z ]", "", zxc)

        df['Sentiment_score'] = df[col_name].apply(lambda x: TextBlob(x).sentiment.polarity)
        
        df['Label'] = np.where(df['Sentiment_score'] > 0, 'Positive', (np.where(df['Sentiment_score'] < 0, 'Negative', 'Neutral')))
        
        total = len(df)
        positive = len(df[df['Label'] == 'Positive'])
        negative = len(df[df['Label'] == 'Negative'])
        neutral = len(df[df['Label'] == 'Neutral'])

        positive_percentage = round((positive / total) * 100, 2)
        negative_percentage = round((negative / total) * 100, 2)
        neutral_percentage = round((neutral / total) * 100, 2)

        if positive_percentage > negative_percentage and positive_percentage > neutral_percentage:
            sentiment = 'Positive'
        elif negative_percentage > positive_percentage and negative_percentage > neutral_percentage:
            sentiment = 'Negative'
        elif neutral_percentage > positive_percentage and neutral_percentage > negative_percentage:
            sentiment = 'Neutral'
        else:
            sentiment = 'Neutral'

        score = {"Positive": positive_percentage, "Negative": negative_percentage, "Neutral": neutral_percentage}

        email = session['email']
        user = collection.find_one({'EMAIL_ID': email})
        sentiment_data = {
            "USER_ID": user['_id'],
            "FILE_NAME": file.filename,
            "FILE_TYPE": type,
            "SENTIMENT_RESPONSE": sentiment,
            "TOTAL_COMMENTS": total,
            "POSITIVE_COMMENTS": positive,
            "NEGATIVE_COMMENTS": negative,
            "NEUTRAL_COMMENTS": neutral,
            "SENTIMENT_SCORE": score,
            "FILE_UPLOAD_DATETIME": file_upload_time,
            "SENTIMENT_DATETIME": datetime.now(),
            "WORDCLOUD":zxcc
        }
        print(sentiment_data)
        collection3.insert_one(sentiment_data)
        df=df[[col_name,'Label']]
        if "export" in request.args:
            try:
                csv = df.to_csv(index=False)
                print(csv)
                response = Response(csv, content_type="text/csv")
                response.headers["Content-Disposition"] = "attachment; filename=SentimentFile.csv"
                print("Download request handled")
                return response
            except:
                return jsonify("Unauthorized Access")
        else:
            temp = {"FILE_TYPE": type,
                "SENTIMENT_RESPONSE": sentiment,
                "TOTAL_COMMENTS": total, 
                "POSITIVE_COMMENTS": positive,
                "NEGATIVE_COMMENTS": negative,
                "NEUTRAL_COMMENTS": neutral,
                "SENTIMENT_SCORE": score,
                "data":df.values.tolist(),
                "SENTIMENT_DATETIME": datetime.now(),
                "WORDCLOUD":zxcc}

    return jsonify(temp), 200

@app.route('/userhistorytable')
def userhistorytable():
    email = session['email']
    user = collection.find_one({'EMAIL_ID': email})
    user_id=user['_id']
    query = [
    {
        '$match': {'USER_ID': user_id}
    },{'$project':{'_id':0,
                  "FILE_NAME":1,
                   "FILE_TYPE":1,
                   "FILE_UPLOAD_DATETIME":1,
                  "SENTIMENT_RESPONSE":1,
                  "SENTIMENT_SCORE":1
                  }}
    ]
    df = pd.DataFrame(list(collection3.aggregate(query)))
    df['FILE_UPLOAD_DATETIME']=pd.to_datetime(df['FILE_UPLOAD_DATETIME'])
    df['FILE_UPLOAD_DATETIME']=df['FILE_UPLOAD_DATETIME'].dt.strftime('%b %d,%Y')
    df=df.sort_values(by='FILE_UPLOAD_DATETIME',ascending=False)
    df=df[['FILE_NAME','FILE_TYPE','FILE_UPLOAD_DATETIME','SENTIMENT_RESPONSE','SENTIMENT_SCORE']]
    temp={'data':df.values.tolist()}
    return json.dumps(temp)

@app.route('/userhistorycard')
def userhistorycard():
    email = session['email']
    user = collection.find_one({'EMAIL_ID': email})
    user_id = user['_id']

    query = [
        {
            '$match': {'USER_ID': user_id}
        },
        {
            "$group": {
                "_id": {
                    "$cond": [
                        { "$in": ["$FILE_TYPE", ["WORD", "CSV/EXCEL"]] },
                        "FILE",
                        "TEXT"
                    ]
                },
                "count": { "$sum": 1 }
            }
        }
    ]
    df = pd.DataFrame(list(collection3.aggregate(query)))
    if df.empty:
        temp = {'Text': 0, 'File': 0}
    else:
        if 'TEXT' in df['_id'].values and 'FILE' not in df['_id'].values:
            temp = {'Text': str(df[df['_id'] == 'TEXT']['count'].iloc[0]), 'File': 0}
        elif 'TEXT' not in df['_id'].values and 'FILE' in df['_id'].values:
            temp = {'Text': 0, 'File': str(df[df['_id'] == 'FILE']['count'].iloc[0])}
        else:
            temp = {'Text': str(df[df['_id'] == 'TEXT']['count'].iloc[0]), 'File': str(df[df['_id'] == 'FILE']['count'].iloc[0])}
    return json.dumps(temp)


if __name__ == "__main__":
    # recognize_speech()
    app.run(debug=True)