"""
配置文件 - 应用配置项
"""
import os


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///app.db')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///dev.db')


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URI', 'postgresql://user:pass@localhost/prod_db')


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///test.db')


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}


def get_config(config_name=None):
    """获取配置类"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    config_class = config_map.get(config_name, config_map['default'])
    return config_class
