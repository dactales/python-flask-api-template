from flask_sqlalchemy import SQLAlchemy


class PrePingSQLAlchemy(SQLAlchemy):
    # https://github.com/mitsuhiko/flask-sqlalchemy/issues/589
    # https://stackoverflow.com/questions/6471549/avoiding-mysql-server-has-gone-away-on-infrequently-used-python-flask-server
    def apply_pool_defaults(self, app, options):
        SQLAlchemy.apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True
