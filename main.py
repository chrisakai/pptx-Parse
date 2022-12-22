import os
import ZipFile
import pptxParser
import shutil

# pptxParsePath = 'pptxParse'
#
# if not os.path.exists(pptxParsePath + '/'):
#     os.makedirs(pptxParsePath + '/')
#
# ZipFile.extractZip('demo.zip', pptxParsePath + '/')
#
# path_list = os.listdir(pptxParsePath + '/')
#
# #
# for filename in path_list:
#     if os.path.splitext(filename)[1] == ".pptx":
#         print(filename)
#         pptxName = pptxParsePath + '/' + filename
#         print(pptxName)
#     if os.path.splitext(filename)[1] == ".mp4":
#         src = os.path.join(pptxParsePath + '/', filename)
#         if not os.path.exists(pptxParsePath + '/'+'videos/'):
#             os.makedirs(pptxParsePath + '/'+'videos/')
#         dst = os.path.join(pptxParsePath + '/'+'videos/', filename)
#         shutil.move(src, dst)
# pptxParser.pptxParse(pptxName)
#
# # 压缩文件
# ZipFile.backupZip(pptxParsePath)
#
# # 删除缓存文件夹
# shutil.rmtree(pptxParsePath)