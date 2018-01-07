import base64
import codecs
import hashlib
import logging
import mimetypes
import os

import boto3
import magic

#TODO: website config: put_bucket_website - ErrorDocument, IndexDocument, RoutingRules, ...
#TODO: optionally store index file with signatures to avoid updating unchanged files

class AWSS3Deploy(object):

    AMAZON_KEY_META = {
        'Content-Disposition',
        'Content-Encoding',
        'Content-Language',
        'Content-Length',
        'Content-MD5',
        'Content-Type',
        'Expires',
        'Website-Redirect-Location',
    }

    def __init__(
            self, bucket,
            aws_access_key_id=None,
            aws_secret_access_key=None,
            aws_profile_name=None,
            key_prefix='',
            file_metadata_key='_s3_meta',
            file_acl_key='_s3_acl',
            default_acl='public-read',
            md5sum=True,
            clean_prefix=False,
    ):
        """
        If neither access ley, secret key, or prodile is specified, use environment variables. If profile specified, uses credentials from .aws/credentials
        """

        self.bucket = bucket
        self.access_key = aws_access_key_id or os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_key = aws_secret_access_key or os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.aws_profile_name = aws_profile_name
        self.key_prefix = key_prefix
        self.file_meta_key = file_metadata_key
        self.file_acl_key = file_acl_key
        self.default_acl = default_acl
        self.md5sum = md5sum
        self.clean_prefix = clean_prefix

        self.logger = logging.getLogger(self.__module__)
        self.mime = magic.Magic(mime=True)

    def get_content_type(self, data):
        return self.mime.from_buffer(data[:1024])

    def md5(self, data):
        return base64.b64encode(hashlib.md5(data).digest())

    def __call__(self, files, hana):
        s3_session = None

        if self.aws_profile_name:
            s3_session = boto3.Session(profile_name=self.aws_profile_name)

        else:
            s3_session = boto3.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
            )

        s3_resource = s3_session.resource('s3')
        s3_bucket = s3_resource.Bucket(self.bucket)

        if self.clean_prefix:
            paginator = s3_resource.meta.client.get_paginator('list_objects')
            pages = paginator.paginate(
                Bucket=self.bucket,
                Prefix=self.key_prefix,
            )

            for page in pages:
                if 'Contents' in page:
                    keys = [o['Key'] for o in page['Contents']]
                    s3_resource.meta.client.delete_objects(
                        Bucket=self.bucket,
                        Delete={
                            'Objects': [{'Key': k} for k in keys]
                        }
                    )

        for filename, f in files:

            if not f.is_binary:
                f['contents'] = codecs.encode(f['contents'], 'utf-8')

            s3_meta = f.get(self.file_meta_key, {})
            s3_acl = f.get(self.file_acl_key, self.default_acl)

            if 'Content-Type' not in s3_meta:
                content_type = mimetypes.guess_type(filename)[0]

                if not content_type:
                    content_type = self.get_content_type(f['contents'])

                s3_meta['Content-Type'] = content_type

            if self.md5sum and 'Content-MD5' not in s3_meta:
                s3_meta['Content-MD5'] = self.md5(f['contents'])

            key_params = {c.replace('-', ''): s3_meta.pop(c) for c in AWSS3Deploy.AMAZON_KEY_META if c in s3_meta}

            key = os.path.join(self.key_prefix, filename)

            s3_bucket.Object(key).put(
                ACL=s3_acl,
                Body=f['contents'],
                Metadata=s3_meta,
                **key_params
            )

