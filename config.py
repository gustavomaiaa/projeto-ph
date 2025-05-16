import os

class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '16112004'
    MYSQL_DB = 'ph_agua'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:16112004@localhost/ph_agua"
    SECRET_KEY = "phobjectiveactive"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
