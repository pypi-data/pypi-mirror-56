import calendar
import os
import tempfile
import shutil
import hashlib
import base64
import binascii
import io
import urllib.parse
import time
import json
import glob as local_glob
import re
import collections
import functools
import threading
import ssl
from typing import overload, TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from typing_extensions import Literal

import urllib3
import xmltodict
import filelock

from . import google, azure
from .common import Request


EARLY_EXPIRATION_SECONDS = 5 * 60
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 30
HASH_CHUNK_SIZE = 65536
STREAMING_CHUNK_SIZE = 2 ** 20
AZURE_MAX_CHUNK_SIZE = 4 * 2 ** 20
# https://cloud.google.com/storage/docs/json_api/v1/how-tos/resumable-upload
assert STREAMING_CHUNK_SIZE % (256 * 1024) == 0
# it looks like azure signed urls cannot exceed the lifetime of the token used
# to create them, so don't keep the key around too long
AZURE_SAS_TOKEN_EXPIRATION_SECONDS = 60 * 60

Stat = collections.namedtuple("Stat", ["size", "mtime"])
ReadStats = collections.namedtuple("ReadStats", ["bytes_read", "requests", "failures"])

_http = None
_http_pid = None
_http_lock = threading.Lock()


def _get_http_pool():
    # ssl is not fork safe https://docs.python.org/2/library/ssl.html#multi-processing
    # urllib3 may not be fork safe https://github.com/urllib3/urllib3/issues/1179
    # both are supposedly threadsafe though, so we shouldn't need a thread-local pool
    global _http, _http_pid
    with _http_lock:
        if _http is None or _http_pid != os.getpid():
            # tensorflow imports requests with calls
            #   import urllib3.contrib.pyopenssl
            #   urllib3.contrib.pyopenssl.inject_into_urllib3()
            # which will monkey patch urllib3 to use pyopenssl and sometimes break things
            # with errors such as "certificate verify failed"
            # https://github.com/pyca/pyopenssl/issues/823
            # https://github.com/psf/requests/issues/5238
            # in order to fix this here are a couple of options:

            # method 1
            # from urllib3.util import ssl_

            # if ssl_.IS_PYOPENSSL:
            #     import urllib3.contrib.pyopenssl

            #     urllib3.contrib.pyopenssl.extract_from_urllib3()
            # http = urllib3.PoolManager()

            # method 2
            # build a context based on https://github.com/urllib3/urllib3/blob/edc3ddb3d1cbc5871df4a17a53ca53be7b37facc/src/urllib3/util/ssl_.py#L220
            # this exists because there's no obvious way to cause that function to use the ssl.SSLContext except for un-monkey-patching urllib3
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.verify_mode = ssl.CERT_REQUIRED
            context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_COMPRESSION
            context.load_default_certs()
            _http_pid = os.getpid()
            _http = urllib3.PoolManager(ssl_context=context)

        return _http


def __log_callback(msg):
    print(msg)


# pylint can't figure this out when it's a def
_log_callback = __log_callback


def set_log_callback(fn):
    global _log_callback
    _log_callback = fn


class TokenManager:
    """
    Automatically refresh a token when it expires
    """

    def __init__(self, get_token_fn):
        self._get_token_fn = get_token_fn
        self._tokens = {}
        self._lock = threading.Lock()
        self._expiration = None

    def get_token(self, *args):
        with self._lock:
            now = time.time()
            if (
                self._expiration is None
                or (now + EARLY_EXPIRATION_SECONDS) > self._expiration
            ):
                if args in self._tokens:
                    del self._tokens[args]

            if args not in self._tokens:
                self._tokens[args], self._expiration = self._get_token_fn(*args)
        return self._tokens[args]


def _google_get_access_token():
    now = time.time()
    build_req = functools.partial(
        google.create_access_token_request,
        ["https://www.googleapis.com/auth/devstorage.full_control"],
    )
    with _execute_request(build_req) as resp:
        assert resp.status == 200, f"unexpected status {resp.status}"
        result = json.load(resp)
        return result["access_token"], now + float(result["expires_in"])


def _azure_get_access_token():
    now = time.time()
    build_req = functools.partial(
        azure.create_access_token_request, "https://storage.azure.com/"
    )
    with _execute_request(build_req) as resp:
        assert resp.status == 200, f"unexpected status {resp.status}"
        result = json.load(resp)
        return result["access_token"], now + float(result["expires_in"])


def _azure_get_sas_token(account):
    def build_req():
        req = azure.create_user_delegation_sas_request(account=account)
        return azure.make_api_request(
            req, access_token=global_azure_access_token_manager.get_token()
        )

    resp = _execute_request(build_req)
    assert resp.status == 200, f"unexpected status {resp.status}"
    out = xmltodict.parse(resp)
    t = time.time() + AZURE_SAS_TOKEN_EXPIRATION_SECONDS
    return out["UserDelegationKey"], t


global_google_access_token_manager = TokenManager(_google_get_access_token)

global_azure_access_token_manager = TokenManager(_azure_get_access_token)

global_azure_sas_token_manager = TokenManager(_azure_get_sas_token)


def _exponential_sleep_generator(initial, maximum, multiplier=2):
    value = initial
    while True:
        yield value
        value *= multiplier
        if value > maximum:
            value = maximum


def _execute_azure_api_request(req):
    def build_req():
        return azure.make_api_request(
            req, access_token=global_azure_access_token_manager.get_token()
        )

    return _execute_request(build_req)


