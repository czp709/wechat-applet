'''
date:2019.7.7
copyright:buaalzm
'''
from qqaibase import QQAIBase
import hashlib
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote
import base64
import random
import time

class VisionImgFilter(QQAIBase):
    interface_url = "https://api.ai.qq.com/fcgi-bin/ptu/ptu_imgfilter"  # API地址
    def get_params(self, image, filter):
        self.basic_param_init()
        '''图片用base64编码'''
        base64_data = base64.b64encode(image)
        params = {'app_id': self.param_dict['app_id'],
                  'image': base64_data,
                  'time_stamp': self.param_dict['time_stamp'],
                  'nonce_str': self.param_dict['nonce_str'],
                  'filter': str(filter)
                }
        self.param_dict['image'] = base64_data
        sign_before = ''
        # 要对key排序再拼接
        for key in sorted(params):
            # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
            sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
        # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
        sign_before += 'app_key={}'.format(self.param_dict['app_key'])
        '''计算MD5摘要，得到签名字符串'''
        sign = hashlib.md5(sign_before.encode('utf-8')).hexdigest()
        sign = sign.upper()
        params['sign'] = sign
        return params

    def get_content(self, image, filter,filenamepath):
        params = self.get_params(image, filter)
        try:
            r = requests.post(self.interface_url, data=params)
            print(r.text)
            # soup = BeautifulSoup(r.text, 'lxml')
            # allcontents = soup.select('body')[0].text.strip()
            allcontents_json = json.loads(r.text)  # str转成dict
            image_data = base64.b64decode(allcontents_json["data"]['image'])
            with open(filenamepath+'.jpg', 'wb') as f:
                f.write(image_data)
        except:
            print('exception occur')

if __name__ == '__main__':
    img_filter = VisionImgFilter('2167941371', 'DED6ZWzjBApKonTF')
    with open(r'E:\fyf.jpg', 'rb')as f:
        img_filter.get_content(f.read(), 29,time.time())

