from minio import Minio, S3Error

MINIO_CONF = {
    'endpoint': '192.168.3.184:9000',
    'access_key': 'minioadmin',
    'secret_key': 'minioadmin',
    'secure': False
}


# 上传文件至minio指定bucket中
def upload_minio(bucket: str, file_name: str, file_path):
    client = Minio(**MINIO_CONF)
    client.fput_object(bucket_name=bucket, object_name=file_name, file_path=file_path, content_type='application/zip')


# 读取bucket下的文件
def latest_minio_find(bucket: str, object: str):
    client = Minio(**MINIO_CONF)
    if not client.bucket_exists(bucket):
        return None
    data = client.get_object(bucket, object)
    return data.data.decode('utf-8')


# 下载
# def load_data_minio(bucket: str, object: str):
#     client = Minio(**MINIO_CONF)
#     if not client.bucket_exists(bucket):
#         return None
#     data = client.get_object(bucket, object)
#     path = "receive.zip"
#     with open(path, 'wb') as file_data:
#         for d in data.stream(32 * 1024):
#             file_data.write(d)
#     return data.data


# 从bucket 下载文件 + 写入指定文件
def download_file(bucket_name, file, file_path, stream=1024 * 32):
    try:
        client = Minio(**MINIO_CONF)
        data = client.get_object(bucket_name, file)
        with open(file_path, "wb") as fp:
            for d in data.stream(stream):
                fp.write(d)
    except S3Error as e:
        print("[error]:", e)
