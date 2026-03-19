from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx

app = Flask(__name__)
CORS(app)

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

@app.route('/')
def home():
    return "AI Backend Running"

if __name__ == '__main__':
    app.run()
