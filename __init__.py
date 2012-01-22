import api

local_api = api.API()

def get_coins():
    return local_api.get_coins()
    
def get_pools():
    return local_api.get_pools()

__all__ = ['get_coins', 'get_pools']
