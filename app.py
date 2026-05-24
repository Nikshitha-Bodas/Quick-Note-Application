from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Create database
def init_db():

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()


# Home Page
@app.route('/')
def home():

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes")

    notes = cursor.fetchall()

    conn.close()

    return render_template('index.html', notes=notes)


# Add Note
@app.route('/add', methods=['POST'])
def add_note():

    data = request.get_json()

    note = data['note']

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (note,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Note added successfully'
    })


# Delete Note
@app.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Note deleted successfully'
    })


# Edit Note
@app.route('/edit/<int:id>', methods=['POST'])
def edit_note(id):

    data = request.get_json()

    updated_note = data['note']

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notes SET content=? WHERE id=?",
        (updated_note, id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Note updated successfully'
    })


if __name__ == '__main__':
    app.run(debug=True)