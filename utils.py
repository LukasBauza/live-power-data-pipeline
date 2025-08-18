import time


def interval_passed(threadName, message, interval: int):
    while True:
        time.sleep(interval)
        print(f"thread: {threadName}, message: {message}, interval: {interval}")
