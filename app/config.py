import os


class Configuration:
    SECRET_KEY = os.environ.get('SECRET_KEY')
