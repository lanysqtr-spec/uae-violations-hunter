import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "<h1>Server is Live!</h1><p>Ready for next steps.</p>"

if __name__ == '__main__':
    # السطر ده هو اللي Render مستنيه عشان يربط الـ Port
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
