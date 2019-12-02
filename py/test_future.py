#------------------------------------------------------------
#   coding:utf-8
#------------------------------------------------------------
#   Updata History
#   November  23  02:00, 2019 (Sat)
#------------------------------------------------------------
# 
#------------------------------------------------------------

import asyncio
import sys
from random import randint

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

def ojama(loop):
    print("こんにちは")
    loop.call_soon(ojama, loop)


try:
    n = int(sys.argv[1])
except IndexError:
    print("Input an integer.")
    n = int(input())
if n < 1:
    n = 1

#  メイン
loop = asyncio.get_event_loop()
future = loop.create_future()
future.add_done_callback(_callback)

#loop.call_soon(ojama, loop)
loop.call_soon(eternal_hello, loop)
loop.call_soon(random_hit, future, n)
result = loop.run_until_complete(future)
print("{}回".format(result))
loop.close()