import base64
import requests
from PIL import Image
import time
def get_access_token():
    """
    获取 access_token
    """
    # 注意 SK 与 AK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=su5UynGpMEiVUhmvvtBggscv&client_secret=l8Gr8IKzaqmqxNv2sVrmDY52pp2q0DHw'
    response = requests.get(host)
    if response:
        return response.json()['access_token']

def get_foreground(originalImagePath, ):
    """
    人像分割
    """
    
    # 二进制方式打开图片文件
    f = open(originalImagePath, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}

    # 请求 百度 AI 开放平台
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg?access_token=" + get_access_token()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"image": img}
    response = requests.post(request_url, data=params, headers=headers)

    if response:
        foreground = response.json()['foreground']
        img_data = base64.b64decode(foreground)
        # 人像图片存放地址
        foreground_path = 'foreground.png'
        with open(foreground_path, 'wb') as f:
            f.write(img_data)
    # if response:
    #      foreground = response.json()['foreground']
    #      img_data = base64.b64decode(foreground)
    #      return img_data
    # else:
    #      return 0
def get_background(path):
    """
    背景图片
    """
    color = ('red', 'blue', 'white')
    photo = Image.open(path)
    size = photo.size
    print(size)
    imgs=[]
    for c in color:
        # 一寸照片大小
        img = Image.new("RGBA", size, c)
        imgs.append(img)
    return imgs
    
def main(path):
    get_foreground(path)
    p = Image.open('foreground.png')
    # 将图像裁剪到合适的像素
    
    # 分离图片
    r,g,b,a = p.split()

    imgs = get_background('foreground.png')
    i=0
    filenames=[]
    # 将底色图像和人物图像合并，mask参数为去掉透明背景色
    for img in imgs:
        img.paste(p, (0, 0), mask = a)
        filename=str(i)+'.png'
        img.save(filename)
        i+=1
        filenames.append(filename)
    return filenames
