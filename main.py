import requests
import signal
import time
import ritpytrading
from time import sleep

class ApiException(Exception):
    pass

def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True

API_KEY = {'X-API-key': 'TY0Y1KE9'}    # use your RIT API key here
host_url = 'http://localhost:9999'     # Make sure the RIT client uses the same port
base_path = '/v1'
base_url = host_url + base_path
shutdown = False

ORDER_LIMIT = 5
MAX_SIZE = 1000
TOTAL_VOLUME = 20000
COUNT = int(TOTAL_VOLUME/MAX_SIZE)
number_of_orders = 0
total_speedbumps = 0



def speedbump(transaction_time):
    global total_speedbumps
    global number_of_orders
    order_speedbump = -transaction_time + 1/ORDER_LIMIT
    total_speedbumps =  total_speedbumps + order_speedbump
    number_of_orders += 1
    sleep(total_speedbumps/number_of_orders)


def main():
    with requests.Session() as s:
        s.headers.update(API_KEY)
        while number_of_orders < COUNT:
            start = time.time()
            resp = s.post(base_url, params= {'ticker': 'ALGO', 'type': 'LIMIT',
            'quantity': MAX_SIZE, 'price':20, 'action': 'BUY'})

            if resp.ok:
                transaction_time = time.time() - start
                speedbump(transaction_time)
            else:
                print(resp.json())



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()