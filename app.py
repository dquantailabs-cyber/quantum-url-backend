from flask import Flask, jsonify, request, redirect, render_template
from flask_cors import CORS
from quantum_logic import generate_quantum_code
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Database setup
def init_db():
    conn = sqlite3.connect('urls.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            short_code TEXT PRIMARY KEY,
            original_url TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    # Render HTML page from templates folder
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    long_url = data.get('url')
    custom_alias = data.get('alias')
    if not long_url:
        return jsonify({"error": "URL required"}), 400
    
    code = custom_alias or generate_quantum_code()
    
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    while True:
        cursor.execute("SELECT short_code FROM urls WHERE short_code=?", (code,))
        if not cursor.fetchone():
            break
        code = generate_quantum_code()
    
    cursor.execute("INSERT INTO urls (short_code, original_url) VALUES (?, ?)", (code, long_url))
    conn.commit()
    conn.close()
    
    return jsonify({"quantum_code": code})

@app.route('/<short_code>')
def redirect_url(short_code):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_code=?", (short_code,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return redirect(result[0])
    return "Short link not found", 404

if __name__ == '__main__':
    # Use dynamic port for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
