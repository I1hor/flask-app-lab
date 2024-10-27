from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def resume():
    return render_template('resume.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/education')
def education():
    return render_template('education.html')

if __name__ == '__main__':
    app.run(debug=True)
