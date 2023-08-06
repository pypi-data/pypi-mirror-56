# -*- coding: utf-8 -*-

import os
import io
import hashlib
import json
import threading
import tempfile
import sys
import shutil

import botocore
import boto3

from modelhub import __version__
from . import conf
from .utils import cached_property, mkdir
from .exceptions import VersionError

# from collections import OrderedDict


# class API(object):

#     def __init__(self):
#         self.base_path = urllib.parse.urljoin(conf.API_URI, "model")

#     def __getattr__(self, attr):
#         url = urllib.parse.urljoin(self.base_path, attr)

#         @contextlib.wraps(session.post)
#         def post(*args, **kwargs):
#             return session.post(url, *args, **kwargs)
#         return post


def get_path_last_child(path):
    return list(filter(None, path.split("/")))[-1]


class ProgressPercentage(object):

    def __init__(self, size):
        self._size = size
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            if self._size:
                percentage = (self._seen_so_far / self._size) * 100
                to_write = "\r>>%s / %s  (%.2f%%)" % (
                    self._seen_so_far, self._size,
                    percentage)
            else:
                to_write = "\r>>%s"
            sys.stdout.write(to_write)
            sys.stdout.flush()
            if self._seen_so_far == self._size:
                sys.stdout.write("\n")


class API(object):

    @cached_property
    def session(self):
        assert all([
            conf.AWS_ACCESS_KEY_ID,
            conf.AWS_SECRET_ACCESS_KEY,
            conf.AWS_REGION_NAME,
        ]), "AWS S3 information is required, check if these information exists in `~/.modelhubrc` or use `modelhub config` to set"
        return boto3.session.Session(
            aws_access_key_id=conf.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=conf.AWS_SECRET_ACCESS_KEY,
            region_name=conf.AWS_REGION_NAME,
        )

    @cached_property
    def s3(self):
        return self.session.resource('s3')

    @cached_property
    def bucket(self):
        return self.s3.Bucket(conf.AWS_BUCKET_NAME)

    @cached_property
    def client(self):
        return self.session.client("s3")

    @cached_property
    def server_info(self):
        return self.get_json("modelhub_server_info.json")

    def _get_aws_full_path(self, *paths):
        return os.path.join(conf.AWS_BASE_PATH, *paths)

    def ensure_version(self, key):
        from distutils.version import LooseVersion
        require_version = LooseVersion(self.server_info.get("min_%s_version" % key))
        if require_version is None:
            return
        if require_version > LooseVersion(__version__):
            raise VersionError("%s need modelhub version higher than %s, now is %s" % (key, require_version, __version__))

    def _ls_request(self, full_path, recursive=False):
        kwargs = {} if recursive else {"Delimiter": "/"}
        return api.client.list_objects_v2(Bucket=conf.AWS_BUCKET_NAME, Prefix=full_path, StartAfter=full_path, **kwargs)

    def ls_subfolder(self, *paths):
        full_path = self._get_aws_full_path(*paths)
        # TODO
        return [os.path.relpath(item["Prefix"], full_path) for item in self._ls_request(full_path).get("CommonPrefixes", [])]

    def ls_file(self, *paths, **kwargs):
        recursive = kwargs.get("recursive", False)
        full_path = self._get_aws_full_path(*paths)
        if not full_path.endswith("/"):
            full_path += "/"
        res = self._ls_request(full_path, recursive=recursive).get("Contents", [])
        for item in res:
            item["name"] = os.path.basename(item["Key"])
            item["path"] = os.path.relpath(item["Key"], full_path)

        return res

    def copy_dir(self, old_name, new_name):
        for file in self.ls_file(old_name, recursive=True):
            old_file_name = os.path.join(old_name, file["path"])
            new_file_name = os.path.join(new_name, file["path"])
            self.copy_file(old_file_name, new_file_name)

    def copy_file(self, old_name, new_name):
        # print("copy", old_name, new_name)
        old_full_name = self._get_aws_full_path(old_name)
        new_full_name = self._get_aws_full_path(new_name)
        api.client.copy_object(
            Bucket=conf.AWS_BUCKET_NAME,
            CopySource={'Bucket': conf.AWS_BUCKET_NAME, 'Key': old_full_name},
            Key=new_full_name
        )
        # api.client.delete_object(Bucket=conf.AWS_BUCKET_NAME, Key=old_full_name)

    def get_file(self, fp, *paths, **kwargs):
        md5 = kwargs.get("md5", None)
        progressbar = kwargs.get("progressbar", False)
        size = kwargs.get("size", None)
        auto_copy = kwargs.get("auto_copy", True)
        full_path = self._get_aws_full_path(*paths)
        if progressbar:
            callback = ProgressPercentage(size)
        else:
            callback = None

        if md5 is not None and auto_copy:
            _fp = fp
            fp = tempfile.TemporaryFile()
        try:
            self.bucket.download_fileobj(full_path, fp, Callback=callback)
        except botocore.exceptions.ClientError as e:
            if e.response.get("Error", {}).get("Code") == "404":
                raise self.FileDoesNotExist(full_path)
            raise
        fp.seek(0)
        if md5 is not None:
            new_md5 = self.md5sum(fp)
            if md5 != new_md5:
                raise self.FileCorruptError(full_path, new_md5)
            if auto_copy:
                self.local_copy_file(fp, _fp)
                fp.close()
                fp = _fp
        return fp

    def get_json(self, *paths):
        with io.BytesIO() as f:
            self.get_file(f, *paths)
            return json.loads(f.read().decode())

    def upload_file(self, fp, *paths, **kwargs):
        progressbar = kwargs.get("progressbar", False)
        full_path = self._get_aws_full_path(*paths)
        if progressbar:
            size = self.get_fp_size(fp)
            callback = ProgressPercentage(size)
        else:
            callback = None
        self.bucket.upload_fileobj(fp, full_path, Callback=callback)

    def upload_json(self, content, *paths, **kwargs):
        with io.BytesIO() as f:
            json_str = json.dumps(content, **kwargs)
            f.write(json_str.encode())
            f.seek(0)
            self.upload_file(f, *paths)

    def delete_file(self, *paths, **kwargs):
        recursive = kwargs.get("recursive", False)
        full_path = self._get_aws_full_path(*paths)
        if not full_path.endswith("/"):
            full_path += "/"
        if recursive:
            paths = [file_item["Key"] for file_item in self.ls_file(*paths, recursive=True)]
        else:
            paths = []
        paths.append(full_path)
        # print(paths)
        res = self.bucket.delete_objects(Delete=dict(
            Objects=[
                dict(
                    Key=path
                )
                for path in paths
            ]
        ))
        assert res.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200
        # print("res", res)
        if "Deleted" not in res:
            raise ValueError(res["Errors"])
        return [item["Key"] for item in res["Deleted"]]

    class FileDoesNotExist(Exception):
        pass

    class FileCorruptError(Exception):
        pass

    @staticmethod
    def md5sum(fp):
        d = hashlib.md5()
        while True:
            buf = fp.read(4096)  # 128 is smaller than the typical filesystem block
            if not buf:
                fp.seek(0)
                break
            d.update(buf)
        return d.hexdigest()

    @staticmethod
    def local_copy_file(from_fp, to_fp):
        while True:
            buf = from_fp.read(4096)  # 128 is smaller than the typical filesystem block
            if not buf:
                break
            to_fp.write(buf)
        to_fp.seek(0)
        from_fp.seek(0)

    @staticmethod
    def get_fp_size(fp):
        fp.seek(0, os.SEEK_END)
        res = fp.tell()
        fp.seek(0)
        return res

    @staticmethod
    def local_link_dir(source_path, target_path):
        mkdir(target_path)
        for root, dirs, files in os.walk(source_path):
            rel_path = os.path.relpath(root, source_path)
            if rel_path == ".":
                target_root = target_path
            else:
                target_root = os.path.join(target_path, rel_path)
            for dir in dirs:
                os.mkdir(os.path.join(target_root, dir))
            for file in files:
                try:
                    os.link(os.path.join(root, file), os.path.join(target_root, file))
                except OSError as e:
                    if e.errno != 18:
                        raise
                    # print("fallback to copy", file)
                    shutil.copy2(os.path.join(root, file), os.path.join(target_root, file))

api = API()
