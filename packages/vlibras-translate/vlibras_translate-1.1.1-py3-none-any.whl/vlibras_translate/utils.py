# SOLUTION 1

# import multiprocessing
# import time

# # bar


# def bar(timeout):
#     for i in range(timeout):
#         print(f"Tick {i}")
#         time.sleep(1)

#     print(f'timeout reached!')


# if __name__ == '__main__':
#     timeout = 20

#     # Start bar as a process
#     p = multiprocessing.Process(target=bar, args=[timeout])
#     p.start()

#     # Wait for 10 seconds or until process finishes
#     p.join(10)

#     # If thread is still active
#     if p.is_alive():
#         print("running... let's kill it...")

#         # Terminate
#         p.terminate()
#         p.join()


# SOLUTION 2

import signal
from contextlib import contextmanager
import platform
from datetime import datetime as dt


def now():
    return dt.now().strftime('%Y/%m/%d %H:%M:%S')


@contextmanager
def timeout(time):
    on_linux = platform.system() == 'Linux'

    def raise_timeout(signum, frame):
        raise TimeoutError

    if on_linux:
        # Register a function to raise a TimeoutError on the signal.
        signal.signal(signal.SIGALRM, raise_timeout)
        # Schedule the signal to be sent after ``time``.
        signal.alarm(time)

    # try:
    yield
    # except TimeoutError:
    #     pass
    # finally:
    if on_linux:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def sample_func():
    # Add a timeout block.
    with timeout(2):
        print('entering block')
        import time
        time.sleep(3)
        print('This should never get printed because the line before timed out')
    print('Reached only if no exception was raised.')


if __name__ == '__main__':
    try:
        sample_func()
    except Exception as e:
        print('Raised TimeoutError')
        raise e
