import logging

from flask import Flask, request
from logging.handlers import SMTPHandler


MAIL_FORMAT = """
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s
Remote Addr:        %(remote_addr)s
URL:                %(url)s

Message:

%(message)s
"""


LOG_ADDITIONAL_LOGGERS = []


class Logger:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        class RequestFormatter(logging.Formatter):
            """ Extend logging Formatter to contain request content
            """

            def format(self, record):
                record.url = request.url
                record.remote_addr = request.remote_addr
                return super().format(record)

        formatter = RequestFormatter(
            "[%(asctime)s] %(remote_addr)s requested %(url)s\n"
            "%(levelname)s in %(module)s: %(message)s"
        )

        # Send mail in case of logging.ERROR or above
        mail_handler = SMTPHandler(
            (app.config["MAIL_HOST"], app.config["MAIL_PORT"]),
            app.config["MAIL_DEFAULT_SENDER"],
            app.config["MAIL_ADMINS"],
            app.config["MAIL_ERROR_SUBJECT"],
            (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"]),
        )
        mail_handler.setFormatter(logging.Formatter(MAIL_FORMAT))
        mail_handler.setLevel(logging.ERROR)
        if not app.debug:
            for logger in app.logger + LOG_ADDITIONAL_LOGGERS:
                logger.addHandler(mail_handler)

        return app.logger
