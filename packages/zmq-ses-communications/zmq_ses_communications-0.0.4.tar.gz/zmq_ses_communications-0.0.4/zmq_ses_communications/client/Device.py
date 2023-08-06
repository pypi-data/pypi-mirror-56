#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .pub_sub_node import PubSubNode
from .req_res_node import ReqResNode
from .msgs.heartbeat_pb2 import HeartBeat
from .msgs.command_pb2 import CommandRequest
import logging
import os


class SES_Device(PubSubNode, ReqResNode):
    def __init__(self, host, port, device_identity):
        self.device_logger = logging.getLogger(f"SES_Device_{os.getpid()}")
        self.device_identity = device_identity
        PubSubNode.__init__(self, "127.0.0.1", port)
        ReqResNode.__init__(self, "127.0.0.1", port + 2, device_identity)
        

    # async def node_main(self):
    #     await asyncio.gather(self.subscriber_loop())

    def callback_msg_rcvd(self, address, contents):
        message = contents
        rec_hb = HeartBeat()
        # print(f"received message in Node : {topic}: {message}")
        try:
            rec_hb.ParseFromString(message)
            self.on_HeartBeat_received(message)
        except Exception as e:
            # print("Received : ", message)
            self.on_message_received(message)

    def on_HeartBeat_received(self, message):
        self.device_logger.debug(f"{self.device_identity} received {message}")

    def on_message_received(self, message):
        self.device_logger.debug(f"{self.device_identity} received {message}")

    def on_request_received(self, source, request):
        self.device_logger.debug(f"request reveived from {request}")
        # Handle all the callbacks here
        # callback_fun = getattr(self, "on_request_receive", None)  # Creation o
        # callback_fun(source, request)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(name)s %(threadName)s %(asctime)s [%(levelname)s] : %(message)s",
    )
    dev = SES_Device("127.0.0.1", 6000, "A")
    dev.create_publisher()
    dev2 = SES_Device("127.0.0.1", 6000, "B")
    dev2.create_publisher()
    dev.send_request("B", "REQUEST from A")
    dev2.send_request("A", "REQUEST from B")
