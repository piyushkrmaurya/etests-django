from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False


class InstituteMediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_INSTITUTE_STORAGE_BUCKET_NAME
    location = settings.AWS_INSTITUTE_MEDIA_LOCATION
    custom_domain = settings.AWS_INSTITUTE_DOMAIN
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    default_acl = "private"
