import os
from urllib.parse import urljoin

from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

from root import settings


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    default_acl = 'public-read'


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


# HIDE IN PRODUCTION
class CKEditorLocalStorage(FileSystemStorage):
    location = os.path.join(settings.MEDIA_ROOT, "ckeditor")
    base_url = urljoin(settings.MEDIA_URL, "ckeditor/")


# HIDE IN DEVELOPMENT
class CKEditorAWSStorage(S3Boto3Storage):
    location = 'ckeditor'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = False