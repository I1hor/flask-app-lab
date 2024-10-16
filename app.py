import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!', 200

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return f"This is your homepage ;) - {agent}  = "

@app.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', 0, int)

    return f"Welcome, {name} your age is {age}"

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
