#!/usr/bin/env python
# encoding: utf-8
"""
@Author: zhichuang.zhang@yiducloud.cn
@Created on: 2019-11-15 15:20
"""
import sys
import sqlite3
import getpass
import logging
import keyring
from itertools import chain
from typing import Iterator
from urllib.parse import urlparse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ChromeCookie:
    """
    creation_utc：Cookie产生的utc时间
    host_key：Cookie所在的网页(domain)
    name：Cookie名称
    value：不加密的Cookie值，由于Chrome几乎都会对Cookie值加密后再存储，因此这个字段基本都是空的
    path：如果服务器需要设置Cookies，那么服务器在响应浏览器请求的时候会返回Set-Cookie的响应，并且附带所要设置的Cookies，这里的path的默认值就是返回Set-Cookie的那个页面。path以'/'为开头。
    expires_utc：Cookie的有效期限
    is_secure：指示在浏览器与服务器之间传输该Cookie时需要采用加密通道，即https
    is_httponly：当设置了该值为1时，在浏览器上运行的JS不能读取到该Cookie，该Cookie只能由http请求读取。这个标记主要目的是提高Cookie的安全性，防止无关的JS脚本窃取Cookie中的重要信息
    last_access_utc：上一次访问到该Cookie的时间
    has_expires：Cookie的期限是否有效
    is_persistent：如果expires_utc不为0，那么这个值为1
    priority：Cookie的删除优先级，Cookie也有存储上限的，当超出上限则需要删除，此时会有特定的删除策略来删除不同priority的Cookie
    encrypted_value：加密后的Cookie值
    firstpartyonly：first-party以及third-party是HTTP Request的一种分类，\
    """

    def __init__(self):
        self.iterations = None
        self.my_pass = None
        self.cookie_path = None
        self.connect = None
        self.logger = None
        self.decryptor = None

    def _init_sqlite3_connect(self) -> None:
        """获取sqlite连接"""
        if not self.cookie_path:
            raise Exception("not find cookie_path")
        connect = sqlite3.connect(self.cookie_path)
        connect.row_factory = dict_factory
        self.connect = connect

    def init_by_system(self) -> None:
        """根据系统初始化参数"""
        self.logger = logging.getLogger(__name__)
        if sys.platform == 'darwin':
            self._init_for_mac()
        elif sys.platform == 'linux':
            self._init_for_linux()
        else:
            raise Exception("不支持{}系统".format(sys.platform))
        self._init_decryptor()
        self._init_sqlite3_connect()

    def _init_for_linux(self) -> None:
        """Linux初始化参数、"""
        self.iterations = 1
        self.cookie_path = "~/.config/chromium/Default/Cookies"
        self.my_pass = 'peanuts'.encode('utf8')

    def _init_for_mac(self) -> None:
        """Mac初始化参数、"""
        self.iterations = 1003
        user = getpass.getuser()
        self.cookie_path = "/Users/{}/Library/ApplicationSupport/Google/Chrome/Default/Cookies".format(
            user)
        self.my_pass = keyring.get_password(
            'Chrome Safe Storage', 'Chrome').encode("utf8")

    def _init_decryptor(self) -> None:
        """初始化Cipher 解密时使用"""
        enc_key = PBKDF2HMAC(
            algorithm=SHA1(),
            backend=default_backend(),
            iterations=self.iterations,
            length=16,
            salt=b"saltysalt",
        ).derive(self.my_pass)
        self.cipher = Cipher(algorithm=AES(enc_key), mode=CBC(
            b" " * 16), backend=default_backend())

    @staticmethod
    def clean(decrypted: bytes) -> str:
        """清除格式"""
        last = decrypted[-1]
        if isinstance(last, int):
            return decrypted[:-last].decode("utf8")
        return decrypted[: -ord(last)].decode("utf8")

    def encrypted_value_decrypt(self, encrypted_value: bytes) -> str:
        """chome cookie encrypted_value解密"""
        encrypted_value = encrypted_value[3:]
        decryptor = self.cipher.decryptor()
        return self.clean(decryptor.update(encrypted_value) + decryptor.finalize())

    def execute(self, sql: str) -> Iterator:
        """执行sql"""
        self.logger.info("execute sql: {}".format(sql))
        cursor = self.connect.cursor()
        for row in cursor.execute(sql):
            value = self.encrypted_value_decrypt(
                row.get('encrypted_value'))
            row['value'] = value
            yield row
        cursor.close()

    @classmethod
    def _get_host_name(cls, host: str) -> str:
        """获取域名
        example.com
        .example.com
        foo.example.com
        .foo.example.com
        """
        hostname = urlparse(host).hostname
        if not hostname:
            yield host
            yield "." + host
            return
        hostname_list = hostname.split('.')
        for i in range(2, len(hostname_list) + 1):
            domain = ".".join(hostname_list[-i:])
            yield domain
            yield "." + domain

    def get_cookie_by_host(self, host: str) -> Iterator[str]:
        """获取cookie
        """
        result = []
        cookies = {}
        for host_name in self._get_host_name(host):
            sql = 'select * from cookies where host_key like "%{host_name}%";'.format(host_name=host_name)
            result.append(self.execute(sql))
        for item in chain(*result):
            cookies.setdefault(item['name'], item['value'])
        return cookies

    def get_cookie_by_sql(self, sql):
        cookies = {}
        for item in self.execute(sql=sql):
            cookies.setdefault(item['name'], item['value'])
        return cookies

    def __enter__(self):
        self.init_by_system()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()

