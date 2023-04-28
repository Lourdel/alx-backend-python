#!/usr/bin/env python3
"""Module defines a function to_kv"""


from typing import Tuple, Union


def to_kv(k: str, v: Union[int,float]) -> Tuple[str, float]:
    """Method returns a tuple"""
    return (k, float(v ** 2))
