"""
btcnet_info

A package that gives you info on oodles of bitcoin pools
"""


local_api = None
__patched = False
def __patch():
    """
    Extremely magical gevent deffering patch
    """
    global __patched
    if not __patched:
        import gevent.monkey
        gevent.monkey.patch_all(thread = False, time=False)
        __patched = True
        import api, os
        global local_api
        local_api = api.API()

def get_coins():
    """
    Returns a set of coin objects.
    x.fields describes existing fields
    """
    __patch()
    return local_api.get_coins()
    
def get_pools():
    """
    Returns a set of Pool objects.
    x.fields describes existing fields
    """
    __patch()
    return local_api.get_pools()
    
def get_pool(name):
    """
    Returns a matching pool with the name
    Otherwise returns []
    """
    __patch()
    return filter(lambda x: x.name == name, local_api.get_pools())
    
def get_difficulty(coin):
    """
    Returns the difficulty of a coin
    """
    __patch()
    return local_api.get_difficulty(coin)
    
def get_exchange(coin):
    """
    Returns the exchange rate for the coin
    """
    __patch()
    return local_api.get_exchange(coin)
    

__all__ = ['get_coins', 'get_pools', 'get_difficulty']

