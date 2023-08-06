#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/22 15:48
# @Author  : wiken
# @Site    : 
# @File    : ys_requests.py
# @Software: PyCharm
# @Desc    :
import requests
from datetime import datetime, timedelta
from ys_service.http_service.system_service import now



class YsRequests(object):
    def __init__(self, context):
        self.session = requests.Session()
        self.start_time = now()
        self._deadline = context.get_header("deadline")
        self.set_deadline()

    def set_deadline(self):
        if not self._deadline:
            raise TimeoutError("未传入deadline")
        else:
            self._deadline = datetime.strptime(self._deadline, "%Y-%m-%d %H:%M:%S")

    @classmethod
    def create(cls, context):
        """
        创建ys_requests 实例
        :param context:
        :return: 实例对象
        """
        return cls(context)

    def get(self, *args, timeout=30, **kwargs):
        self.is_timeout(timeout)
        response = self.session.get(*args, timeout=30, **kwargs)
        return response

    def post(self, timeout, *args, **kwargs):
        self.is_timeout(timeout)
        response = self.session.post(*args, timeout=30, **kwargs)
        return response

    def is_timeout(self, timeout):
        """
        从队列消息中得到到期时间，如果下一次请求超时后还不到期则执返回True
        :param timeout:
        :return: bool
        """
        if now() - self._deadline < timedelta(seconds=timeout):
            return True
        else:
            raise TimeoutError("deadline:{}， 已超时".format(self._deadline))


if __name__ == "__main__":
    ...
