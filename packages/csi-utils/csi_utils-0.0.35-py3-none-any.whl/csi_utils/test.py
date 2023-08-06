import time
from threading import Thread

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


def router_worker_test():
    router = csi_utils.CSI_ROUTER("routing")

    def testwork1():
        work = csi_utils.CSI_WORKER("routing", "A")
        for i in range(5):
            print(f"A recv {i}th", end="")
            print(work.recv_data())

    def testwork2():
        work = csi_utils.CSI_WORKER("routing", "B")
        for i in range(5):
            print(f"B recv {i}th", end="")
            print(work.recv_data())

    Thread(target=testwork1).start()
    Thread(target=testwork2).start()
    time.sleep(1)
    for i in range(10):
        router.send_data("A", b"testmsg")
        router.send_data("B", b"testmsg")
