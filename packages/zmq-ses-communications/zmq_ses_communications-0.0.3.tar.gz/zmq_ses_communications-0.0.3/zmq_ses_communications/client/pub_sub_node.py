#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
from threading import Thread

from .async_pub import Publisher
from .async_sub import Subscriber
from .msgs.heartbeat_pb2 import HeartBeat


class PubSubNode(Publisher, Subscriber):
    def __init__(self, host, port):
        self.pubsub_logger = logging.getLogger("PubSubNode")
        Publisher.__init__(self, host, port)
        Subscriber.__init__(self, host, port + 1)
        pub = Thread(target=self.run_pub)
        subs = ["test", "HEARTBEAT"]
        sub = Thread(target=self.run_sub, args=(subs,))
        pub.start()
        sub.start()
        self.pubsub_logger.info("Started Publisher and subscriber threads")

    def get_hb_msg(self):
        msg = HeartBeat()
        msg.device_name = "test_device"
        msg.device_id = 1
        msg.device_lifetime = 1
        return msg.SerializeToString()

    async def publish_heartbeat(self):
        while True:
            await asyncio.sleep(1)
            await self.send_proto_message("HEARTBEAT", self.get_hb_msg())
            self.pubsub_logger.debug("publishing heartbeat")

    async def publish_test(self):
        while True:
            await asyncio.sleep(1)
            await self.send_message("test", "this is test")
            self.pubsub_logger.debug("publishing test msg")

    def create_publisher(self):
        future = asyncio.run_coroutine_threadsafe(
            self.publish_heartbeat(), self.pub_loop
        )
        future = asyncio.run_coroutine_threadsafe(self.publish_test(), self.pub_loop)


if __name__ == "__main__":
    N1 = PubSubNode("127.0.0.1", 6000)
    print("this will not print")
    N1.create_publisher()
