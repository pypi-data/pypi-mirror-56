# Simple request-reply broker
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import zmq


class ReqRepRouter:
    def __init__(self, host, port):
        print("Starting request reply router")
        self.frontend_url = f"tcp://{host}:{port}"
        self.backend_url = f"tcp://{host}:{port+1}"
        context = zmq.Context()
        self.frontend = context.socket(zmq.ROUTER)
        self.backend = context.socket(zmq.ROUTER)

        # self.start_routing()

    def start_request_reply_routing(self):
        self.frontend.bind(self.frontend_url)  # "tcp://127.0.0.1:5559"
        self.backend.bind(self.backend_url)  # "tcp://127.0.0.1:5560"
        print(f"Request frontend bound to {self.frontend_url}")
        print(f"Reply backend bound to {self.backend_url}")
        poller = zmq.Poller()
        poller.register(self.frontend, zmq.POLLIN)
        poller.register(self.backend, zmq.POLLIN)
        while True:
            socks = dict(poller.poll())
            #     message = frontend.recv_multipart()
            #     print(message)
            #     backend.send_multipart(message)
            #     identity, reply = backend.recv_multipart()
            #     print(f"got reply {identity}: {reply}")

            if socks.get(self.frontend) == zmq.POLLIN:
                message = self.frontend.recv_multipart()
                print(
                    "router got ", message
                )  # Reqesting node sends source, destinaion, message, return_destination
                print(
                    "forwarding", message[1:]
                )  # the first item is the destination for a router socket. source is stripped and rest is given to backend router.
                self.backend.send_multipart(message[1:])

            if socks.get(self.backend) == zmq.POLLIN:
                message = self.backend.recv_multipart()
                print(
                    "dealer got", message
                )  # Reply node appends the return destination as destination, source is stripped and forwared to frontend router
                print("returning", message[1:])
                self.frontend.send_multipart(message[1:])


if __name__ == "__main__":
    R = ReqRepRouter("127.0.0.1", 6002)
    R.start_request_reply_routing()

