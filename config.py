# minio服务地址及端口（用于返回后台填值）
minio_host = '192.168.3.184'
minio_port = '9000'
# minio服务地址及端口，账号密码
MINIO_CONF = {
    'endpoint': '192.168.3.184:9000',
    'access_key': 'minioadmin',
    'secret_key': 'minioadmin',
    'secure': False
}
# 解析ppt结果（zip）存放于minio中的桶名
minio_bucket = 'pptx'
# 解析文件夹的暂存路径
local_pptParse_File = 'E:\PythonWorkspace\pptxParse'
# local_pptParse_File = '/home/rootcf/PythonWorkspace/pptxParse'
# 临时解析文件夹名
pptxParsePath = 'pptxParseTemp'
