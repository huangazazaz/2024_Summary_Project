# -*- coding: utf-8 -*-
import json

import oss2
import os
from io import BytesIO


class AliOSS(object):
    def __init__(self):
        self.endpoint = "https://oss-cn-shenzhen.aliyuncs.com"
        with open('config.json') as config_file:
            config = json.load(config_file)

        ID = config['ALIOSS_ACCESS_KEY_ID']
        Secret = config['ALIOSS_ACCESS_KEY_SECRET']

        self.bucketName = "sustech-event-center"

        # 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
        auth = oss2.Auth(ID, Secret)
        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称。
        self.bucket = oss2.Bucket(auth, self.endpoint, self.bucketName)

    def uploadFile(self, data, name):
        fileobj = BytesIO(data)
        fileobj.seek(0, os.SEEK_SET)
        current = fileobj.tell()
        self.bucket.put_object(name, fileobj)
        return "https://" + self.bucketName + "." + self.endpoint[self.endpoint.rfind("/") + 1:] + "/" + name
