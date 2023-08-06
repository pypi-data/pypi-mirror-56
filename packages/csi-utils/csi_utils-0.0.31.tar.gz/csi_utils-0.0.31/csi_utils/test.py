import time

import csi_utils


def performance_test(sub, dataset):
    start = [time.time()]
    data = sub.recv_data()
    start.append(time.time())

    res = csi_utils.preprocess_sub_raw(data)
    start.append(time.time())
    dataset.array_raw.append(res["raw"])
    dataset.array_amp.append(res["amp"])
    dataset.array_phase_diff.append(res["phase_diff"])
    start.append(time.time())
    for i in range(3):
        print(start[i + 1] - start[i])
    print(100 / (start[-1] - start[0]))
