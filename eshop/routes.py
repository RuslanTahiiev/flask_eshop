from flask import render_template, request, redirect, flash, url_for, session, current_app as app
from flask_login import current_user
from flask_security import login_required
from .models import Product, User
from .forms import CreateForm


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('home/index.html', products=products, current_user=current_user)


@app.route('/about')
def about():
    return render_template('home/about.html')


# admin
@app.route('/dashboard/<username>/create', methods=['POST', 'GET'])
@login_required
def create(username):
    """
    Создание услуг на сайте
    :param username:
    :return: возвращает страничку создания услуг или перенаправляет на страницу со списком услуг в панели инструментов.
    """
    form = CreateForm(request.form)
    if form.validate_on_submit():
        new_product = Product(
                        form.title.data,
                        form.description.data,
                        form.price.data,
                        current_user.email
                        )
        if new_product.add_to():
            return redirect(url_for('dashboard_products', username=current_user.username))
        else:
            return render_template('admin/create.html', form=form, ), flash('ERROR')
    return render_template('admin/create.html', form=form, current_user=current_user)


@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    """
    Страница панели инструментов
    :param username:
    :return: страницу панели инструментов
    """
    return render_template('admin/dashboard.html', current_user=current_user)


@app.route('/dashboard/<username>/products')
@login_required
def dashboard_products(username):
    """
    Список услуг пользователся на странице панели инструментов
    :param username:
    :return: список услуг пользователя
    """
    products = Product.query.filter_by(creator=current_user.email).all()
    return render_template('admin/products.html', products=products, current_user=current_user)


@app.route('/dashboard/<username>/products/<int:product_id>')
@login_required
def dashboard_product(username, product_id):
    """
    Редактирование услуги
    :param username:
    :param product_id:
    :return:
    """
    try:
        product = Product.query.filter_by(id=product_id).first()
    except Exception as e:
        flash('ERROR')
    return render_template('admin/product.html', product=product, username=current_user.username)


@app.route('/dashboard/<username>/<int:product_id>/delete')
@login_required
def dashboard_product_delete(username, product_id):
    """
    Удаление услуги
    :param username:
    :param product_id:
    :return:
    """
    product = Product.query.get_or_404(product_id)
    if product.delete_from():
        return redirect(url_for('dashboard_products', username=current_user.username))
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


# test stuff
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