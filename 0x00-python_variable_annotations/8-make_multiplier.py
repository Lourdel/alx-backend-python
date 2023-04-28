#!/usr/bin/env python3
"""Module defines a function make_multiplier"""


from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Method multiplies any float by multiplier and returns a function"""
     return lambda any_float: multiplier * any_float
