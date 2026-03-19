from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import requests

app = Flask(__name__)
CORS(app)

# 🔐 GOOGLE CONFIG (REPLACE THESE)
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "https://documentsimilarity-ai.onrender.com/google"

# 📂 FILE READER
def read_file(file):
    try:
        if file.filename.endswith(".txt"):
            return file.read().decode("utf-8", errors="ignore")

        elif file.filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text

        elif file.filename.endswith(".docx"):
            doc = docx.Document(file)
            return "\n".join([p.text for p in doc.paragraphs])

    except:
        return ""

    return ""

# 🤖 AI COMPARE
@app.route('/compare', methods=['POST'])
def compare():
    try:
        file1 = request.files['file1']
        file2 = request.files['file2']

        text1 = read_file(file1)
        text2 = read_file(file2)

        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]

        return jsonify({'similarity': round(similarity * 100, 2)})

    except Exception as e:
        return jsonify({'error': str(e)})

# 👤 SIMPLE LOGIN (TEMP)
users = {}

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']

    users[email] = password
    return jsonify({"status": "success"})

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if email in users and users[email] == password:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

# 🌐 GOOGLE LOGIN
@app.route('/google')
def google_login():
    code = request.args.get("code")

    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    token_res = requests.post(token_url, data=data).json()
    access_token = token_res.get("access_token")

    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"access_token": access_token}
    ).json()

    email = user_info.get("email")

    return redirect("https://documentsimilarity.com?user=" + email)

# 🏠 HOME
@app.route('/')
def home():
    return "AI Backend Running"

if __name__ == '__main__':
    app.run()
