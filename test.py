import re

# 匹配文件名中的唯一码
filename = 'http://127.0.0.1:5000/wii-instructions/19010271751001-XX作业指导书【10-999】.zip'
x = re.search(r"(?<=-)\w+作业指导书", filename)
if x:
    print(x.group())
