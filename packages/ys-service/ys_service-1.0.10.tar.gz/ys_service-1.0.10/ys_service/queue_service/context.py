#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Time    : 2019/11/4 14:35
# @Author  : v5yangzai
# @Site    : https://github.com/v5yangzai
# @File    : context.py
# @project : ys_module
# @Software: PyCharm
# @Desc    :
from bson.objectid import ObjectId
from ys_service.queue_service.action import *

from ys_service.http_service.log_service import LogCreate
from ys_service.http_service.context_attach_data_server import ContextAttachDataServer
from ys_service.http_service.attach_data_service import CreateAttachDataService


class Context(object):
    """
    将获取的详细进行封装为Context对象
    """
    def __init__(self, queue, logger, connection, channel, method_frame, header_frame, body, service):
        self.queue = queue
        self.logger = logger
        self.conn = connection
        self.chan = channel
        self.method_frame = method_frame
        self.header_frame = header_frame
        self.body = body
        self.timing = None  # 定时
        self.service = service
        self.object_id = ObjectId
        self.logger = None  # 日志对像
        self._context_attach_data_handler = None

    @property
    def delivery_tag(self):
        return self.method_frame.delivery_tag

    def ack(self, reply_data=None):
        return ActionAck(self, reply_data)()

    def nack(self):

        return ActionNack(self)()

    def next_to(
            self,
            exchange_name=None,
            routing_key=None,
            new_message_body=None,
            new_message_headers=None,
    ):
        return ActionNextTo(self, exchange_name, routing_key, new_message_body, new_message_headers)()

    def go_back(self, exchange_name, routing_key, new_message_body, new_message_headers):
        return ActionNextTo(self, exchange_name, routing_key, new_message_body, new_message_headers)()

    def get_header(self, key):
        return self.header_frame.headers.get(key)

    @property
    def text(self):
        """
        获取数据的字符串格式
        :return:
        """
        return self.body.decode("utf-8") if self.body else ""

    def get_json(self):
        """
        获取数据反序列化后的对象
        :return: 反序列化后的对象
        """
        try:
            return json.loads(self.text)
        except json.JSONDecodeError:
            return None

    def log(self, message, level="info", data_property=None, version=None, auth=None,
            application_name=None, application_module=None):

        if not self.logger:
            application = {
                "applicationName": "py_host: " + (application_name or self.queue.queue_name),
                "applicationVersion": version,
                "applicationModule": application_module,
                "author": auth
            }

            trace_property = {
                "traceId": self.header_frame.headers.get("trace_id"),
                "processId": self.header_frame.headers.get("process_id"),
                "processStage": self.header_frame.headers.get("process_stage")
            }
            if not self.logger:
                self.logger = LogCreate().create(application, trace_property)

        return self.logger.send_log(message,
                                    level=level,
                                    data_property=data_property)

    @property
    def attach_data(self):
        
        if not self._context_attach_data_handler:
            attach_data_handler = CreateAttachDataService().create()
            try:
                message_id = self.get_json()["messageId"]
            except (TypeError, KeyError) as e:
                return {
                    "is_success": False,
                    "status_code": "",
                    "message": "从队列中获取message_id失败, 异常信息{}".format(e),
                    "data": self.body
                }
            self._context_attach_data_handler = ContextAttachDataServer(
                message_id=message_id,
                handler=attach_data_handler
            )
            
        return self._context_attach_data_handler
