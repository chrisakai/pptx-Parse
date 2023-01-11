import re

# 匹配文件名中的唯一码
filename = 'http://127.0.0.1:5000/wii-instructions/19010271751001_XX作业指导书【10-999】.zip'
print(filename.split("/")[3])
print(filename.split("/")[-1])
x = re.search(r"\[\S*\]", filename)
if x:
    print(x.group())
