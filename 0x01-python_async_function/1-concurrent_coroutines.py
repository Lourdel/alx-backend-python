#!/usr/bin/env python3
"""Module defines wait_n method"""

import asyncio
import random
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Method executes multiple coroutines and returns a list of delays"""
    tasks = [asyncio.create_task(wait_random(max_delay)) for i in range(n)]
    delays = []
    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)
    return delays
