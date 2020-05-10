from time import strftime, localtime
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_socketio import SocketIO, send
import  json


class Channel:
    def __init__(self, name):
        self.name = name
        self.users=[]
        self.messages=[]
    def add_message(self, message):
        self.messages.append(message)
    def get_messages(self):
        messages=[]
        for message in self.messages:
            temp = {'username': message.user, 'text': message.text, 'time':message.time}
            messages.append(temp)
        return messages


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

# Global variables
channels = [Channel('news'), Channel('test')]
users = []

# Server settings
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
socketio = SocketIO(app)

# First page. User have to enter thier name or get acces to the dialogues
@app.route('/')
def index():
    if 'user_name' in session:
        return redirect(url_for('dialogues'))
    return render_template('index.html')


#Log out?I believe simple enough
@app.route('/log-out')
def log_out():
    session.pop('user_name', None)
    return redirect(url_for('index'))

# Second PAge. Dialogues. If user tries to get acces without entereing a name he
# redirects to the start Page
@app.route('/dialogues', methods=['POST', 'GET'])
def dialogues():
    messages = channels[0].get_messages()

    if request.method == 'POST':
        name = request.form.get('name')
        session['user_name'] = name
        return render_template('dialogues.html', data=json.dumps(messages))

    if request.method == 'GET':
        if 'user_name' in session:
            return render_template('dialogues.html', data=json.dumps(messages))

    return redirect(url_for('index'))


# Resonging on event messsage
@socketio.on('message')
def message(data):
    # Getting variables
    time = strftime('%a-%d %I:%M%p', localtime())
    message = Message(session['user_name'], data, time)
    #Creating a message
    channels[0].add_message(message)
    # Deplo
    send({'message': message.text, 'username': message.user, 'time':time}, broadcast=True)
if __name__ == '__main__':
    socketio.run(app, Debug=True)
