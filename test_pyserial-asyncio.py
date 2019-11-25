# ------------------------------------------------------------
#   coding:utf-8
# ------------------------------------------------------------

import asyncio
import serial_asyncio
import sys
from random import randint

"""
    Raspberry Pi to Arduino
"""
class Output(asyncio.Protocol):
    #  Called when creating a connection
    def connection_made(self, transport):
        self.transport = transport
        print("port opened", transport)
        transport.serial.rts = False
        transport.write(b"1")

    #  When data is received
    def data_received(self, data):
        print("data received:", data)
        self.transport.write(b"0")
        self.transport.close()

    #  When a connection is lost
    def connection_lost(self, exc):
        print("port closed")
        asyncio.get_event_loop().stop()

"""
    e.g. future
"""
def random_hit(future, n_upper, cnt=1, loop=None):
    # n_upper = n
    if loop is None:
        loop = asyncio.get_event_loop()
    value = randint(1, n_upper)
    #print(value)

    if value == n_upper:
        print("Hit!")
        future.set_result(cnt)
    else:
        print("Not yet.")
        cnt += 1
        loop.call_soon(random_hit, future, n_upper, cnt, loop)

def _callback(future):
    print("DONE!")
    loop = asyncio.get_event_loop()

def eternal_hello(loop):
    print("Hello!")
    loop.call_soon(eternal_hello, loop)


#  main function
def main():
    #  Initialize args
    """
    try:
        n = int(sys.argv[1])
    except IndexError:
        print("Input an integer.")
        n = int(input())
    if n < 1:
        n = 1
    """

    loop = asyncio.get_event_loop()
    #  future作成
    future = loop.create_future()
    future.add_done_callback(_callback)

    coro = serial_asyncio.create_serial_connection(loop, Output, "/dev/ttyACM0", baudrate=9600)
    #loop.call_soon(random_hit, future, n)
    #loop.call_soon(eternal_hello, loop)
    loop.run_until_complete(coro)
    #loop.run_forever()
    loop.close()

if __name__ == "__main__":
    main()
