import os
import shutil
import time

from flask import Flask, request

import ZipFile
import minioUploader
import pptxParser

app = Flask(__name__)

pptxParsePath = 'pptxParse'


# 解析压缩文件以及其中的pptx
@app.route('/parse/<zip_name>')
def parse_pptx(zip_name):
    # minio 桶名
    bucketName = "pptx"
    # minio 目标存放文件名
    pptxParseZip = "pptxParse_" + str(int(time.time())) + ".zip"

    # 创建临时解析文件夹
    if not os.path.exists(pptxParsePath + '/'):
        os.makedirs(pptxParsePath + '/')
    # 解压文件
    ZipFile.extractZip(zip_name, pptxParsePath + '/')

    # 列出压缩文件里的所有文件
    path_list = os.listdir(pptxParsePath + '/')

    for filename in path_list:
        if os.path.splitext(filename)[1] == ".pptx":
            print(filename)
            pptxName = pptxParsePath + '/' + filename
            print(pptxName)
            pptxParser.pptxParse(pptxName)
        if os.path.splitext(filename)[1] == ".mp4":
            src = os.path.join(pptxParsePath + '/', filename)
            if not os.path.exists(pptxParsePath + '/' + 'videos/'):
                os.makedirs(pptxParsePath + '/' + 'videos/')
            dst = os.path.join(pptxParsePath + '/' + 'videos/', filename)
            shutil.move(src, dst)

    # 压缩文件
    ZipFile.backupZip(pptxParsePath)

    # 删除缓存文件夹
    shutil.rmtree(pptxParsePath)

    # arg1:minio桶名 arg2:压缩文件名 arg3:源文件地址
    minioUploader.upload_minio(bucketName, pptxParseZip, "E:\PythonWorkspace\pptxParse\pptxParse.zip")
    print("upload success!")
    return bucketName + "/" + pptxParseZip


if __name__ == '__main__':
    app.run()
