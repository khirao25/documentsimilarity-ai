from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS history (email TEXT, score TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?)", (email, password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User created"})

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})

@app.route('/save', methods=['POST'])
def save():
    email = request.form['email']
    score = request.form['score']

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?,?)", (email, score))
    conn.commit()
    conn.close()

    return jsonify({"message": "Saved"})

@app.route('/history', methods=['POST'])
def history():
    email = request.form['email']

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT score FROM history WHERE email=?", (email,))
    data = c.fetchall()
    conn.close()

    return jsonify(data)

@app.route('/')
def home():
    return "Backend Running"

if __name__ == '__main__':
    app.run()
