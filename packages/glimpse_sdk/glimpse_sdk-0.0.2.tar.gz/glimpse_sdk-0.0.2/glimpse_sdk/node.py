#!/usr/bin/env python
# -*- coding=utf-8 -*-
import json
import rsa
import time
import base64

from tornado import httpclient

from glimpse_sdk.mycrypto import aes


def sort_dict(d):
    keys = d.keys()
    keys.sort()
    return map(d.get, keys)


class GlimpseNode:
    def __init__(self, gate_way=None, aes_key=None, pub_key=None, private_key=None, node_id=None,
                 hash_algorithm='SHA-256'):
        self.gate_way = gate_way
        self.aes_key = aes_key
        self.node_id = node_id
        self.pub_key = pub_key
        self.private_key = private_key
        self.hash_algorithm = hash_algorithm

    def set_aes_key(self, aes_key: str):
        """ 设置Aes密钥 """
        self.aes_key = aes_key

    def sign(self, content: str):
        """ 签名 """
        return rsa.sign(content.encode("utf8"), self.private_key, self.hash_algorithm)

    async def execute(self, api: str, params=None):
        """ 异步执行请求 """

        # 在body中加入时间戳，防止重放攻击
        params['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = json.dumps(params, sort_keys=True)
        # 将body内容加密
        cipher = aes.encrypt(self.aes_key, content)
        # 根据密文生成签名
        sign = rsa.sign(cipher.encode("utf8"), self.private_key, self.hash_algorithm)
        # 将签名base64编码
        sign = str(base64.b64encode(sign), encoding='utf8')
        # 封装请求体
        body = {
            'node_id': self.node_id,
            'content': cipher,
            'sign': sign,
        }
        request = httpclient.HTTPRequest(self.gate_way + api, method="POST", body=json.dumps(body),
                                         headers={'Content-Type': 'application/javascript'})
        response = await httpclient.AsyncHTTPClient().fetch(request)

        return response.body.decode(errors="ignore")
