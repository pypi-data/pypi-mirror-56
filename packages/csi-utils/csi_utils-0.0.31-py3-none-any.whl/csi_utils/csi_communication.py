import sys
import time

import numpy as np
import zmq

from .serialsocket import SerializingContext


class CSI_SUB:
    def __init__(self, addr="192.168.1.29", port="5556"):
        assert isinstance(addr, str)
        assert isinstance(port, str)
        ctx = SerializingContext()
        self.sub = ctx.socket(zmq.SUB)
        self.sub.setsockopt_string(zmq.SUBSCRIBE, "")
        self.sub.setsockopt(zmq.CONFLATE, 1)

        self.sub.connect("tcp://" + addr + ":" + port)

    def recv_data(self):
        return self.sub.recv_zipped_pickle()


class CSI_IPC:
    def __init__(self, addr):
        assert isinstance(addr, str)
        ctx = SerializingContext()
        self.pub = ctx.socket(zmq.PUB)
        self.pub.bind("inproc:// " + addr + "_tx")

        self.sub = ctx.socket(zmq.SUB)
        self.sub.setsockopt_string(zmq.SUBSCRIBE, "")
        self.sub.setsockopt(zmq.CONFLATE, 1)
        self.sub.connect("inproc://" + addr + "_rx")

    def recv_data(self):
        return self.sub.recv_zipped_pickle()

    def trans_data(self, x):
        self.pub.send_zipped_pickle(x)
