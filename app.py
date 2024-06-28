from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
from flask_cors import CORS
import sqlite3
import uuid
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'store.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS purchases (
                        id TEXT PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        credit_card TEXT,
                        item_id INTEGER,
                        item_name TEXT,
                        item_price INTEGER
                    )''')
        conn.commit()

# Initialize the database at the start of the application
init_db()

@app.route('/')
def index():
    return render_template('store.html')

@app.route('/buy', methods=['POST'])
def buy():
    try:
        data = request.get_json()
        print("Incoming data:", data)  # Debugging line

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        credit_card = data.get('credit_card')
        item_id = data.get('item_id')

        print(f"first_name: {first_name}, last_name: {last_name}, email: {email}, credit_card: {credit_card}, item_id: {item_id}")  # Debugging line

        if not all([first_name, last_name, email, credit_card, item_id]):
            return jsonify({'error': 'Missing data in request'}), 400

        items = {
            1: ('Nikes', 500),
            2: ('Adidas', 600),
            3: ('Raf Simmons', 1000)
        }

        if int(item_id) not in items:
            return jsonify({'error': 'Invalid item ID'}), 400

        item_name, item_price = items[int(item_id)]

        purchase_id = str(uuid.uuid4())

        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO purchases (id, first_name, last_name, email, credit_card, item_id, item_name, item_price) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (purchase_id, first_name, last_name, email, credit_card, item_id, item_name, item_price))
            conn.commit()

        return jsonify({'purchase_id': purchase_id, 'item_name': item_name, 'item_price': item_price})
    except Exception as e:
        print("Error:", e)  # Debugging line
        return jsonify({'error': 'An error occurred processing your request'}), 500

@app.route('/purchases', methods=['GET'])
def get_purchases():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM purchases')
        purchases = c.fetchall()

    return jsonify(purchases)

@app.route('/images/<path:filename>')
def send_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    app.run(debug=True, port=6969)
