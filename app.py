from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Initialize the database
def init_db():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = [{'id': row[0], 'title': row[1], 'content': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(notes)

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.json
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (data['title'], data['content']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note added successfully'}), 201

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note deleted successfully'})

if __name__ == '__main__':
    init_db()
    # Get the port from the environment variable or default to 10000
    port = int(os.environ.get("PORT", 10000))
    # Run the Flask app on all available interfaces (0.0.0.0)
    app.run(host="0.0.0.0", port=port, debug=True)
