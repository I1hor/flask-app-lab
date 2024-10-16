import os
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def main():
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

@app.route('/admin')
def admin():
    to_url = "/hi/administrator?age=45"
    to_url = url_for("greetings", name="administrator", age=25)
    return redirect(to_url)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
