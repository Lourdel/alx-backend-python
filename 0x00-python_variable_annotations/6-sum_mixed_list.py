#!/usr/bin/env python3
"""Module defines sum_mixed_list function"""


from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Method returns sum of a list of mixed data types"""
    return (sum(mxd_lst))
