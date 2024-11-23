from flask import Blueprint, render_template, abort, redirect, url_for, flash, session
from .forms import PostForm
from . import post_bp
import json, os

posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
] 

@post_bp.route('/')
def get_posts():
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    if id > 3:
        abort(404)
    post = posts[id - 1]
    return render_template("detail_post.html", post=post)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_active = form.is_active.data
        publish_date = form.publish_date.data
        category = form.category.data

        
        file_path = os.path.join(os.path.dirname(__file__), 'static/assets/posts.json')
        with open(file_path) as f:
            data = json.load(f)['data']
        id = len(data) + 1

        if "username" in session:
            author = session["username"]
        else:
            author = f"noname{id}"

        data.append({"id": id, "title": title, "content": content, "author": author, "is_active": is_active, "publish_date": str(publish_date), "category": category})
        new_data = {
            "data": data
        }
        with open(file_path, "w") as f:

            json.dump(new_data, f, indent=4)
        
        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.add_post'))
    return render_template('add_posts.html', form=form)

@post_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

