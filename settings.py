import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = False
    TESTING = False
    ENV = os.getenv("ENVIRONMENT")

    @classmethod
    def for_actual_environment(cls):
        all_config = [TestConfig, DevelopmentConfig, ProductionConfig]

        for config in all_config:
            if config.is_correct_for(cls.ENV):
                return config

        return DevelopmentConfig

    @classmethod
    def name(cls):
        raise NotImplementedError('Subclass responsability')

    @classmethod
    def need_initialization(cls):
        raise NotImplementedError('Subclass responsibility')

class TestConfig(Config):
    NAME = 'testing'
    TESTING = True
    ENV = os.getenv("ENVIRONMENT")
    MONGO_DBNAME = os.getenv('MONGO_TEST_DBNAME')
    MONGO_URI = os.getenv('MONGO_TEST_URI')

    @classmethod
    def name(cls):
        return cls.NAME

    @classmethod
    def is_correct_for(cls, environment_name):
        return environment_name == cls.name()

    @classmethod
    def need_initialization(cls):
        return True

class DevelopmentConfig(Config):
    NAME = 'development'
    DEBUG = True
    ENV = os.getenv("ENVIRONMENT")
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')
    MONGO_URI = os.getenv('MONGO_URI')

    @classmethod
    def name(cls):
        return cls.NAME

    @classmethod
    def is_correct_for(cls, environment_name):
        return environment_name == cls.name()

    @classmethod
    def need_initialization(cls):
        return True

class ProductionConfig(Config):
    NAME = 'production'
    DEBUG = True
    ENV = os.getenv("ENVIRONMENT")
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')
    MONGO_URI = os.getenv('MONGO_URI')

    @classmethod
    def name(cls):
        return cls.NAME

    @classmethod
    def is_correct_for(cls, environment_name):
        return environment_name == cls.NAME
    
    @classmethod
    def need_initialization(cls):
        return False
