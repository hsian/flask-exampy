import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_ADMIN = "hsian"
    FLASKY_ADMIN_PASSWORD = "123456"

    ALLUSERS = [
    "石田野",
    "蒋增东",
    "王达枝",
    "曾令平",
    "王润华",
    "龙旭智",
    "何海深",
    "余航",
    "傅阳光",
    "余得水",
    "陈昌斌",
    "黎家俊",
    "杨胜珍",
    "刘德鑫",
    "涂凡",
    "叶小生",
    "黎鹏飞",
    "刘蔚峰",
    "黄何瑞",
    "测试"]


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig,
}