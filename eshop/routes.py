from flask import render_template, request, redirect, flash, url_for, session
from flask_login import login_required, current_user
from flask import current_app as app
from .models import Product, User
from .forms import CreateForm


@app.route('/')
def index():
    items = Product.query.all()
    return render_template('home/index.html', data=items, current_user=current_user)


@app.route('/about')
def about():
    return render_template('home/about.html')


# admin
@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form = CreateForm(request.form)
    if form.validate_on_submit():
        new_product = Product(
                        form.title.data,
                        form.price.data,
                        current_user.email
                        )
        if new_product.add_to():
            return redirect(url_for('index'))
        else:
            return render_template('admin/create.html', form=form), flash('ERROR')
    return render_template('admin/create.html', form=form)


@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    user = User.query.filter_by(username=username).first()
    products = Product.query.filter_by(creator=user.email).all()
    return render_template('admin/dashboard.html', products=products, user=user)


@app.route('/dashboard/<username>/<int:product_id>')
@login_required
def dashboard_product(username, product_id):
    try:
        product = Product.query.filter_by(id=product_id).first()
    except Exception as e:
        flash('ERROR')
    return render_template('admin/product.html', product=product, username=username)


@app.route('/dashboard/<username>/<int:product_id>/delete')
@login_required
def dashboard_product_delete(username, product_id):
    product = Product.query.get_or_404(product_id)
    if product.delete_from():
        return redirect(url_for('dashboard', username=username))
    else:
        flash('ERROR')


@app.route('/users')
@login_required
def user_list():
    users = User.query.all()
    return render_template('admin/users.html', users=users)


# 404 handler
@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return render_template('page404.html')


# test
@app.route('/test')
@login_required
def test():
    session['redis_test'] = 'This is a session variable.'
    return render_template('test.html', body='Ты в матрице...')


@app.route('/session', methods=['GET'])
@login_required
def session_view():
    """Display session variable value."""
    return render_template(
        'session.html',
        session_variable=str(session.get('redis_test'))
    )