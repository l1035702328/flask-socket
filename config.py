import datetime
import os


from apscheduler.jobstores.redis import RedisJobStore
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True
    @staticmethod
    def init_app(app):
        pass

    # # 定时任务
    # JOBS = [
    #     {
    #         "id": "job1",
    #         "func": "advanced:job1",
    #         "args": (1, 2),
    #         "trigger": "interval",
    #         "seconds": 10,
    #     }
    # ]

    SCHEDULER_JOBSTORES = {"default": RedisJobStore(db=3, host="119.91.55.183", port=6379, password='')}

    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 20}}

    SCHEDULER_JOB_DEFAULTS = {"coalesce": False, "max_instances": 3}

    SCHEDULER_API_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:LIJINfei1837463@119.91.55.183:3306/flask_study'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
