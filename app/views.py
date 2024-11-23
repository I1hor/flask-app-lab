from flask import request, redirect, url_for, render_template, abort, current_app


@current_app.route('/')
def main():
    return render_template("resume.html")
