import sys
import time
from multiprocessing import Pool
import guzzler
import functools
import signal

URLS_FILE = 'urls.txt'
FREQUENCY_OF_CONSOLE_UPDATE_SECONDS = 0.01  # Update every 10 milliseconds


def main():
    '''
    Starts Guzzling processes based on optional user commandline arguments and exits
    '''
    urls = guzzler.read_urls(URLS_FILE)

    bound_type, limit = guzzler.set_args()
    start_time = time.time()
    p = Pool()

    workers = p.map_async(
        functools.partial(guzzler.guzzle, bound_type, limit, start_time), urls)

    p.close()

    print('Guzzling started.')

    while not workers.ready():
        time.sleep(FREQUENCY_OF_CONSOLE_UPDATE_SECONDS)
        print(guzzler.guzzle_status(start_time), end="")

    p.join()
    print()


def SIGINT_handler(signal, frame):
    '''
    Gracefully exits on KeyboardInterrupt
    signal and frame are parameters with traceback information.
    '''
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, SIGINT_handler)
    main()
