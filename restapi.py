import os
import re
import shutil
import time

from flask import Flask, request

import ZipFile
import minioUtil
import pptxParser

app = Flask(__name__)

# 临时解析文件夹
pptxParsePath = 'pptxParseTemp'


# 根据请求解析的压缩文件名以及目标存放路径
# 1.从minio下载目标压缩文件
# 2.解压压缩文件以及解析其中的pptx
# 3.将解析后的压缩文件上传minio并返回地址与唯一码
@app.route('/parse/<zip_name>', methods=['GET'])
def parse_pptx(zip_name):
    # 压缩文件名校验
    x = re.search(r"\d*(?=-)", zip_name)
    if not x:
        return "压缩文件命名唯一码格式错误"
    y = re.search(r"(?<=-)\w+作业指导书", zip_name)
    if not y:
        return "压缩文件命名指导书命名格式错误"
    z = re.search(r"【\S*】", zip_name)
    if not z:
        return "压缩文件命名架次号格式错误"

    # 接收到的压缩包在minio服务上的存放地址
    zipSourcePath = request.args['path']
    print("压缩包在minio服务上的存放地址: " + zipSourcePath)
    bucket = zipSourcePath.split("/")[3]
    print("minio存放桶名为: " + bucket)
    file = zipSourcePath.split("/")[-1]
    print("minio下载文件名为: " + file)

    # 1.从minio下载目标压缩文件
    filePath = os.getcwd() + os.sep + file
    minioUtil.download_file(bucket, file, filePath,)

    # 2.解压压缩文件以及解析其中的pptx
    # 判断压缩文件是否下载到当前工程目录下
    if not os.path.exists(zip_name):
        return "下载文件遇到了问题"

    # 创建临时解析文件夹
    if not os.path.exists(pptxParsePath + os.sep):
        os.makedirs(pptxParsePath + os.sep)
    # 解压文件
    ZipFile.extractZip(zip_name, pptxParsePath + os.sep)

    # 列出压缩文件里的所有文件
    path_list = os.listdir(pptxParsePath + os.sep)

    for filename in path_list:
        if os.path.splitext(filename)[1] == ".pptx":
            # filename命名规则：19010271751001-XX作业指导书【10-999】
            print(filename)
            # 匹配文件名中的唯一码
            x = re.search(r"\d*(?=-)", filename)
            if not x:
                return "pptx文件命名唯一码格式错误"
            y = re.search(r"(?<=-)\w+作业指导书", filename)
            if not y:
                return "pptx文件命名指导书命名格式错误"
            z = re.search(r"【\S*】", filename)
            if not z:
                return "pptx文件命名架次号格式错误"
            # pptxName 解析pptx路径
            pptxName = pptxParsePath + os.sep + filename
            print(pptxName)
            # 解析pptx
            pptxParser.pptxParse(pptxName)
        if os.path.splitext(filename)[1] == ".mp4":
            src = os.path.join(pptxParsePath + os.sep, filename)
            if not os.path.exists(pptxParsePath + os.sep + 'videos' + os.sep):
                os.makedirs(pptxParsePath + os.sep + 'videos' + os.sep)
            dst = os.path.join(pptxParsePath + os.sep + 'videos' + os.sep, filename)
            shutil.move(src, dst)

    # 压缩文件
    ZipFile.backupZip(pptxParsePath)

    # 删除缓存文件夹以及下载源压缩文件
    shutil.rmtree(pptxParsePath)
    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        print(filePath + "  不存在，无需删除")

    # 3.将解析后的压缩文件上传minio并返回地址与唯一码
    # minio 解析输出桶名
    bucketName = "pptx"
    # minio中目标存放文件名
    pptxParseZip = "pptxParse_" + str(int(time.time())) + ".zip"

    # arg1:minio桶名 arg2:压缩文件名 arg3:源文件地址
    minioUtil.upload_minio(bucketName, pptxParseZip, "D:\PythonWorkspace\pptxParse\pptxParseTemp.zip")
    print("upload success!")
    # 读取json
    if os.path.exists("pptx-parse.json"):
        with open(os.getcwd() + os.sep + "pptx-parse.json", 'r', encoding='utf-8') as fp:
            data = fp.read()
        fp.close()
    else:
        data = "没有json文件"
    # 返回地址与唯一码
    return " savePath=" + bucketName + os.sep + pptxParseZip + " id=" + x.group() + " jsonBody=" + data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