def _execute_google_api_request(req):
    def build_req():
        return google.make_api_request(
            req, access_token=global_google_access_token_manager.get_token()
        )

    return _execute_request(build_req)


def _execute_request(build_req, retry_statuses=(500, 502, 503, 504)):
    for attempt, backoff in enumerate(_exponential_sleep_generator(0.1, maximum=60.0)):
        req = build_req()
        url = req.url
        if req.params is not None:
            if len(req.params) > 0:
                url += "?" + urllib.parse.urlencode(req.params)
        data = req.data
        if data is not None:
            if not isinstance(data, (bytes, bytearray)):
                if req.encoding == "json":
                    data = json.dumps(data)
                elif req.encoding == "xml":
                    data = xmltodict.unparse(data)
                else:
                    raise Exception("invalid encoding")
                data = data.encode("utf8")

        err = None
        try:
            resp = _get_http_pool().request(
                method=req.method,
                url=url,
                headers=req.headers,
                body=data,
                timeout=urllib3.Timeout(connect=CONNECT_TIMEOUT, read=READ_TIMEOUT),
                preload_content=False,
                retries=False,
                redirect=False,
            )
            if resp.status in retry_statuses:
                err = f"request failed with status {resp.status}"
            else:
                return resp
        except (
            urllib3.exceptions.ConnectTimeoutError,
            urllib3.exceptions.ReadTimeoutError,
            urllib3.exceptions.ProtocolError,
        ) as e:
            err = e
        if attempt >= 3:
            _log_callback(
                f"error {err} when executing http request {req}, sleeping {backoff} seconds"
            )
        time.sleep(backoff)
    return None  # unreachable, for pylint


def _is_local_path(path):
    return not _is_google_path(path) and not _is_azure_path(path)


def _is_google_path(path):
    url = urllib.parse.urlparse(path)
    return url.scheme == "gs"


def _is_azure_path(path):
    url = urllib.parse.urlparse(path)
    return url.scheme == "as"


def copy(src, dst, overwrite=False):
    if not overwrite:
        if exists(dst):
            raise FileExistsError(
                f"destination '{dst}' already exists and overwrite is disabled"
            )

    # special case cloud to cloud copy, don't download the file
    if _is_google_path(src) and _is_google_path(dst):
        srcbucket, srcname = google.split_url(src)
        dstbucket, dstname = google.split_url(dst)
        token = None
        while True:
            params = None
            if token is not None:
                params = {"rewriteToken": token}
            req = Request(
                url=google.build_url(
                    "/storage/v1/b/{sourceBucket}/o/{sourceObject}/rewriteTo/b/{destinationBucket}/o/{destinationObject}",
                    sourceBucket=srcbucket,
                    sourceObject=srcname,
                    destinationBucket=dstbucket,
                    destinationObject=dstname,
                ),
                method="POST",
                params=params,
                encoding="json",
            )
            with _execute_google_api_request(req) as resp:
                if resp.status == 404:
                    raise FileNotFoundError(f"src file '{src}' not found")
                assert resp.status == 200, f"unexpected status {resp.status}"
                result = json.load(resp)
                if result["done"]:
                    break
                token = result["rewriteToken"]
        return

    if _is_azure_path(src) and _is_azure_path(dst):
        # https://docs.microsoft.com/en-us/rest/api/storageservices/copy-blob
        dst_account, dst_container, dst_blob = azure.split_url(dst)
        src_account, src_container, src_blob = azure.split_url(src)
        req = Request(
            url=azure.build_url(
                dst_account,
                "/{container}/{blob}",
                container=dst_container,
                blob=dst_blob,
            ),
            method="PUT",
            headers={
                "x-ms-copy-source": azure.build_url(
                    src_account,
                    "/{container}/{blob}",
                    container=src_container,
                    blob=src_blob,
                )
            },
        )

        with _execute_azure_api_request(req) as resp:
            if resp.status == 404:
                raise FileNotFoundError(f"src file '{src}' not found")
            assert resp.status == 202, f"unexpected status {resp.status}"
            copy_id = resp.headers["x-ms-copy-id"]
            copy_status = resp.headers["x-ms-copy-status"]

        # wait for potentially async copy operation to finish
        # https://docs.microsoft.com/en-us/rest/api/storageservices/get-blob
        # pending, success, aborted failed
        while copy_status == "pending":
            req = Request(
                url=azure.build_url(
                    dst_account,
                    "/{container}/{blob}",
                    container=dst_container,
                    blob=dst_blob,
                ),
                method="GET",
            )
            with _execute_azure_api_request(req) as resp:
                assert resp.status == 200, f"unexpected status {resp.status}"
                assert resp.headers["x-ms-copy-id"] == copy_id
                copy_status = resp.headers["x-ms-copy-status"]
        assert copy_status == "success"
        return

    with BlobFile(src, "rb") as src_f, BlobFile(dst, "wb") as dst_f:
        shutil.copyfileobj(src_f, dst_f, length=STREAMING_CHUNK_SIZE)


def _calc_range(start=None, end=None):
    # https://cloud.google.com/storage/docs/xml-api/get-object-download
    # oddly range requests are not mentioned in the JSON API, only in the XML api
    if start is not None and end is not None:
        return f"bytes={start}-{end-1}"
    elif start is not None:
        return f"bytes={start}-"
    elif end is not None:
        if end > 0:
            return f"bytes=0-{end-1}"
        else:
            return f"bytes=-{-int(end)}"
    else:
        raise Exception("invalid range")


