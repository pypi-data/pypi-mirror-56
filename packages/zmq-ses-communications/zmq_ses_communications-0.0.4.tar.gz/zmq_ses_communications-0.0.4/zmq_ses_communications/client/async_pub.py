#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import zmq
import zmq.asyncio
from zmq.asyncio import Context
import os
import psutil
from threading import Thread
import logging


class Publisher(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.publisher_logger = logging.getLogger("Publisher")
        self.publisher_ctx = Context.instance()
        self.publisher_url = f"tcp://{host}:{port}"
        self.publisher_logger.info(f"Publisher connecting to {self.publisher_url}")
        self.pub_loop = asyncio.new_event_loop()

    async def send_message(self, topic, message):
        await self.publisher.send_multipart(
            [topic.encode("utf-8"), message.encode("utf-8")]
        )

    async def send_proto_message(self, topic, message):
        await self.publisher.send_multipart([topic.encode("utf-8"), message])

    async def publisher_loop(self):
        await asyncio.sleep(0.1)
        self.publisher = self.publisher_ctx.socket(zmq.PUB)
        self.publisher.connect(self.publisher_url)
        # i = 0
        # while True:
        # message = f"blla: {i}"
        # self.process = psutil.Process(os.getpid())
        # print(
        #     f"Publishing message: {message}, memory usage RSS : {self.process.memory_info().rss/(1024*1024):.2f} MB"
        # )

        # await self.send_message("ERROR", message)
        # await asyncio.sleep(0.1)
        # i += 1

    def run_pub(self):
        asyncio.set_event_loop(self.pub_loop)
        self.pub_loop.create_task(self.publisher_loop())
        self.pub_loop.run_forever()


if __name__ == "__main__":
    p = Publisher("127.0.0.1", 6000)
    asyncio.run(p.publisher_loop())
