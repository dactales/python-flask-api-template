from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class PrePingSQLAlchemy(SQLAlchemy):
    # https://github.com/mitsuhiko/flask-sqlalchemy/issues/589
    # https://stackoverflow.com/questions/6471549/avoiding-mysql-server-has-gone-away-on-infrequently-used-python-flask-server
    def apply_pool_defaults(self, app, options):
        SQLAlchemy.apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True


def deltatime(time):
    if not hasattr(time, "days"):  # dirty hack
        now = datetime.utcnow()
        if isinstance(time, str):
            time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        time = abs(now - time)

    d = {"days": time.days}
    d["hours"], rem = divmod(time.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return d


def strfdelta(time, fmt=None):
    if not hasattr(time, "days"):  # dirty hack
        now = datetime.utcnow()
        if isinstance(time, str):
            time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        delta = abs(now - time)

    d = {"days": delta.days}
    d["hours"], rem = divmod(delta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    if fmt:
        return fmt.format(**d)
    if time > now:
        return "in {days} days".format(**d)
    else:
        return "{days} days ago".format(**d)


def niceage(time):
    t = deltatime(time)
    ret = ""
    if "days" in t and t["days"]:
        ret += "{days} days "
    if "hours" in t and t["hours"]:
        ret += "{hours} hours "
    if "minutes" in t and t["minutes"]:
        ret += "{minutes} minutes "
    if "seconds" in t and t["seconds"]:
        ret += "{seconds} seconds "
    return ret.format(**t)