def _create_google_page_iterator(url, method, params):
    params = params.copy()

    while True:
        req = Request(url=url, method=method, params=params)
        with _execute_google_api_request(req) as resp:
            result = json.load(resp)
            yield result
            if "nextPageToken" not in result:
                break
        params["pageToken"] = result["nextPageToken"]


def _create_azure_page_iterator(url, method, data=None, params=None):
    if params is not None:
        params = params.copy()
    if data is not None:
        data = data.copy()
    while True:
        req = Request(url=url, method=method, params=params, data=data)
        with _execute_azure_api_request(req) as resp:
            result = xmltodict.parse(resp)["EnumerationResults"]
            yield result
            if result["NextMarker"] is None:
                break
        params["marker"] = result["NextMarker"]


def _google_get_names(result, skip_item_name):
    if "prefixes" in result:
        for p in result["prefixes"]:
            yield p
    if "items" in result:
        for item in result["items"]:
            if item["name"] == skip_item_name:
                continue
            yield item["name"]


def _azure_get_names(result, skip_item_name):
    blobs = result["Blobs"]
    if "Blob" in blobs:
        if isinstance(blobs["Blob"], dict):
            blobs["Blob"] = [blobs["Blob"]]
        for b in blobs["Blob"]:
            if b["Name"] == skip_item_name:
                continue
            yield b["Name"]
    if "BlobPrefix" in blobs:
        if isinstance(blobs["BlobPrefix"], dict):
            blobs["BlobPrefix"] = [blobs["BlobPrefix"]]
        for bp in blobs["BlobPrefix"]:
            yield bp["Name"]


def _google_isfile(path):
    bucket, blob = google.split_url(path)
    if blob == "":
        return False, None
    req = Request(
        url=google.build_url(
            "/storage/v1/b/{bucket}/o/{object}", bucket=bucket, object=blob
        ),
        method="GET",
    )
    with _execute_google_api_request(req) as resp:
        assert resp.status in (200, 404), f"unexpected status {resp.status}"
        return resp.status == 200, json.load(resp)


def _azure_isfile(path):
    account, container, blob = azure.split_url(path)
    if blob == "":
        return False, None
    req = Request(
        url=azure.build_url(
            account, "/{container}/{blob}", container=container, blob=blob
        ),
        method="HEAD",
    )
    with _execute_azure_api_request(req) as resp:
        assert resp.status in (200, 404), f"unexpected status {resp.status}"
        return resp.status == 200, resp.headers


def exists(path):
    """
    Return true if that path exists (either as a file or a directory)
    """
    if _is_local_path(path):
        return os.path.exists(path)
    elif _is_google_path(path):
        isfile, metadata = _google_isfile(path)
        if isfile:
            return True
        return isdir(path)
    elif _is_azure_path(path):
        isfile, metadata = _azure_isfile(path)
        if isfile:
            return True
        return isdir(path)
    else:
        raise Exception("unrecognized path")


def glob(pattern):
    """
    Find files matching a pattern, only supports a single "*" operator
    """
    assert "?" not in pattern and "[" not in pattern and "]" not in pattern
    if _is_local_path(pattern):
        for filepath in local_glob.glob(pattern):
            yield filepath
    elif _is_google_path(pattern) or _is_azure_path(pattern):
        if "*" in pattern:
            assert pattern.count("*") == 1
            prefix, _sep, suffix = pattern.partition("*")
            if _is_google_path(pattern):
                bucket, blob_prefix = google.split_url(prefix)
                assert "*" not in bucket
                it = _create_google_page_iterator(
                    url=google.build_url("/storage/v1/b/{bucket}/o", bucket=bucket),
                    method="GET",
                    params=dict(prefix=blob_prefix),
                )
                root = f"gs://{bucket}"
                get_names = _google_get_names
            else:
                account, container, blob_prefix = azure.split_url(prefix)
                assert "*" not in account and "*" not in container
                it = _create_azure_page_iterator(
                    url=azure.build_url(account, "/{container}", container=container),
                    method="GET",
                    params=dict(comp="list", restype="container", prefix=blob_prefix),
                )
                root = f"as://{account}-{container}"
                get_names = _azure_get_names

            # * should not match /, but this is hard to do with fnmatch so use re
            re_pattern = re.compile(
                re.escape(prefix) + r"[^/]*" + re.escape(suffix) + r"$"
            )
            for result in it:
                for name in get_names(result, blob_prefix):
                    filepath = join(root, name)
                    if bool(re_pattern.match(filepath)):
                        yield filepath
        else:
            if exists(pattern):
                yield pattern
    else:
        raise Exception("unrecognized path")


