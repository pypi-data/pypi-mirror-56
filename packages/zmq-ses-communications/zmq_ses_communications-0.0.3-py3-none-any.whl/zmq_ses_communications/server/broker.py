#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from .pub_sub_router import PubSubRouter
from .req_res_router import ReqRepRouter


class Broker(PubSubRouter, ReqRepRouter):
    def __init__(self, host, port):
        PubSubRouter.__init__(self, host, port)
        ReqRepRouter.__init__(self, host, port + 2)
        t1 = Thread(target=self.start_publish_subscribe_routing)
        t2 = Thread(target=self.start_request_reply_routing)
        t1.start()
        t2.start()


if __name__ == "__main__":
    broker = Broker("127.0.0.1", 6000)

