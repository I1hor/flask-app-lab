from flask import request, redirect, url_for, render_template, abort, make_response, session, flash
from . import user_bp
from datetime import timedelta, datetime

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

@user_bp.route('/profile', methods=['GET', 'POST'])
def get_profile():
    if "username" not in session:
        flash("Ви повинні увійти, щоб переглянути профіль.", "error")
        return redirect(url_for('user.login'))
    
    cookies = request.cookies
    username = session['username']
    color_scheme = request.cookies.get('color_scheme', 'light')

    if request.method == 'POST':
        action = request.form.get('action')
        key = request.form.get('key')
        value = request.form.get('value')
        max_age = request.form.get('max_age', type=int)

        response = make_response(redirect(url_for('user.get_profile')))
        if action == 'add' and key and value:
            response.set_cookie(key, value, max_age=max_age)
            flash(f"Кука '{key}' успішно додана.", "success")
            return response

        elif action == 'delete':
            if key:
                response.set_cookie(key, '', expires=0)
                flash(f"Кука '{key}' успішно видалена.", "info")
            else:
                for cookie_key in cookies.keys():
                    response.set_cookie(cookie_key, '', expires=0)
                session.pop('username', None)
                flash("Всі кукі успішно видалені. Будь ласка, увійдіть знову.", "info")
                return redirect(url_for('user.login'))

    return render_template("profile.html", username=username, cookies=cookies, color_scheme=color_scheme)

@user_bp.route('/set_color_scheme/<string:scheme>', methods=['POST'])
def set_color_scheme(scheme):
    if scheme not in ['light', 'dark']:
        flash("Недійсна кольорова схема", "error")
        return redirect(url_for('user.get_profile'))

    response = make_response(redirect(url_for('user.get_profile')))
    response.set_cookie('color_scheme', scheme, max_age=30*24*60*60)
    flash(f"Кольорова схема '{scheme}' застосована.", "success")
    return response

@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('login')
        password = request.form.get('password')
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Вхід успішний!", "success")
            return redirect(url_for("user.get_profile"))
        else:
            flash("Неправильне ім'я користувача або пароль", "fail")
    
    return render_template("login.html")

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for('user.login'))


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

@user_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", 
                           name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("user.greetings", name="administrator", age=45, _external=True)
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
    response.set_cookie('username', '', expires=0)
    return response

if __name__ == '__main__':
    user_bp.run(debug=True)