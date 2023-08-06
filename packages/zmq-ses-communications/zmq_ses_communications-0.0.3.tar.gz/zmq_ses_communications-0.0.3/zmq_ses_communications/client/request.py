#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import zmq
import zmq.asyncio
from zmq.asyncio import Context
import os
import sys
import logging


class Requester:
    def __init__(self, host, port, identitiy):
        self.requester_logger = logging.getLogger("Requester")
        self.requester_url = f"tcp://{host}:{port}"  # 127.0.0.1, 5559
        self.req_socket = zmq.Context().socket(zmq.DEALER)
        self.req_socket.identity = identitiy.encode("utf-8")
        self.requester_logger.info(f"Requester connecting to {self.requester_url}")
        self.req_socket.connect(self.requester_url)
        self.request_timeout_ms = 2000
        self.req_socket.setsockopt(zmq.RCVTIMEO, self.request_timeout_ms)

    def send_request(self, target, msg):
        self.requester_logger.debug(f"sending request: {msg}")
        self.req_socket.send_multipart(
            [target.encode("ascii"), msg.encode("utf-8"), self.req_socket.identity]
        )
        try:
            reply = self.req_socket.recv_multipart()
            self.requester_logger.debug(f"got reply {reply}")
        except zmq.error.Again as e:
            self.requester_logger.debug(
                f"Request timed out after {self.request_timeout_ms} ms, type : {e}"
            )


if __name__ == "__main__":

    idev = "req1"
    if len(sys.argv) > 1:
        idev = sys.argv[1]
        target = sys.argv[2]
    R = Requester("127.0.0.1", 5559, idev)
    R.send_request(target, "hello")
