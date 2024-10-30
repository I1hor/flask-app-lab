from flask import request, redirect, url_for, render_template, abort, make_response, session, flash
from . import user_bp
from datetime import timedelta, datetime

@user_bp.route('/profile')
def get_profile():
    if "username" in session:
        username = session['username']
        return render_template("profile.html", username=username)
    return redirect(url_for('user.login'))

@user_bp.route("/login",  methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['login']
        session["username"] = username
        return redirect(url_for("user.get_profile"))
    flash("Invalid: session", "fail")
    return render_template("login.html")

@user_bp.route('/logout')
def logout():
    # Видалення користувача із сесії
    session.pop('username', None)
    session.pop('age', None)
    return redirect(url_for('user.get_profile'))


@user_bp.route('/')
def get_resume():
    return render_template('resume.html')

@user_bp.route('/about_me')
def get_about_me():
    return render_template('about_me.html')

@user_bp.route('/experience')
def get_experience():
    return render_template('experience.html')

@user_bp.route('/skills')
def get_skills():
    return render_template('skills.html')

@user_bp.route('/education')
def get_education():
    return render_template('education.html')

@user_bp.route("/hi/<string:name>")   #/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", 
                           name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("user.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', expires=datetime.now()+timedelta(seconds=10))
    response.set_cookie('username', 'student', max_age=timedelta(seconds=10))
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response

if __name__ == '__main__':
    user_bp.run(debug=True)