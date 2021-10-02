'''
date:2019.7.7
copyright:buaalzm
'''
import time
import random
import string
from abc import ABCMeta, abstractmethod


class QQAIBase():
    __metaclass__ = ABCMeta
    param_dict = {}

    def __init__(self, app_id, app_key):
        self.param_dict['app_id'] = app_id
        self.param_dict['app_key'] = app_key

    def basic_param_init(self):
        '''请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）'''
        t = time.time()
        self.param_dict['time_stamp'] = str(int(t))

        '''请求随机字符串，用于保证签名不可预测'''
        self.param_dict['nonce_str'] = ''.join(random.sample(string.ascii_letters + string.digits, 10))

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def get_content(self):
        pass

    @abstractmethod
    def get_params(self):
        pass