def isdir(path):
    """
    Return true if a path is an existing directory
    """
    if _is_local_path(path):
        return os.path.isdir(path)
    elif _is_google_path(path):
        if not path.endswith("/"):
            path += "/"
        bucket, blob_prefix = google.split_url(path)
        if blob_prefix == "":
            req = Request(
                url=google.build_url("/storage/v1/b/{bucket}", bucket=bucket),
                method="GET",
            )
            with _execute_google_api_request(req) as resp:
                return resp.status == 200
        else:
            params = dict(prefix=blob_prefix, delimiter="/", maxResults=1)
            req = Request(
                url=google.build_url("/storage/v1/b/{bucket}/o", bucket=bucket),
                method="GET",
                params=params,
            )
            with _execute_google_api_request(req) as resp:
                result = json.load(resp)
                return "items" in result or "prefixes" in result
    elif _is_azure_path(path):
        if not path.endswith("/"):
            path += "/"
        account, container, blob = azure.split_url(path)
        if blob == "":
            req = Request(
                url=azure.build_url(
                    account, "/{container}", container=container, blob=blob
                ),
                method="GET",
                params=dict(restype="container"),
            )
            with _execute_azure_api_request(req) as resp:
                return resp.status == 200
        else:
            req = Request(
                url=azure.build_url(account, "/{container}", container=container),
                method="GET",
                params=dict(
                    comp="list",
                    restype="container",
                    prefix=blob,
                    delimiter="/",
                    maxresults=1,
                ),
            )
            with _execute_azure_api_request(req) as resp:
                result = xmltodict.parse(resp)["EnumerationResults"]
                return result["Blobs"] is not None and (
                    "BlobPrefix" in result["Blobs"] or "Blob" in result["Blobs"]
                )
    else:
        raise Exception("unrecognized path")


def listdir(path):
    """
    Returns an iterator of the contents of the directory at `path`
    """
    if not path.endswith("/"):
        path += "/"
    if not exists(path):
        raise FileNotFoundError(f"The system cannot find the path specified: '{path}'")
    if not isdir(path):
        raise NotADirectoryError(f"The directory name is invalid: '{path}'")
    if _is_local_path(path):
        for d in os.listdir(path):
            if os.path.isdir(os.path.join(path, d)):
                yield d + "/"
            else:
                yield d
    elif _is_google_path(path):
        bucket, blob = google.split_url(path)
        it = _create_google_page_iterator(
            url=google.build_url("/storage/v1/b/{bucket}/o", bucket=bucket),
            method="GET",
            params=dict(delimiter="/", prefix=blob),
        )
        for result in it:
            for name in _google_get_names(result, blob):
                yield name[len(blob) :]
    elif _is_azure_path(path):
        account, container, blob = azure.split_url(path)
        it = _create_azure_page_iterator(
            url=azure.build_url(account, "/{container}", container=container),
            method="GET",
            params=dict(comp="list", restype="container", prefix=blob, delimiter="/"),
        )
        for result in it:
            for name in _azure_get_names(result, blob):
                yield name[len(blob) :]
    else:
        raise Exception("unrecognized path")


def makedirs(path):
    """
    Make any directories necessary to ensure that path is a directory
    """
    if _is_local_path(path):
        os.makedirs(path, exist_ok=True)
        return
    elif _is_google_path(path):
        if not path.endswith("/"):
            path += "/"
        bucket, blob = google.split_url(path)
        req = Request(
            url=google.build_url("/upload/storage/v1/b/{bucket}/o", bucket=bucket),
            method="POST",
            params=dict(uploadType="media", name=blob),
        )
        with _execute_google_api_request(req) as resp:
            assert resp.status == 200, f"unexpected status {resp.status}"
    elif _is_azure_path(path):
        if not path.endswith("/"):
            path += "/"
        account, container, blob = azure.split_url(path)
        req = Request(
            url=azure.build_url(
                account, "/{container}/{blob}", container=container, blob=blob
            ),
            method="PUT",
            headers={"x-ms-blob-type": "BlockBlob"},
        )
        with _execute_azure_api_request(req) as resp:
            assert resp.status == 201, f"unexpected status {resp.status}"
    else:
        raise Exception("unrecognized path")


def remove(path):
    """
    Remove a file at the given path
    """
    if _is_local_path(path):
        os.remove(path)
    elif _is_google_path(path):
        bucket, blob = google.split_url(path)
        if blob == "" or blob.endswith("/"):
            raise IsADirectoryError(f"Is a directory: '{path}'")
        req = Request(
            url=google.build_url(
                "/storage/v1/b/{bucket}/o/{object}", bucket=bucket, object=blob
            ),
            method="DELETE",
        )
        with _execute_google_api_request(req) as resp:
            if resp.status == 404:
                raise FileNotFoundError(
                    f"The system cannot find the path specified: '{path}'"
                )
            assert resp.status == 204, f"unexpected status {resp.status}"
    elif _is_azure_path(path):
        account, container, blob = azure.split_url(path)
        if blob == "" or blob.endswith("/"):
            raise IsADirectoryError(f"Is a directory: '{path}'")
        req = Request(
            url=azure.build_url(
                account, "/{container}/{blob}", container=container, blob=blob
            ),
            method="DELETE",
        )
        with _execute_azure_api_request(req) as resp:
            if resp.status == 404:
                raise FileNotFoundError(
                    f"The system cannot find the path specified: '{path}'"
                )
            assert resp.status == 202, f"unexpected status {resp.status}"
    else:
        raise Exception("unrecognized path")


