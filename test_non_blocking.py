#------------------------------------------------------------
#   coding:utf-8
#------------------------------------------------------------
#   Updata History
#   November  23  02:00, 2019 (Sat)
#------------------------------------------------------------
# 
#------------------------------------------------------------

import time
import asyncio

async def waiter(name):
    for _ in range(3):
        await asyncio.sleep(1)
        print(f"{name}は1秒待ちました")

async def main():
    await asyncio.wait([waiter("aomame"), waiter("tengo")])

if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    print(f"time:{time.time() - start}")