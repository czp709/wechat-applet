from fastapi.param_functions import Body
import uvicorn
from fastapi import FastAPI, File, UploadFile,Query
from typing import Optional
from photo import main as Photo
import time
import base64
from vision_imgfilter import VisionImgFilter

img_filter = VisionImgFilter('2168002906', 'ur55BPzcFRYjwCdj')

app = FastAPI()

@app.post("/file_upload")
async def upload(file: UploadFile = File(...)):  
    filename = file.filename
    temp = filename.split('.')
    if temp[len(temp)-1]  not in ["png", "jpg"]:    # 不是png，jpg
        return {"code": 203, "msg": "不支持的图片格式"}
    else:
        try:
            res = await file.read()
            with open(filename, "wb") as f:  # 文件会保存在跟服务器启动目录同一级
                f.write(res)
            files = Photo(filename)
            photos=[]
            for file in files:
                with open(file, 'rb') as f:
                    res = base64.b64encode(f.read())
                    photos.append(res)
            return {"code": 200, "msg": "上传成功","data":photos}
        except Exception as e:
            return {"code": 201, "msg": "上传失败"}
@app.post("/file_upload1")
async def upload1(file: UploadFile = File(...)):  
    filename = file.filename
    temp = filename.split('.')
    if temp[len(temp)-1]  not in ["png", "jpg"]:    # 不是png，jpg
        return {"code": 203, "msg": "不支持的图片格式"}
    else:
        try:
            res = await file.read()
            with open(filename, "wb") as f:  # 文件会保存在跟服务器启动目录同一级
                f.write(res)
            photos=[]
            ls = [16,14,13,17,29,29,13]
            for item in ls:
                time.sleep(1.0)
                with open(filename, 'rb')as f:
                    path = str(time.time())
                    img_filter.get_content(f.read(), item,path)
                with open(path+'.jpg','rb') as f:
                    photos.append(base64.b64encode(f.read()))
            return {"code": 200, "msg": "上传成功","data":photos}
        except Exception as e:
            return {"code": 201, "msg": "上传失败"}



if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000, workers=1)
