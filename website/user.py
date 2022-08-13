from flask import Blueprint, flash, request, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from . import db
from .models import User, user_type, is_premium

user = Blueprint("user", __name__, static_folder='static', template_folder='templates')


# Route che porta al profilo principale dell'utente
@user.route('/profile/<int:user_id>')
def userprofile(user_id):
    user = User.query.filter_by(id=user_id).first()
    role = user_type(user_id)
    membership = is_premium(user_id)
    return render_template("profile.html", user=user, role=role, membership=membership)
