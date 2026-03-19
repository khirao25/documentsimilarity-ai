from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/compare', methods=['POST'])
def compare():
    text1 = request.form['text1']
    text2 = request.form['text2']

    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]

    return jsonify({'similarity': round(similarity * 100, 2)})

@app.route('/')
def home():
    return "AI Backend Running"

if __name__ == '__main__':
    app.run()
