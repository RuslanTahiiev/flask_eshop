from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, logout_user, current_user, login_user
from eshop import login_manager, security
from eshop.forms import SignupForm, LoginForm
from eshop.models import User, db


auth_bp = Blueprint('auth_bp',
                    __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/auth/static'
                    )


@auth_bp.before_app_first_request
def create_role():
    """
    Зарисовки под использование Flask Security
    :return:
    """
    add_role = security.datastore.create_role(name='editor', description='Edit products')
    db.session.add(add_role)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except Exception as e:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('Войдите в систему.')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            new_user = User(
                            form.email.data,
                            form.username.data,
                            form.name.data
                            )
            new_user.set_password(form.password.data)
            if new_user.add_to():
                login_user(new_user)
                return redirect(url_for('dashboard', username=form.username.data))
            else:
                flash('ERROR')
        flash('Уже существует такой пользователь')
    return render_template('auth/signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', username=current_user.username))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            return redirect(url_for('dashboard', username=current_user.username))
        flash('Такого пользователя не существует или неверно введен пароль.')
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))


@auth_bp.errorhandler(404)
def auth_error(error):
    return redirect('page_not_found')
