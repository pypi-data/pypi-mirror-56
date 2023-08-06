import time

import numpy as np

num_subcarrier = 114


def f1(x, y, z):
    d1 = {"idx": x, "timestamp": y}
    d1.update(z)
    return d1


def preprocess_sub_raw(data):
    global num_subcarrier
    status_l, csi_data_l = zip(
        *((f1(d["idx"], d["timestamp"], d["status"]), d["csi"]) for d in data)
    )

    csi_data_l = np.asarray(csi_data_l)


    raw_amp = np.sqrt(csi_data_l[..., 0] ** 2 + csi_data_l[..., 1] ** 2)
    raw_phase = np.arctan2(csi_data_l[..., 1], csi_data_l[..., 0])


    # raw_amp = np.log(raw_amp + 1e-12) / np.log(512)

    phase_unwrap = np.unwrap(raw_phase, axis=-1)

    phase_unwrap_diff = np.diff(phase_unwrap, axis=1)

    phase_unwrap_diff_offset = phase_unwrap_diff[..., 0]
    phase_unwrap_diff_offset = np.stack(
        [phase_unwrap_diff_offset] * num_subcarrier, axis=-1
    )

    phase_unwrap_diff = phase_unwrap_diff - phase_unwrap_diff_offset


    return {
        "status": status_l,
        "raw": csi_data_l,
        "amp": raw_amp,
        "phase": phase_unwrap,
        "phase_diff": phase_unwrap_diff,
    }
