"""
btcnet_info

A package that gives you info on oodles of bitcoin pools
"""
import api, os

local_api = api.API()

def get_coins():
    """
    Returns a set of coin objects.
    x.fields describes existing fields
    """
    return local_api.get_coins()
    
def get_pools():
    """
    Returns a set of Pool objects.
    x.fields describes existing fields
    """
    return local_api.get_pools()

__all__ = ['get_coins', 'get_pools']

