#------------------------------------------------------------
#   coding:utf-8
#------------------------------------------------------------
#   Updata History
#   November  27  11:00, 2019 (Wed)
#------------------------------------------------------------
#   Arduinoとの非同期通信test
#------------------------------------------------------------

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
        transport.write(b"1;")

    #  When data is received
    def data_received(self, data):
        print("data received:", data)
        if data == "finished":
            self.transport.close()
        self.transport.write(b"0;")
        
    #  When a connection is lost
    def connection_lost(self, exc):
        print("port closed")
        asyncio.get_event_loop().stop()

#  main function
def main():
    loop = asyncio.get_event_loop()
    coro = serial_asyncio.create_serial_connection(
        loop, Output, 
        "/dev/ttyACM0",
        baudrate=9600)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    #  Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    main()