def rmdir(path):
    """
    Remove an empty directory at the given path
    """
    if _is_local_path(path):
        os.rmdir(path)
        return

    # directories in blob storage are different from normal directories
    # a directory exists if there are any blobs that have that directory as a prefix
    # when the last blob with that prefix is deleted, the directory no longer exists
    # except in the case when there is a blob with a name ending in a slash
    # representing an empty directory

    # to make this more usable it is not an error to delete a directory that does
    # not exist, but is still an error to delete a non-empty one
    if not path.endswith("/"):
        path += "/"

    if _is_google_path(path):
        _bucket, blob = google.split_url(path)
    elif _is_azure_path(path):
        _account, _container, blob = azure.split_url(path)
    else:
        raise Exception("unrecognized path")

    if blob == "":
        raise Exception(f"Cannot delete bucket: '{path}'")
    it = listdir(path)
    try:
        next(it)
    except FileNotFoundError:
        # this directory does not exist
        return
    except StopIteration:
        # this directory exists and is empty
        pass
    else:
        # this directory exists but is not empty
        raise OSError(f"The directory is not empty: '{path}'")

    if _is_google_path(path):
        bucket, blob = google.split_url(path)
        req = Request(
            url=google.build_url(
                "/storage/v1/b/{bucket}/o/{object}", bucket=bucket, object=blob
            ),
            method="DELETE",
        )
        with _execute_google_api_request(req) as resp:
            assert resp.status == 204, f"unexpected status {resp.status}"
    elif _is_azure_path(path):
        account, container, blob = azure.split_url(path)
        req = Request(
            url=azure.build_url(
                account, "/{container}/{blob}", container=container, blob=blob
            ),
            method="DELETE",
        )
        with _execute_azure_api_request(req) as resp:
            assert resp.status == 202, f"unexpected status {resp.status}"
    else:
        raise Exception("unrecognized path")


