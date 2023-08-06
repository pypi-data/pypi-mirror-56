from flask import render_template


# Custom error pages
def page_not_found(e):
    return render_template('error/404.html'), 404


def internal_server_error(e):
    return render_template('error/500.html'), 500


class Production:
    DEBUG = False
    TESTING = False
    ENV = 'production'
    # This will be overwritten by the values in
    # instance/config.py
    SECRET_KEY = 'production_secret_key'
    # Will create the file in the current folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../ctrlv_client.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        # flask-quickstart/instance/config.py
        app.config.from_pyfile('config.py', silent=True)
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(500, internal_server_error)
        return


class Development:
    DEBUG = True
    TESTING = False
    ENV = 'development'
    SECRET_KEY = 'development_secret_key'
    # Will create the file in the current folder
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        app.register_error_handler(404, page_not_found)
        return


class Testing:
    DEBUG = False
    TESTING = True
    ENV = 'testing'
    SECRET_KEY = 'testing_secret_key'
    # Set to Flase CSRF tokens not handled
    # in unit tests
    # Testing logins
    WTF_CSRF_ENABLED = False
    # PRESERVE_CONTEXT_ON_EXCEPTION = False
    # https://gehrcke.de/2015/05/in-memory-sqlite-database-and-flask-a-threading-trap/
    # https://stackoverflow.com/questions/21766960/operationalerror-no-such-table-in-flask-with-sqlalchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @staticmethod
    def init_app(app):
        pass


config = {
    'production': Production,
    'development': Development,
    'testing': Testing
}
