from typing import Callable, Coroutine, List
import pandas as pd
import numpy as np
from pandas.core.accessor import register_index_accessor
import requests
import json
import aiohttp
import asyncio
import time


TS_fresh = pd.read_csv('./TS_fresh.csv')
rates = pd.read_csv('./reserve_luna_usd.csv', index_col=0)
TS_fresh['height'] = TS_fresh['height'].apply(lambda x: int(x))
# TS_fresh = TS_fresh[:3]
exclude = rates[~rates['result'].str.contains("API rate limit exceeded")]
remain = TS_fresh[~TS_fresh['height'].isin(exclude['height'])]
responses = []  # stores responses for postal codes
# i = 0


class Retry(object):
    """class providing a decorator for retring HTTP requests"""

    def __init__(self, nbtimes: int, wait_time_sec: int = 0):
        self.nbtimes = nbtimes
        self.times = 0
        self.errors = []
        self.wait_time_sec = wait_time_sec

    def __call__(self, func: Callable):
        def wrapper(*args, **kwargs):
            self.times += 1
            if self.nbtimes != self.times:
                print(self.nbtimes, self.times)
                try:
                    value = func(*args, **kwargs)
                    return value
                except Exception as err:
                    print(f"error: retrying after waiting for {self.wait_time_sec} sec")
                    if hasattr(err, "message"):
                        self.errors.append(err.message)
                    else:
                        self.errors.append(err)
                    time.sleep(self.wait_time_sec)
                    wrapper(*args, **kwargs)
            else:
                print(
                    f"fails to execute retried {self.times} times. Lists of errors : {self.errors}"
                )
                return

        return wrapper


async def http_get(session: aiohttp.ClientSession, url: str) -> Coroutine:
    """Execute an GET http call async """
    retries = 5
    delay = 2
    for i in range(retries):
        try:
            async with session.get(url) as response:
                resp = await response.json()
                return resp
        except Exception as e:
            if i < retries - 1:
                print(f"Retrying events failed {i} with {e}")
                time.sleep(delay)
                continue
            else:
                print("Out of retries")
                raise


async def fetch_all(urls: List, inner: Callable):
    """Gather many HTTP call made async """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                inner(
                    session,
                    url
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses

heights = remain['height']
print(heights)


def run():
    urls = [
        f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eth" for height in range(200)]
    rr = asyncio.get_event_loop().run_until_complete(fetch_all(urls, http_get))
    newdf = pd.DataFrame({'result': rr})
    # print(newdf)
    # x = pd.concat([rates, newdf]).drop_duplicates(['height'], keep='last')
    newdf.to_csv('gg.csv')


run()
