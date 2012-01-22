import objects

class API():
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
        
