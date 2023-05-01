
from flask import Flask, request, jsonify
import sqlite3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Define event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    print('Received message: ' + data)
    emit('response', 'You said: ' + data)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')
# Define API endpoints
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Retrieve messages from database
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute('SELECT * FROM messages')
        messages = c.fetchall()
        conn.close()
        return jsonify(messages)
    elif request.method == 'POST':
        # Add message to database
        message = request.json['message']
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute('INSERT INTO messages (message) VALUES (?)', (message,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if request.method == 'GET':
        # Retrieve groups from database
        conn = sqlite3.connect('groups.db')
        c = conn.cursor()
        c.execute('SELECT * FROM groups')
        groups = c.fetchall()
        conn.close()
        return jsonify(groups)
    elif request.method == 'POST':
        # Create new group in database
        name = request.json['name']
        members = request.json['members']
        conn = sqlite3.connect('groups.db')
        c = conn.cursor()
        c.execute('INSERT INTO groups (name, members) VALUES (?, ?)', (name, members))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

# Set up SQL database
conn = sqlite3.connect('messages.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT)')
conn.commit()
conn.close()

conn = sqlite3.connect('groups.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, members TEXT)')
conn.commit()
conn.close()

if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug=True)