def stat(path):
    """
    Stat a file or object representing a directory, returns a Stat object
    """
    if _is_local_path(path):
        s = os.stat(path)
        return Stat(size=s.st_size, mtime=s.st_mtime)
    elif _is_google_path(path):
        isfile, metadata = _google_isfile(path)
        if not isfile:
            raise FileNotFoundError(f"No such file: '{path}'")
        ts = time.strptime(
            metadata["updated"].replace("Z", "GMT"), "%Y-%m-%dT%H:%M:%S.%f%Z"
        )
        t = calendar.timegm(ts)
        return Stat(size=int(metadata["size"]), mtime=t)
    elif _is_azure_path(path):
        isfile, metadata = _azure_isfile(path)
        if not isfile:
            raise FileNotFoundError(f"No such file: '{path}'")
        ts = time.strptime(metadata["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")
        t = calendar.timegm(ts)
        return Stat(size=int(metadata["Content-Length"]), mtime=t)
    else:
        raise Exception("unrecognized path")


def walk(top, topdown=True, onerror=None):
    """
    Walk a directory tree in a similar manner to os.walk
    """
    if not isdir(top):
        return

    if _is_local_path(top):
        for (dirpath, dirnames, filenames) in os.walk(
            top=top, topdown=topdown, onerror=onerror
        ):
            assert isinstance(dirpath, str)
            if not dirpath.endswith(os.sep):
                dirpath += os.sep
            yield (dirpath, [d + os.sep for d in dirnames], filenames)
    elif _is_google_path(top) or _is_azure_path(top):
        assert topdown
        if not top.endswith("/"):
            top += "/"
        dq = collections.deque()
        dq.append(top)
        while len(dq) > 0:
            cur = dq.popleft()
            if _is_google_path(top):
                bucket, blob = google.split_url(cur)
                it = _create_google_page_iterator(
                    url=google.build_url("/storage/v1/b/{bucket}/o", bucket=bucket),
                    method="GET",
                    params=dict(delimiter="/", prefix=blob),
                )
                get_names = _google_get_names
            elif _is_azure_path(top):
                account, container, blob = azure.split_url(cur)
                it = _create_azure_page_iterator(
                    url=azure.build_url(account, "/{container}", container=container),
                    method="GET",
                    params=dict(
                        comp="list", restype="container", delimiter="/", prefix=blob
                    ),
                )
                get_names = _azure_get_names
            else:
                raise Exception("unrecognized path")
            dirnames = []
            filenames = []
            for result in it:
                for name in get_names(result, blob):
                    name = name[len(blob) :]
                    if name.endswith("/"):
                        dirnames.append(name)
                    else:
                        filenames.append(name)
            yield (cur, dirnames, filenames)
            dq.extend(join(cur, dirname) for dirname in dirnames)
    else:
        raise Exception("unrecognized path")


def basename(path):
    """
    Get the filename component of the path

    For GCS, this is the part after the bucket
    """
    if _is_google_path(path) or _is_azure_path(path):
        url = urllib.parse.urlparse(path)
        return url.path[1:].split("/")[-1]
    else:
        return os.path.basename(path)


def dirname(path):
    """
    Get the directory name of the path

    If this is a GCS path, the root directory is gs://<bucket name>/
    """
    if _is_google_path(path) or _is_azure_path(path):
        url = urllib.parse.urlparse(path)
        urlpath = url.path[1:]
        if urlpath.endswith("/"):
            urlpath = urlpath[:-1]

        if "/" in urlpath:
            urlpath = "/".join(urlpath.split("/")[:-1]) + "/"
        else:
            urlpath = ""
        return f"{url.scheme}://{url.netloc}/{urlpath}"
    else:
        dn = os.path.dirname(path)
        if dn != "":
            dn += os.sep
        return dn


def join(a, *args):
    """
    Join file paths, if a path is an absolute path, it will replace the entire path component of previous paths
    """
    out = a
    for b in args:
        out = _join2(out, b)
    return out


def _join2(a, b):
    if _is_local_path(a):
        return os.path.join(a, b)
    elif _is_google_path(a) or _is_azure_path(a):
        if not a.endswith("/"):
            a += "/"
        assert "://" not in b
        parsed_a = urllib.parse.urlparse(a)
        newpath = urllib.parse.urljoin(parsed_a.path, b)
        return f"{parsed_a.scheme}://{parsed_a.netloc}" + newpath
    else:
        raise Exception("unrecognized path")


def cache_key(path):
    """
    Get a cache key for a file
    """
    if _is_local_path(path):
        key_parts = [path, os.path.getmtime(path), os.path.getsize(path)]
    elif _is_google_path(path) or _is_azure_path(path):
        return md5(path)
    else:
        raise Exception("unrecognized path")
    return hashlib.md5(
        "|".join(
            hashlib.md5(str(p).encode("utf8")).hexdigest() for p in key_parts
        ).encode("utf8")
    ).hexdigest()


def get_url(path):
    """
    Get a URL for the given path that a browser could open
    """
    if _is_google_path(path):
        bucket, blob = google.split_url(path)
        return google.generate_signed_url(
            bucket, blob, expiration=google.MAX_EXPIRATION
        )
    elif _is_azure_path(path):
        account, container, blob = azure.split_url(path)
        url = azure.build_url(
            account, "/{container}/{blob}", container=container, blob=blob
        )
        token = global_azure_sas_token_manager.get_token(account)
        return azure.generate_signed_url(key=token, url=url)
    elif _is_local_path(path):
        return f"file://{path}", None
    else:
        raise Exception("unrecognized path")


def md5(path):
    """
    Get the MD5 hash for a file
    """
    if _is_google_path(path):
        isfile, metadata = _google_isfile(path)
        if not isfile:
            raise FileNotFoundError(f"No such file: '{path}'")
        return binascii.hexlify(base64.b64decode(metadata["md5Hash"])).decode("utf8")
    elif _is_azure_path(path):
        isfile, metadata = _azure_isfile(path)
        if not isfile:
            raise FileNotFoundError(f"No such file: '{path}'")
        # https://docs.microsoft.com/en-us/rest/api/storageservices/get-blob-properties
        return binascii.hexlify(base64.b64decode(metadata["Content-MD5"])).decode(
            "utf8"
        )
    else:
        m = hashlib.md5()
        with BlobFile(path, "rb") as f:
            while True:
                block = f.read(HASH_CHUNK_SIZE)
                if block == b"":
                    break
                m.update(block)
        return m.hexdigest()


class _ProxyFile:
    def __init__(self, path, mode, cache_dir=None):
        self._mode = mode
        self._remote_path = path

        if self._mode in ("r", "rb"):
            if cache_dir is None:
                self._local_dir = tempfile.mkdtemp()
                self._local_path = join(self._local_dir, basename(path))
                copy(self._remote_path, self._local_path, overwrite=True)
            else:
                path_md5 = hashlib.md5(path.encode("utf8")).hexdigest()
                lock_path = join(cache_dir, f"{path_md5}.lock")
                tmp_path = join(cache_dir, f"{path_md5}.tmp")
                with filelock.FileLock(lock_path):
                    local_path = join(cache_dir, md5(path), basename(path))
                    if not exists(local_path):
                        copy(self._remote_path, tmp_path, overwrite=True)
                        # the file we downloaded may not match the remote file because
                        # the remote file changed while we were downloading it
                        # in this case make sure we don't cache it under the wrong md5
                        local_path = join(cache_dir, md5(tmp_path), basename(path))
                        os.makedirs(dirname(local_path), exist_ok=True)
                        os.replace(tmp_path, local_path)
                self._local_dir = None
                self._local_path = local_path
        else:
            self._local_dir = tempfile.mkdtemp()
            self._local_path = join(self._local_dir, basename(path))
        self._f = open(self._local_path, self._mode)
        self._closed = False

    def __getattr__(self, attr):
        if attr == "_f":
            raise AttributeError(attr)
        return getattr(self._f, attr)

    def __enter__(self):
        return self._f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if not hasattr(self, "_closed") or self._closed:
            return

        self._f.close()
        if self._mode in ("w", "wb"):
            copy(self._local_path, self._remote_path, overwrite=True)
        if self._local_dir is not None:
            os.remove(self._local_path)
            os.rmdir(self._local_dir)
        self._closed = True


class _RangeError:
    """
    Indicate to the caller that we attempted to read past the end of a file
    This can happen if a file was truncated while reading
    """


class _StreamingReadFile(io.RawIOBase):
    def __init__(self, path, size):
        super().__init__()
        self._size = size
        self._path = path
        # current reading byte offset in the file
        self._offset = 0
        self._f = None
        self.requests = 0
        self.failures = 0
        self.bytes_read = 0

    def _get_file(self, offset) -> Tuple[io.RawIOBase, Optional[_RangeError]]:
        raise NotImplementedError

    def readall(self):
        return self.read(self._size - self._offset)

    def readinto(self, b):
        if self._size == self._offset:
            return 0

        n = 0  # for pyright
        for attempt, backoff in enumerate(
            _exponential_sleep_generator(0.1, maximum=60.0)
        ):
            if self._f is None:
                self._f, file_err = self._get_file(self._offset)
                if isinstance(file_err, _RangeError):
                    return 0
                self.requests += 1

            err = None
            try:
                n = self._f.readinto(b)
                if n == 0:
                    # assume that the connection has died
                    self._f.close()
                    self._f = None
                    err = "failed to read from connection"
                else:
                    # only break out if we successfully read at least one byte
                    break
            except (
                urllib3.exceptions.ReadTimeoutError,  # haven't seen this error here, but seems possible
                urllib3.exceptions.ProtocolError,
            ) as e:
                err = e
            self.failures += 1
            if attempt >= 3:
                _log_callback(
                    f"error {err} when executing readinto({len(b)}) at offset {self._offset} on file {self._path}, sleeping for {backoff} seconds"
                )
            time.sleep(backoff)
        self._offset += n
        self.bytes_read += n
        return n

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            new_offset = offset
        elif whence == io.SEEK_CUR:
            new_offset = self._offset + offset
        elif whence == io.SEEK_END:
            new_offset = self._size + offset
        else:
            raise ValueError(f"invalid whence")
        if new_offset != self._offset:
            self._offset = new_offset
            self._f = None
        return self._offset

    def tell(self):
        return self._offset

    def close(self):
        if self.closed:
            return

        if hasattr(self, "_f") and self._f is not None:
            self._f.close()
            self._f = None

        super().close()

    def readable(self):
        return True

    def seekable(self):
        return True


class _GoogleStreamingReadFile(_StreamingReadFile):
    def __init__(self, path):
        isfile, self._metadata = _google_isfile(path)
        if not isfile:
            raise FileNotFoundError(f"No such file or directory: '{path}'")
        super().__init__(path, int(self._metadata["size"]))

    def _get_file(self, offset):
        req = Request(
            url=google.build_url(
                "/storage/v1/b/{bucket}/o/{name}",
                bucket=self._metadata["bucket"],
                name=self._metadata["name"],
            ),
            method="GET",
            params=dict(alt="media"),
            headers={"Range": _calc_range(start=offset)},
        )
        resp = _execute_google_api_request(req)
        if resp.status == 416:
            # likely the file was truncated while we were reading it
            # return an empty file and indicate to the caller what happened
            return io.BytesIO(), _RangeError()
        assert resp.status == 206, f"unexpected status {resp.status}"
        return resp, None


class _AzureStreamingReadFile(_StreamingReadFile):
    def __init__(self, path):
        isfile, self._metadata = _azure_isfile(path)
        if not isfile:
            raise FileNotFoundError(f"No such file or directory: '{path}'")
        super().__init__(path, int(self._metadata["Content-Length"]))

    def _get_file(self, offset):
        account, container, blob = azure.split_url(self._path)
        req = Request(
            url=azure.build_url(
                account, "/{container}/{blob}", container=container, blob=blob
            ),
            method="GET",
            headers={"Range": _calc_range(start=offset)},
        )
        resp = _execute_azure_api_request(req)
        if resp.status == 416:
            # likely the file was truncated while we were reading it
            # return an empty file and indicate to the caller what happened
            return io.BytesIO(), _RangeError()
        assert resp.status == 206, f"unexpected status {resp.status}"
        return resp, None


class _StreamingWriteFile(io.BufferedIOBase):
    def __init__(self):
        # current writing byte offset in the file
        self._offset = 0
        # contents waiting to be uploaded
        self._buf = b""

    def _upload_chunk(self, chunk, finalize):
        raise NotImplementedError

    def _upload_buf(self, finalize=False):
        if finalize:
            size = len(self._buf)
        else:
            size = (len(self._buf) // STREAMING_CHUNK_SIZE) * STREAMING_CHUNK_SIZE
            assert size > 0
        chunk = self._buf[:size]
        self._buf = self._buf[size:]

        self._upload_chunk(chunk, finalize)
        self._offset += len(chunk)

    def close(self):
        if self.closed:
            return

        # we will have a partial remaining buffer at this point
        self._upload_buf(finalize=True)
        super().close()

    def tell(self):
        return self._offset

    def writable(self):
        return True

    def write(self, b):
        self._buf += b
        while len(self._buf) > STREAMING_CHUNK_SIZE:
            self._upload_buf()

    def readinto(self, b):
        raise io.UnsupportedOperation("not readable")

    def detach(self):
        raise io.UnsupportedOperation("no underlying raw stream")

    def read1(self, size=None):
        raise io.UnsupportedOperation("not readable")

    def readinto1(self, b):
        raise io.UnsupportedOperation("not readable")


class _GoogleStreamingWriteFile(_StreamingWriteFile):
    def __init__(self, path):
        bucket, name = google.split_url(path)
        req = Request(
            url=google.build_url(
                "/upload/storage/v1/b/{bucket}/o?uploadType=resumable", bucket=bucket
            ),
            method="POST",
            data=dict(name=name),
            headers={"Content-Type": "application/json; charset=UTF-8"},
        )
        with _execute_google_api_request(req) as resp:
            assert resp.status == 200, f"unexpected status {resp.status}"
            self._upload_url = resp.headers["Location"]
        super().__init__()

    def _upload_chunk(self, chunk, finalize):
        start = self._offset
        end = self._offset + len(chunk) - 1

        total_size = "*"
        if finalize:
            total_size = self._offset + len(chunk)
            assert len(self._buf) == 0

        headers = {
            "Content-Type": "application/octet-stream",
            "Content-Range": f"bytes {start}-{end}/{total_size}",
        }
        if len(chunk) == 0 and finalize:
            # this is not mentioned in the docs but appears to be allowed
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Range
            headers["Content-Range"] = f"bytes */{total_size}"

        req = Request(url=self._upload_url, data=chunk, headers=headers, method="PUT")

        with _execute_google_api_request(req) as resp:
            if finalize:
                assert resp.status in (200, 201), f"unexpected status {resp.status}"
            else:
                # 308 is the expected response
                assert (
                    resp.status == 308
                ), f"unexpected status {resp.status} at offset {self._offset}"


class _AzureStreamingWriteFile(_StreamingWriteFile):
    def __init__(self, path):
        account, container, blob = azure.split_url(path)
        self._url = azure.build_url(
            account, "/{container}/{blob}", container=container, blob=blob
        )
        # premium block blob storage supports block blobs and append blobs
        # https://azure.microsoft.com/en-us/blog/azure-premium-block-blob-storage-is-now-generally-available/
        req = Request(
            url=self._url, method="PUT", headers={"x-ms-blob-type": "AppendBlob"}
        )
        with _execute_azure_api_request(req) as resp:
            if resp.status == 409:
                # a blob already exists with a different type so we failed to create the new one
                remove(path)
                with _execute_azure_api_request(req) as resp:
                    pass
            assert resp.status == 201, f"unexpected status {resp.status}"
        self._md5 = hashlib.md5()
        super().__init__()

    def _upload_chunk(self, chunk, finalize):
        if len(chunk) == 0:
            return

        # max 4MB https://docs.microsoft.com/en-us/rest/api/storageservices/append-block#remarks
        start = 0
        while start < len(chunk):
            end = start + AZURE_MAX_CHUNK_SIZE
            data = chunk[start:end]
            self._md5.update(data)
            req = Request(
                url=self._url,
                method="PUT",
                params=dict(comp="appendblock"),
                data=data,
                headers={"x-ms-blob-condition-appendpos": self._offset + start},
            )

            with _execute_azure_api_request(req) as resp:
                # https://docs.microsoft.com/en-us/rest/api/storageservices/append-block#remarks
                assert resp.status in (201, 412), f"unexpected status {resp.status}"
            start += AZURE_MAX_CHUNK_SIZE

    def close(self):
        if self.closed:
            return

        super().close()
        # azure does not calculate md5s for us, we have to do that manually
        # https://blogs.msdn.microsoft.com/windowsazurestorage/2011/02/17/windows-azure-blob-md5-overview/
        req = Request(
            url=self._url,
            method="PUT",
            params=dict(comp="properties"),
            headers={"x-ms-blob-content-md5": base64.b64encode(self._md5.digest())},
        )

        with _execute_azure_api_request(req) as resp:
            assert resp.status == 200, f"unexpected status {resp.status}"


# https://github.com/microsoft/pyright/issues/354#issuecomment-557836876
@overload
def BlobFile(
    path: str, mode: "Literal['rb']", buffer_size: int = ...
) -> io.BufferedIOBase:
    ...


@overload
def BlobFile(
    path: str, mode: "Literal['wb']", buffer_size: int = ...
) -> io.BufferedIOBase:
    ...


@overload
def BlobFile(
    path: str, mode: "Literal['r']", buffer_size: int = ...
) -> io.TextIOWrapper:
    ...


@overload
def BlobFile(
    path: str, mode: "Literal['w']", buffer_size: int = ...
) -> io.TextIOWrapper:
    ...


def BlobFile(path, mode="r", buffer_size=io.DEFAULT_BUFFER_SIZE):
    """
    Open a local or remote file for reading or writing
    """
    assert not path.endswith("/")
    mode = mode
    assert mode in ("w", "wb", "r", "rb")
    if _is_local_path(path):
        f = io.FileIO(path, mode=mode)
        if "r" in mode:
            f = io.BufferedReader(f, buffer_size=buffer_size)
        else:
            f = io.BufferedWriter(f, buffer_size=buffer_size)
    elif _is_google_path(path):
        if mode in ("w", "wb"):
            f = _GoogleStreamingWriteFile(path)
        elif mode in ("r", "rb"):
            f = _GoogleStreamingReadFile(path)
            f = io.BufferedReader(f, buffer_size=buffer_size)
        else:
            raise Exception(f"unsupported mode {mode}")
    elif _is_azure_path(path):
        if mode in ("w", "wb"):
            f = _AzureStreamingWriteFile(path)
        elif mode in ("r", "rb"):
            f = _AzureStreamingReadFile(path)
            f = io.BufferedReader(f, buffer_size=buffer_size)
        else:
            raise Exception(f"unsupported mode {mode}")
    else:
        raise Exception("unrecognized path")

    if "b" not in mode:
        # PR for type fix https://github.com/python/typeshed/pull/3485
        f = io.TextIOWrapper(f, encoding="utf8")

    return f


class LocalBlobFile:
    """
    Like BlobFile() but in the case that the path is a remote file, all operations take place
    on a local copy of that file.

    When reading this is done by downloading the file during the constructor, for writing this
    means uploading the file on `close()` or during destruction.

    If `cache_dir` is specified and a remote file is opened in read mode, its contents will be
    cached locally.  It is the user's responsibility to clean up this directory.
    """

    def __init__(self, path, mode="r", cache_dir=None):
        assert not path.endswith("/")
        self._mode = mode
        assert self._mode in ("w", "wb", "r", "rb")
        if _is_google_path(path) or _is_azure_path(path):
            self._f = _ProxyFile(path, self._mode, cache_dir=cache_dir)
        elif _is_local_path(path):
            self._f = open(file=path, mode=self._mode)
        else:
            raise Exception("unrecognized path")

    def __enter__(self):
        return self._f.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._f.__exit__(exc_type, exc_val, exc_tb)

    def __getattr__(self, attr):
        if attr == "_f":
            raise AttributeError(attr)
        return getattr(self._f, attr)
