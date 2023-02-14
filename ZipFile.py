import os
import shutil
from zipfile import ZipFile


# 如果文件夹不存在，先创建
def create_directory(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def support_gbk(zip_file: ZipFile):
    name_to_info = zip_file.NameToInfo
    # copy map first
    for name, info in name_to_info.copy().items():
        real_name = name.encode('cp437').decode('gbk')
        if real_name != name:
            info.filename = real_name
            del name_to_info[name]
            name_to_info[real_name] = info
    return zip_file


def extractZip(zipFileName, extractPath):
    # 补全压缩包路径
    zip_filepath = os.path.join(os.getcwd(), zipFileName)

    with ZipFile(zip_filepath, 'r') as zip:
        # 创建一个临时目录，用来存放解压后的文件
        temp_path = os.path.join(os.getcwd(), 'tmp')
        create_directory(temp_path)

        # 解压压缩包中的文件到临时目录中
        zip.extractall(temp_path, members=[m for m in zip.infolist()])

        # 将压缩包文件名用作文件夹名
        # folder_name = os.path.splitext(zipFileName)[0]
        file_path = os.path.join(os.getcwd(), extractPath)
        create_directory(file_path)

        # 移动临时目录中的文件到指定目录中，并在移动时解决文件名中存在的乱码问题
        for file in os.listdir(temp_path):
            temp_file_path = os.path.join(temp_path, file)
            if os.path.isdir(temp_file_path):
                folder_path = os.path.join(file_path, file.encode('cp437').decode('gbk'))
                create_directory(folder_path)
                for videofile in os.listdir(temp_file_path):
                    video_file_path = os.path.join(temp_file_path, videofile)
                    new_file_path = os.path.join(folder_path, videofile.encode('cp437').decode('gbk'))
                    shutil.move(video_file_path, new_file_path)
            else:
                new_file_path = os.path.join(file_path, file.encode('cp437').decode('gbk'))
                shutil.move(temp_file_path, new_file_path)

        # 删除临时文件夹
        shutil.rmtree(temp_path)
    # try:
    #     zipFile = ZipFile(os.path.join(os.getcwd(), zipFileName))
    #     for file in zipFile.namelist():
    #         zipFile.extract(file, extractPath)
    #     zipFile.close()
    #     return "extract success"
    # except:
    #     return "extract failed"


def backupZip(folder):  # 这个函数只做文件夹打包的动作，不判断压缩包是否存在
    zipfile_name = os.path.basename(folder) + '.zip'  # 压缩包和文件夹同名
    with ZipFile(zipfile_name, 'w') as zfile:  # 以写入模式创建压缩包
        for foldername, subfolders, files in os.walk(folder):  # 遍历文件夹
            print('Adding files in ' + foldername + '...')
            zfile.write(foldername)
            for i in files:
                zfile.write(os.path.join(foldername, i))
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
