#!/usr/bin/env python3

"""Module defines an async_generator function"""

import asyncio
import random
import typing


async def async_generator() -> typing.Generator[float, None, None]:
    """asynchronously yield a random number between 0 and 10"""
    for i in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
