from .assets import create_webassets


def create_flask_app():
    from . import app
    from .config import config

    app.config.update(config)

    # https://stackoverflow.com/questions/33241050/trailing-slash-triggers-404-in-flask-path-rule
    app.url_map.strict_slashes = False

    return app


def create_db(app=None):
    if not app:
        app = create_flask_app()
    from . import db

    db.init_app(app)

    @app.before_first_request
    def before_first_request():
        try:
            db.create_all()
        except Exception as e:
            app.logger.warning(str(e))

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app


def create_mail(app=None):
    if not app:
        app = create_flask_app()
    from . import mail

    mail.init_app(app)
    return app


def create_marshmallow(app=None):
    if not app:
        app = create_flask_app()
    from . import marshmallow

    marshmallow.init_app(app)
    return app


def create_logger(app=None):
    if not app:
        app = create_flask_app()
    from . import logger

    logger.init_app(app)
    return app


def create_security(app=None):
    if not app:
        app = create_flask_app()
    from . import db, models, security
    from flask_security import SQLAlchemyUserDatastore

    security.init_app(
        app,
        SQLAlchemyUserDatastore(db, models.User, models.Role),
        register_blueprint=True,
    )

    return app


def create_blueprints(app=None):
    if not app:
        app = create_flask_app()

    # Blueprints
    from .views import webapp

    app.register_blueprint(webapp)

    return app


def create_swagger(app=None):
    from . import swag

    if not app:
        app = create_flask_app()
    swag.init_app(app)


def create_api_blueprints(app=None):
    if not app:
        app = create_flask_app()

    # Blueprints
    from .api.v1 import v1

    app.register_blueprint(v1, url_prefix="/v1")

    return app


def create_jinjafilters(app):
    import yaml
    from flask import request, url_for
    from .utils import strfdelta, niceage

    if not app:
        app = create_flask_app()

    def url_for_other_page(page):
        args = request.view_args.copy()
        args["page"] = page
        return url_for(request.endpoint, **args)

    @app.template_filter("to_yaml")
    def to_yaml(x):
        return "<pre>{}</pre>".format(yaml.dump(x))

    @app.template_filter("niceage")
    def _jinja2_filter_niceage(*args, **kwargs):
        return niceage(*args, **kwargs)

    @app.template_filter("datetime")
    def _jinja2_filter_datetime(date, fmt=None):
        if not date:
            return "unkown"
        if fmt:
            return strfdelta(date, fmt)
        else:
            return strfdelta(date, "{days} days {hours} hours")

    app.jinja_env.globals["url_for_other_page"] = url_for_other_page
    app.jinja_env.add_extension("pyjade.ext.jinja.PyJadeExtension")


def create_app():
    app = create_flask_app()
    create_security(app)
    create_logger(app)
    create_db(app)
    create_mail(app)
    create_webassets(app)
    create_blueprints(app)
    create_jinjafilters(app)
    return app


def create_api():
    app = create_flask_app()
    create_logger(app)
    create_db(app)
    create_mail(app)
    create_marshmallow(app)
    create_api_blueprints(app)
    create_swagger(app)
    return app
