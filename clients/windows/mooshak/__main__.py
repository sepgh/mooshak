import signal
import sys
import threading
import client
import rights


MOOSHAK_CLIENT = None


def signal_handler(signal, frame):
    print('Shutting down gracefully ...')
    MOOSHAK_CLIENT.stop()
    sys.exit(0)


if __name__ == '__main__':
    if not rights.is_user_admin():
        print("Run this program as administrator")
        exit(0)

    MOOSHAK_CLIENT = client.MooshakClient()
    MOOSHAK_CLIENT.start()

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')
    forever = threading.Event()
    forever.wait()

