"""
Api Class which handles basic manipulation of objects
"""
import objects

class API():
    """
    Wrapper Class for api access
    """
    def __init__(self):
        self.objects = objects.Objects()
        
    def get_coins(self):
        """
        Returns a set of cointypes
        """
        return self.objects.coins
        
    def get_pools(self):
        """
        Returns a set of pools
        """
        return self.objects.pools
        
