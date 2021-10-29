from flask import current_app as app
from flask_assets import Bundle


def compile_assets(assets):

    less_test = Bundle(
        'src/*.less',
        filters='less',
        output='css/test.css',
        extra={'rel', 'stylesheet/css'}
    )

    auth_style_bundle_signin = Bundle(
        'auth_bp/src\\signin.css',
        filters='cssmin',
        output='auth_bp/css\\signin.min.css'
    )

    auth_style_bundle_signup = Bundle(
        'auth_bp/src\\signup.css',
        filters='cssmin',
        output='auth_bp/css\\signup.min.css'
    )

    assets.register('auth_style_in', auth_style_bundle_signin)
    assets.register('auth_style_up', auth_style_bundle_signup)
    assets.register('test', less_test)

    if app.config['FLASK_ENV'] != 'production':
        auth_style_bundle_signin.build()
        auth_style_bundle_signup.build()
        less_test.build()

    return assets
