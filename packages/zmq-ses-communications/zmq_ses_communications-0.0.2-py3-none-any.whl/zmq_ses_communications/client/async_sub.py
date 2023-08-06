#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import time
import zmq
import zmq.asyncio
from zmq.asyncio import Context
import os
import psutil
from threading import Thread
import logging


class Subscriber(Thread):
    def __init__(self, host, port):
        self.subscriber_logger = logging.getLogger("Subscriber")
        Thread.__init__(self)
        self.subscriber_url = f"tcp://{host}:{port}"
        self.subscriber_logger.info(f"Subscriber connecting to {self.subscriber_url}")
        self.subscriber_ctx = Context.instance()
        self.process = psutil.Process(os.getpid())
        self.sub_loop = asyncio.new_event_loop()

    async def subscriber_loop(self, subsciptions):
        self.subsciptions = subsciptions
        self.subscriber = self.subscriber_ctx.socket(zmq.SUB)
        self.subscriber.connect(self.subscriber_url)
        for prefix in subsciptions:
            self.subscriber.setsockopt(zmq.SUBSCRIBE, prefix.encode())
            self.subscriber_logger.info(f"Setting subscription for msg : {prefix}")

        while True:
            # print("receiving msg")
            await asyncio.sleep(0.001)
            await self.receive_message()

    async def receive_message(self):
        future = self.subscriber.recv_multipart()
        future.add_done_callback(self.callback_msg_rcvd)
        #
        # print(address, contents)

    def callback_msg_rcvd(self, future):
        pass

    # async def do_something(self):
    #     while True:
    #         await asyncio.sleep(0.0)
    #         #
    #         # print("Doing house keeping")

    def run_sub(self, prefix):
        asyncio.set_event_loop(self.sub_loop)
        self.sub_loop.create_task(self.subscriber_loop(prefix))
        self.sub_loop.run_forever()


if __name__ == "__main__":
    s = Subscriber("127.0.0.1", 6001)
    asyncio.run(s.subscriber_loop())
