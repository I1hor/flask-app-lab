from flask import Blueprint

user_bp = Blueprint('user', __name__, template_folder='templates/users')


from . import views