"""
获取配置中心
调用get_configcenter方法 传入参数: 配置中心url, 应用名,环境名, HTTP Basic Auth用户名,HTTP Basic Auth密码

example:
configcenter = get_configcenter('http:www.configcenter.com','hfa','test','admin','password')
mysqlUrl = configcenter.mysql_url
redis = configcenter.redis

"""


import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin


class ConfigCenter(object):
    """配置中心类"""
    def __init__(self, url, application, profile, username, password):
        config = request_config(url, application, profile, username, password)
        for key, value in config.items():
            if "." in key:
                key = key.replace(".", "_")
            setattr(self, key, value)

    def get_all_config(self):
        return self.__dict__


def request_config(url, application, profile,  username, password):
    """
    请求配置中心 获取项目配置
    :param url: git仓库地址
    :param application:  项目名
    :param profile: 环境名
    :param username: HTTP Basic Auth 认证的用户名
    :param password: HTTP Basic Auth 认证的密码
    :return: 各项配置, 数据格式为字典
    """
    response = requests.get(urljoin(url, f"{application}/{profile}"),
                            auth=HTTPBasicAuth(username, password), timeout=10
                            ).json()
    property_sources = response.get("propertySources", [])
    config = get_config(property_sources)
    return config


def get_config(property_sources):
    """将property_sources的各项配置整合到一个字典里"""
    config = dict()
    for property in property_sources:
        source = property.get('source', {})
        for key, value in source.items():
            config[key] = value
    return config


def get_configcenter(url=None, application=None, profile=None, username=None, password=None):
    """
   获取配置中心类
   :param url: git仓库地址
   :param application:  项目名
   :param profile: 环境名
   :param username: HTTP Basic Auth 认证的用户名
   :param password: HTTP Basic Auth 认证的密码
   :return: ConfigCenter 实例
   """
    config_center = ConfigCenter(url, application, profile, username, password)
    return config_center
