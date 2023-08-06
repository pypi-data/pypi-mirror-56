import pickle
import sys
import time
import zlib
from threading import Thread


import zmq



class CSI_SUB:
    def __init__(self, addr="192.168.1.29", port="5556"):
        assert isinstance(addr, str)
        assert isinstance(port, str)
        ctx = zmq.Context.instance()
        self.sub = ctx.socket(zmq.SUB)
        self.sub.setsockopt_string(zmq.SUBSCRIBE, "")
        self.sub.setsockopt(zmq.CONFLATE, 1)

        self.sub.connect("tcp://" + addr + ":" + port)

    def recv_data(self):
        zobj = self.sub.recv()
        pobj = zlib.decompress(zobj)
        return pickle.loads(pobj)


class CSI_ROUTER:
    def __init__(self, addr):
        assert isinstance(addr, str)
        ctx = zmq.Context.instance()

        self.router = ctx.socket(zmq.ROUTER)
        self.router.bind("ipc://" + addr)

    def recv_data_pickled(self, flag=0):
        identity, zobj = self.router.recv_multipart(flags=flag)
        pobj = zlib.decompress(zobj)
        return identity, pickle.loads(pobj)

    def recv_data(self, flag=0):
        identity, msg = self.router.recv_multipart(flags=flag)
        return identity, msg

    def send_data_pickled(self, identity, x):
        pobj = pickle.dumps(x, protocol=4)
        zobj = zlib.compress(pobj)
        self.router.send_multipart([identity.encode(), zobj])

    def send_data(self, identity, x):
        self.router.send_multipart([identity.encode(), x])


class CSI_WORKER:
    def __init__(self, addr, identity):
        assert isinstance(addr, str)
        ctx = zmq.Context.instance()
        self.worker = ctx.socket(zmq.DEALER)
        self.worker.setsockopt(zmq.IDENTITY, identity.encode())
        # self.worker.setsockopt(zmq.CONFLATE, 1)
        self.worker.connect("ipc://" + addr)

    def recv_data_pickled(self, flag=0):
        zobj = self.worker.recv(flags=flag)
        pobj = zlib.decompress(zobj)
        return pickle.loads(pobj)

    def recv_data(self, flag=0):
        msg = self.worker.recv(flags=flag)
        return msg

    def send_data_pickled(self, x):
        pobj = pickle.dumps(x, protocol=4)
        zobj = zlib.compress(pobj)
        self.worker.send(zobj)

    def send_data(self, x):
        self.worker.send(x)

