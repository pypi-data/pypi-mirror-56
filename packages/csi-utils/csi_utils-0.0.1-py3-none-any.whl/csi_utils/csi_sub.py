import sys
import time

import numpy as np
import zmq

from .serialsocket import SerializingContext

num_subcarrier = 114


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

    def process_data(self, data):

        idx_l, status_l, csi_data_l, timestamp_l = zip(
            *((d["idx"], d["status"], d["csi"], d["timestamp"]) for d in data)
        )

        csi_data_l = np.asarray(csi_data_l)

        raw_amp = np.sqrt(
            csi_data_l[:, :, :, :, 0] ** 2 + csi_data_l[:, :, :, :, 1] ** 2
        )
        raw_phase = np.arctan2(csi_data_l[:, :, :, :, 1], csi_data_l[:, :, :, :, 0])

        raw_amp = np.log(raw_amp + 1e-12) / np.log(512)

        phase_unwrap = np.unwrap(raw_phase, axis=-1)

        phase_unwrap_diff = np.zeros_like(phase_unwrap)
        for i in range(3):
            phase_unwrap_diff[:, i, :, :] = (
                phase_unwrap[:, i % 3, :, :] - phase_unwrap[:, (i + 1) % 3, :, :]
            )

        phase_unwrap_diff_offset = phase_unwrap_diff[:, :, :, 0]
        phase_unwrap_diff_offset = np.stack(
            [phase_unwrap_diff_offset] * num_subcarrier, axis=-1
        )

        phase_unwrap_diff = phase_unwrap_diff - phase_unwrap_diff_offset

        return {
            "raw_csi": csi_data_l,
            "amp": raw_amp,
            "phase": phase_unwrap,
            "phase_diff": phase_unwrap_diff,
        }
