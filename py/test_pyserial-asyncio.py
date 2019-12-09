#------------------------------------------------------------
#   coding:utf-8
#------------------------------------------------------------
#   Updata History
#   December  02  23:00, 2019 (Mon)
#------------------------------------------------------------
#   Arduinoとの非同期通信test
#------------------------------------------------------------

import asyncio
import serial_asyncio

"""
    Raspberry Pi to Arduino
"""
class Output(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self._transport = None

    #  Called when creating a connection
    def connection_made(self, transport):
        self._transport = transport
        print("port opened", self._transport)
        self._transport.serial.rts = False
        self._transport.write(b"1;\n")

    #  When data is received
    def data_received(self, data):
        print("data received", data)
        if b"\n" in data:
            self._transport.close()

    #  When a connection is lost
    def connection_lost(self, exc):
        print("port closed")
        self._transport.loop.stop()

#  main function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    #  セットして
    coro = serial_asyncio.create_serial_connection(
        loop, Output, 
        "/dev/ttyACM0",
        baudrate=9600)
    #    timeout=0.1)
    #  ループ呼ぶ(future的に)
    loop.run_until_complete(coro)
    #try:
    #  ループを繰り返す
    loop.run_forever()
    #except KeyboardInterrupt:
    #    pass

    #  Close the server
    #server.close()
    #loop.run_until_complete(server.wait_closed())
    loop.close()

