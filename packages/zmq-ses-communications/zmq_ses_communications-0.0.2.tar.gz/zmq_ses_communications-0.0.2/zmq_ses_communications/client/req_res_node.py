import asyncio
import zmq

# import zmq.asyncio
# from zmq.asyncio import Context
import os
import sys
from request import Requester
from reply import Responder
import time
import threading
import logging


class ReqResNode(Requester, Responder):
    def __init__(self, host, port, node_name):
        Requester.__init__(self, host, port, node_name)  # "127.0.0.1", 5559
        Responder.__init__(self, host, port + 1, node_name)  #  "127.0.0.1", 5560
        self.start()
        time.sleep(0.5)


if __name__ == "__main__":
    name = "node"
    if len(sys.argv) > 1:
        name = sys.argv[1]
    for i in range(60):
        N = Node(f"{name}{i}")
        N.send_request(f"{name}{i}", "hello")
