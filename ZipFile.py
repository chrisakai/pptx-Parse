import os
from zipfile import ZipFile

def extractZip(zipFileName, extractPath):
    try:
        zipFile = ZipFile(os.path.join(os.getcwd(), zipFileName))
        for file in zipFile.namelist():
            zipFile.extract(file, extractPath)
        zipFile.close()
        return "extract success"
    except:
        return "extract failed"

def backupZip(folder):                                #这个函数只做文件夹打包的动作，不判断压缩包是否存在
    zipfile_name = os.path.basename(folder) + '.zip'    #压缩包和文件夹同名
    with ZipFile(zipfile_name, 'w') as zfile:           #以写入模式创建压缩包
        for foldername, subfolders, files in os.walk(folder):    #遍历文件夹
            print('Adding files in ' + foldername +'...')
            zfile.write(foldername)
            for i in files:
                zfile.write(os.path.join(foldername,i))
                print('Adding ' + i)
    print('Zip Done.')


# def folder2zip(folder):                               #文件夹打包为zip的函数
#     zipfile_name = os.path.basename(folder) + '.zip'
#     if not os.path.exists(zipfile_name):          #检查压缩包是否存在，如果已存在则询问是否继续
#         backupZip(folder)
#     else:
#         response = input("Zipfile exists. Coutinue?('q' for quit): ")
#         if response != 'q':
#             backupZip(folder)
