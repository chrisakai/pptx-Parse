from minio import Minio

MINIO_CONF = {
    'endpoint': '192.168.3.184:9000',
    'access_key': 'minioadmin',
    'secret_key': 'minioadmin',
    'secure': False
}


def upload_minio(bucket: str, file_name: str, file_path):
    client = Minio(**MINIO_CONF)
    client.fput_object(bucket_name=bucket, object_name=file_name, file_path=file_path, content_type='application/zip')

