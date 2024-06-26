import os


class Config:
    # flask
    DEBUG = os.environ.get('FLASK_DEBUG') or True
    TESTING = True
    ENV = 'development'
    # database
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://root:root123@192.168.0.226:3306/DTM'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # jwt
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-key'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_CHECK_FORM = True
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 3600
    JWT_REFRESH_TOKEN_EXPIRES = 360000
    PROPAGATE_EXCEPTIONS = True
