#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import os
import zmq
import binascii
from threading import Thread


class PubSubRouter:
    def __init__(self, host, port):
        print("Starting pub sub router")
        self.sub_router_url = f"tcp://{host}:{port}"
        self.pub_router_url = f"tcp://{host}:{port+1}"
        ctx = zmq.Context.instance()
        self.subscriber = ctx.socket(zmq.XSUB)
        self.publisher = ctx.socket(zmq.XPUB)

    def start_publish_subscribe_routing(self):
        self.subscriber.bind(self.sub_router_url)  # "tcp://127.0.0.1:6000")
        self.publisher.bind(self.pub_router_url)
        print(f"Starting subscriber router at :  {self.sub_router_url}")
        print(f"Starting publishing router at :  {self.pub_router_url}")
        zmq.proxy(self.subscriber, self.publisher)


if __name__ == "__main__":
    R = PubSubRouter("127.0.0.1", 6000)

