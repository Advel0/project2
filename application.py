from time import strftime, localtime
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_socketio import SocketIO, send

class Channel:
    def __init__(self, name):
        self.name = name
        self.users=[]
        self.messages=[]
    def add_message(self, message):
        self.messages.append(message)

class User:
    def __init__(self, name):
        self.name = name
        self.avaible_channels = []
    def enter_channel(channel):
        self.avaible_channels.append(channel)
        channel.users.append(self)

class Message:
    def __init__(self, user, text, time):
        self.user = user
        self.text = text
        self.time = time

channels = [Channel('news'), Channel('test')]
users = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

socketio = SocketIO(app)

# First page. User have to enter thier name or get acces to the dialogues
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dialogues'))

    return render_template('index.html')


#Log out?I believe simple enough
@app.route('/log-out')
def log_out():
    session.pop('user', None)
    return redirect(url_for('index'))

# Second PAge. Dialogues. If user tries to get acces without entereing a name he
# redirects to the start Page
@app.route('/dialogues', methods=['POST', 'GET'])
def dialogues():
    if request.method == 'POST':
        name = request.form.get('name')
        session['user'] = name
        return render_template('dialogues.html')

    if request.method == 'GET':
        if 'user' in session:
            return render_template('dialogues.html')
        if len(channels[0].messages) > 0:
            return redirect(url_for('index', {'messages':channels[0].messages}))

    return redirect(url_for('index'))

@socketio.on('message')
def message(data):
    time = strftime('%a-%d %I:%M%p', localtime())
    message = Message('advel', data, time)
    channels[0].add_message(message)
    print(channels[0].name)
    send({'message': message.text, 'username': message.user, 'time':time}, broadcast=True)
if __name__ == '__main__':
    socketio.run(app, Debug=True)
